import logging
import re

from enum import Enum, auto
from typing import Self, TypedDict, cast
from urllib.parse import urlparse
from dataclasses import dataclass

from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.format import AudioFormat
from spotify_dl.model.web import TrackMetadata
from spotify_dl.model.internal import TrackMetadata as ITrackMetadata
from spotify_dl.utils.bytes_stuff import to_bytes


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

        self._metadata: TrackMetadata | None = None
        self._metadata_internal: ITrackMetadata | None = None
        self.format: AudioFormat | None = None

    def get_metadata_internal(
        self,
        auth: SpotifyAuthPKCE,
    ) -> ITrackMetadata:
        if self._metadata_internal:
            return self._metadata_internal

        res = auth.session.get(
            f"https://spclient.wg.spotify.com/metadata/4/track/{self.id_b16}?market=from_token",
            headers={"Accept": "application/json"},
        )
        res.raise_for_status()

        self._metadata_internal = cast(ITrackMetadata, res.json())
        self.logger.debug(self._metadata_internal)

        return self._metadata_internal

    def get_metadata(
        self,
        auth: SpotifyAuthPKCE,
        fields: str | None = None,
    ) -> TrackMetadata:
        if self._metadata:
            return self._metadata

        fields = f"&fields={fields}" if fields else ""
        res = auth.session.get(
            f"https://api.spotify.com/v1/tracks/{self.id_b62}{fields}?market=from_token",
            headers={"Accept": "application/json"},
        )
        res.raise_for_status()

        self._metadata = cast(TrackMetadata, res.json())
        self.logger.debug(self._metadata_internal)

        return self._metadata

    def get_formats(self, auth: SpotifyAuthPKCE) -> list[AudioFormat]:
        metadata = self.get_metadata_internal(auth)
        files: list[AudioFile] | None = metadata.get("file") or metadata.get(
            "alternative"
        )
        if not files:
            raise ValueError("Expecting a list of files")

        try:
            if "file" in files[0] and isinstance(cast(object, files[0]["file"]), list):
                files = files[0]["file"]
        except Exception:
            pass

        return [
            AudioFormat(
                AudioFormat.Type[file["format"]],
                file["file_id"],
                metadata["gid"],
            )
            for file in files
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
