# pyright: reportAny=false

from enum import Enum, auto
from typing import cast
from collections.abc import Iterator
from urllib.request import urlopen

import curl_cffi

from spotify_dl.api.musicbrainz.mbid import MBID
from spotify_dl.model.coverartarchive import Art, ArtSize, ArtType, CAAResponse
from spotify_dl.model.id3 import ID3Picture


class CoverArtType(Enum):
    FRONT = auto()
    BACK = auto()
    BOOKLET = auto()
    MEDIUM = auto()
    TRAY = auto()
    OBI = auto()
    SPINE = auto()
    TRACK = auto()
    STICKER = auto()
    OTHER = auto()
    POSTER = auto()
    WATERMARK = auto()
    LINER = auto()

    @staticmethod
    def to_id3(type: "CoverArtType") -> ID3Picture:
        return {
            CoverArtType.FRONT: ID3Picture.FRONT_COVER,
            CoverArtType.BACK: ID3Picture.BACK_COVER,
            CoverArtType.BOOKLET: ID3Picture.LEAFLET_PAGE,
            CoverArtType.MEDIUM: ID3Picture.MEDIA,
            CoverArtType.TRAY: ID3Picture.BACK_COVER,
            CoverArtType.OBI: ID3Picture.OTHER,
            CoverArtType.SPINE: ID3Picture.OTHER,
            CoverArtType.TRACK: ID3Picture.OTHER,
            CoverArtType.STICKER: ID3Picture.OTHER,
            CoverArtType.OTHER: ID3Picture.OTHER,
            CoverArtType.POSTER: ID3Picture.OTHER,
            CoverArtType.WATERMARK: ID3Picture.OTHER,
            CoverArtType.LINER: ID3Picture.LEAFLET_PAGE,
        }.get(type, ID3Picture.OTHER)


class CoverArt:
    def __init__(self, art: Art) -> None:
        self.data: Art = art

    def fetch(self, size: ArtSize) -> bytes:
        data = urlopen(self.data["thumbnails"][size])
        return data.read()

    @property
    def type(self) -> CoverArtType:
        return CoverArtType[self.data["types"][0].upper()]

    @property
    def type_as_id3(self) -> ID3Picture:
        return CoverArtType.to_id3(self.type)


class CoverArts:
    _cache: dict[str, CAAResponse] = {}

    def __init__(self, mbid: MBID) -> None:
        self.mbid: MBID = mbid
        if mbid.id in CoverArts._cache:
            self.res = CoverArts._cache[mbid.id]
        else:
            self.res: CAAResponse = self._request()
            CoverArts._cache[mbid.id] = self.res

    def get_type(self, type: ArtType) -> CoverArt | None:
        art = None
        for image in self.res["images"]:
            if image["types"][0].upper() == type:
                return CoverArt(image)

        if not art:
            return None

    def get_images(self) -> Iterator[CoverArt]:
        for image in self.res["images"]:
            yield CoverArt(image)

    def fetch(self, type: ArtType, size: ArtSize) -> bytes | None:
        art = self.get_type(type)
        if not art:
            return None

        return art.fetch(size)

    def _request(self) -> CAAResponse:
        res = curl_cffi.get(f"https://coverartarchive.org/release/{self.mbid.id}", impersonate="chrome")
        res.raise_for_status()

        return cast(CAAResponse, res.json())
