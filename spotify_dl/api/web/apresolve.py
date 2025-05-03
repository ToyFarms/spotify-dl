import random
import requests


def get_accesspoint() -> list[tuple[str, int]]:
    res = requests.get("https://apresolve.spotify.com/?type=accesspoint")

    json: dict[str, list[str]] = res.json()
    urls = json.get("accesspoint", None)
    if urls is None:
        raise ValueError("No urls")

    return [(addr, int(port)) for addr, port in (ap.split(":", 1) for ap in urls)]


def get_random_accesspoint() -> tuple[str, int]:
    return random.choice(get_accesspoint())
