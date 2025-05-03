# pyright: reportAny=false, reportExplicitAny=false
from typing import Self, cast

import requests


class MBID:
    def __init__(self, id: str) -> None:
        self.id: str = id

    @classmethod
    def from_isrc(cls, isrc: str) -> Self:
        res = requests.get(
            f"https://musicbrainz.org/ws/2/recording/?query=isrc:{isrc}&fmt=json",
        )
        res.raise_for_status()

        json = res.json()
        ret = cls(cast(str, json["recordings"][0]["releases"][0]["id"]))

        return ret

