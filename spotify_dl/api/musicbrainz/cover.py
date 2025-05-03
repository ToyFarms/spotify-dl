# pyright: reportAny=false
import requests

from enum import Enum, auto
from typing import cast
from collections.abc import Iterator
from urllib.request import urlopen

from spotify_dl.api.musicbrainz.mbid import MBID
from spotify_dl.model.coverartarchive import Art, ArtSize, ArtType, CAAResponse
from spotify_dl.model.id3 import ID3PictureType


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
    def to_id3(type: "CoverArtType") -> ID3PictureType:
        return {
            CoverArtType.FRONT: ID3PictureType.FRONT_COVER,
            CoverArtType.BACK: ID3PictureType.BACK_COVER,
            CoverArtType.BOOKLET: ID3PictureType.LEAFLET_PAGE,
            CoverArtType.MEDIUM: ID3PictureType.MEDIA,
            CoverArtType.TRAY: ID3PictureType.BACK_COVER,
            CoverArtType.OBI: ID3PictureType.OTHER,
            CoverArtType.SPINE: ID3PictureType.OTHER,
            CoverArtType.TRACK: ID3PictureType.OTHER,
            CoverArtType.STICKER: ID3PictureType.OTHER,
            CoverArtType.OTHER: ID3PictureType.OTHER,
            CoverArtType.POSTER: ID3PictureType.OTHER,
            CoverArtType.WATERMARK: ID3PictureType.OTHER,
            CoverArtType.LINER: ID3PictureType.LEAFLET_PAGE,
        }.get(type, ID3PictureType.OTHER)


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
    def type_as_id3(self) -> ID3PictureType:
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
        res = requests.get(f"https://coverartarchive.org/release/{self.mbid.id}")
        res.raise_for_status()

        return cast(CAAResponse, res.json())
