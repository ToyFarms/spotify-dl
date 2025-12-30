import random

import curl_cffi


def get_accesspoint() -> list[tuple[str, int]]:
    res = curl_cffi.get("https://apresolve.spotify.com/?type=accesspoint", impersonate="chrome")

    json: dict[str, list[str]] = res.json()  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
    urls = json.get("accesspoint", None)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    if urls is None:
        raise ValueError("No urls")

    return [(addr, int(port)) for addr, port in (ap.split(":", 1) for ap in urls)]  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportUnknownArgumentType]


def get_spclient() -> list[tuple[str, int]]:
    res = curl_cffi.get("https://apresolve.spotify.com/?type=spclient", impersonate="chrome")

    json: dict[str, list[str]] = res.json()  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
    urls = json.get("spclient", None)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
    if urls is None:
        raise ValueError("No urls")

    return [(addr, int(port)) for addr, port in (ap.split(":", 1) for ap in urls)]  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType, reportUnknownMemberType]


def get_random_accesspoint() -> tuple[str, int]:
    return random.choice(get_accesspoint())


def get_random_spclient() -> tuple[str, int]:
    return random.choice(get_spclient())
