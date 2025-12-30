# pyright: reportAny=false, reportExplicitAny=false
from typing import Self, cast

import curl_cffi


class MBID:
    def __init__(self, id: str) -> None:
        self.id: str = id

    @classmethod
    def from_isrc(cls, isrc: str) -> Self:
        res = curl_cffi.get(
            f"https://musicbrainz.org/ws/2/recording/?query=isrc:{isrc}&fmt=json",
            impersonate="chrome",
        )
        res.raise_for_status()

        json = res.json()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        ret = cls(cast(str, json["recordings"][0]["releases"][0]["id"]))

        return ret

