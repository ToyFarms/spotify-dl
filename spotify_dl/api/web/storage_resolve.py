from typing import TypedDict, cast
from requests import Session


class StorageResolve(TypedDict):
    result: str
    cdnurl: list[str]
    fileid: str
    ttl: int


def storage_resolve(session: Session, file_id: str) -> StorageResolve:
    res = session.get(
        f"https://gew4-spclient.spotify.com/storage-resolve/v2/files/audio/interactive/10/{file_id}",
        params={
            "version": 10000000,
            "product": 9,
            "platform": 39,
            "alt": "json",
        },
    )

    res.raise_for_status()

    return cast(StorageResolve, res.json())
