import binascii
import logging
import re

from enum import Enum, auto
from typing import Self, TypedDict, cast
from urllib.parse import urlparse
from dataclasses import dataclass

import curl_cffi

from spotify_dl.api.internal.proto.extension_kind_pb2 import ExtensionKind
from spotify_dl.api.internal.spotify_client import SpotifyClient
from spotify_dl.api.web.apresolve import get_random_spclient
from spotify_dl.auth.clienttoken import ClientToken
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.format import AudioFormat
from spotify_dl.model.getTrack_gql import GraphQLResponse, TrackUnion
from spotify_dl.model.web import ManifestFileMP4, MediaResponse
from spotify_dl.utils.bytes_stuff import to_bytes
from spotify_dl.api.internal.proto.extended_metadata_pb2 import (
    EntityRequest,
    BatchedEntityRequest,
    ExtensionQuery,
    BatchedExtensionResponse,
)
from spotify_dl.api.internal.proto import metadata_pb2 as Metadata


class AudioFile(TypedDict):
    file_id: str
    format: str


class Track:
    logger: logging.Logger = logging.Logger("spdl:track")

    class Type(Enum):
        ALBUM = auto()
        ARTIST = auto()
        EPISODE = auto()
        PLAYLIST = auto()
        SHOW = auto()
        TRACK = auto()
        LOCAL = auto()
        UNKNOWN = auto()

    BASE62_LEN: int = 22

    def __init__(self, id_base62: str, id_base16: str, type: Type) -> None:
        # used by web api (e.g. track url)
        self.id_b62: str = id_base62
        # used by internal api
        self.id_b16: str = id_base16
        self.type: Track.Type = type

        # TODO: global caching system
        self._metadata: TrackUnion | None = None
        self._metadata_internal: Metadata.Track | None = None
        self._manifest: MediaResponse | None = None
        self.format: AudioFormat | None = None

    def get_mp4_manifest(
        self, auth: SpotifyAuthPKCE, file_id: str
    ) -> list[ManifestFileMP4]:
        def get() -> list[ManifestFileMP4]:
            # TODO: why is uri sometimes different in the response?
            assert self._manifest
            try:
                return self._manifest["media"][uri]["item"]["manifest"]["file_ids_mp4"]
            except KeyError:
                return next(iter(self._manifest["media"].values()))["item"]["manifest"]["file_ids_mp4"]

        uri = f"spotify:track:{file_id}"
        if self._manifest:
            return get()

        res = auth.session.get(
            f"https://{get_random_spclient()[0]}/track-playback/v1/media/{uri}?manifestFileFormat=file_ids_mp4"
        )
        res.raise_for_status()

        self._manifest = cast(
            MediaResponse, res.json()  # pyright: ignore[reportUnknownMemberType]
        )
        return get()

    def get_metadata_internal(
        self,
        auth: SpotifyAuthPKCE,
    ) -> Metadata.Track:
        if self._metadata_internal:
            return self._metadata_internal

        query = ExtensionQuery(extension_kind=ExtensionKind.TRACK_V4)
        req = EntityRequest(entity_uri=f"spotify:track:{self.id_b62}", query=[query])
        batched_req = BatchedEntityRequest(entity_request=[req])
        res = auth.session.post(
            "https://spclient.wg.spotify.com/extended-metadata/v0/extended-metadata",
            headers={"Content-Type": "application/x-protobuf"},
            data=batched_req.SerializeToString(),
        )
        res.raise_for_status()

        batched_res = BatchedExtensionResponse()
        _ = batched_res.ParseFromString(res.content)

        data = batched_res.extended_metadata[0].extension_data[0].extension_data.value

        self._metadata_internal = Metadata.Track()
        _ = self._metadata_internal.ParseFromString(data)

        return self._metadata_internal

    def get_metadata(self) -> TrackUnion:
        from spotify_dl.state import state

        if self._metadata:
            return self._metadata

        if not state.client:
            state.client = SpotifyClient.random_ap(state.auth)

        if not state.clienttoken:
            state.clienttoken = ClientToken(state.client)

        res = curl_cffi.post(
            "https://api-partner.spotify.com/pathfinder/v2/query",
            json={
                "variables": {"uri": f"spotify:track:{self.id_b62}"},
                "operationName": "getTrack",
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "d208301e63ccb8504831114cb8db1201636a016187d7c832c8c00933e2cd64c6",
                    }
                },
            },
            headers={
                "authorization": f"Bearer {state.auth.token}",
                "client-token": state.ensure_clienttoken().token,
            },
            impersonate="chrome",
        )
        res.raise_for_status()
        json = cast(
            GraphQLResponse, res.json()  # pyright: ignore[reportUnknownMemberType]
        )

        self._metadata = json["data"]["trackUnion"]
        return self._metadata

    def get_formats(self, auth: SpotifyAuthPKCE) -> list[AudioFormat]:
        metadata = self.get_metadata_internal(auth)

        files: list[Metadata.AudioFile] = list(metadata.file) or list(
            metadata.alternative[0].file
        )
        if not files:
            raise ValueError("Expecting a list of files")

        mp4s = self.get_mp4_manifest(auth, self.id_b62)

        MP4_QUALITY = {
            128000: AudioFormat.Type.MP4_128,
            256000: AudioFormat.Type.MP4_256,
        }

        return [
            AudioFormat(
                AudioFormat.Type.from_proto(file.format),
                binascii.hexlify(file.file_id).decode(),
                binascii.hexlify(metadata.gid).decode(),
            )
            for file in files
        ] + [
            AudioFormat(
                MP4_QUALITY[mp4["bitrate"]],
                mp4["file_id"],
                binascii.hexlify(metadata.gid).decode(),
            )
            for mp4 in mp4s
        ]

    def get_format(
        self,
        auth: SpotifyAuthPKCE,
        target_format: AudioFormat.Type,
    ) -> AudioFormat | None:
        for format in self.get_formats(auth):
            if format.type == target_format:
                return format

    def set_format(self, format: AudioFormat) -> None:
        self.format = format

    @classmethod
    def probe(cls, s: str) -> Self:
        if s.startswith("spotify:"):
            return cls.from_uri(s)
        elif re.match(r"^https?://.*/track/.*$", s):
            return cls.from_url(s)
        elif len(s) == cls.BASE62_LEN:
            return cls.from_base62(s)
        else:
            raise ValueError(f"Unknown format: {s}")

    @classmethod
    def from_url(cls, url: str) -> Self:
        # https://open.spotify.com/track/abcdef?si=abcdef

        url_parts = urlparse(url)
        parts = url_parts.path.removeprefix("/").split("/")

        id = ""
        type = Track.Type.UNKNOWN

        try:
            if parts[0] != "track":
                raise ValueError("Expected <spotify>/track/<id> from url")

            id = parts[1]
        except IndexError:
            raise ValueError(f"Invalid URL: {url}")

        return cls(id, cls.decode_base62(id), type)

    @classmethod
    def from_uri(cls, uri: str) -> Self:
        # Basic: `spotify:{type}:{id}`
        # Named: `spotify:user:{user}:{type}:{id}`
        # Local: `spotify:local:{artist}:{album_title}:{track_title}:{duration_in_seconds}`

        id = ""
        type = Track.Type.UNKNOWN
        parts = uri.split(":")

        try:
            scheme = parts[0]
            if scheme != "spotify":
                raise ValueError(
                    f'Expected "spotify" as the first part of the uri, found "{scheme}"'
                )

            if parts[1] == "user":
                id = parts[4]
                type = Track.Type[parts[3].upper()]
            elif parts[1] == "local":
                raise ValueError("Local track is not supported")
            else:
                id = parts[2]
                type = Track.Type[parts[1].upper()]
        except IndexError:
            raise ValueError(f"Invalid URI: {uri}")

        return cls(id, cls.decode_base62(id), type)

    @staticmethod
    def decode_base62(id: str | bytes) -> str:
        s = id.decode() if isinstance(id, bytes) else id
        if len(s) != Track.BASE62_LEN:
            raise ValueError(f"Expected id to have length of 22, but its {len(s)}")

        spid = 0
        for c in s:
            if "0" <= c <= "9":
                p = ord(c) - ord("0")
            elif "a" <= c <= "z":
                p = ord(c) - ord("a") + 10
            elif "A" <= c <= "Z":
                p = ord(c) - ord("A") + 36
            else:
                raise ValueError("Invalid base62 character")

            spid = spid * 62 + p

        return to_bytes(spid).hex()

    @classmethod
    def from_base62(cls, id: str | bytes) -> Self:
        return cls(
            id if isinstance(id, str) else id.decode("utf-8"),
            cls.decode_base62(id),
            Track.Type.UNKNOWN,
        )


@dataclass
class ReplayGain:
    track_gain_db: float
    track_peak: float
    album_gain_db: float
    album_peak: float


@dataclass
class TrackHeader:
    replaygain: ReplayGain
