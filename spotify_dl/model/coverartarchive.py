from typing import Literal, TypedDict

from spotify_dl.model.shared import URL


type ArtSize = Literal["1200", "500", "250", "large", "small"]


Thumbnail = TypedDict(
    "Thumbnail",
    {
        "1200": URL,
        "500": URL,
        "250": URL,
        "large": URL,
        "small": URL,
    },
)


type ArtType = Literal[
    "FRONT",
    "BACK",
    "BOOKLET",
    "MEDIUM",
    "TRAY",
    "OBI",
    "SPINE",
    "TRACK",
    "STICKER",
    "OTHER",
    "POSTER",
    "WATERMARK",
    "LINER",
]


class Art(TypedDict):
    approved: bool
    back: bool
    comment: str
    edit: int
    front: bool
    id: str
    image: URL
    thumbnails: Thumbnail
    types: list[ArtType]


class CAAResponse(TypedDict):
    images: list[Art]
    release: URL
