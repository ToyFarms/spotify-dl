from typing import TypedDict, cast

import curl_cffi


class StorageResolve(TypedDict):
    result: str
    cdnurl: list[str]
    fileid: str
    ttl: int


def storage_resolve(session: curl_cffi.Session, file_id: str) -> StorageResolve:
    res = session.get(
        f"https://gew4-spclient.spotify.com/storage-resolve/v2/files/audio/interactive/10/{file_id}",
        params={
            "version": 10000000,
            "product": 9,
            "platform": 39,
            "alt": "json",
        },
        impersonate="chrome",
    )

    res.raise_for_status()

    return cast(StorageResolve, res.json())  # pyright: ignore[reportUnknownMemberType]
