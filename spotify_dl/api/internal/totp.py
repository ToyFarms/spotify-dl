import base64
import hashlib
import hmac
import struct
import time
from typing import cast
import requests

from spotify_dl.utils.misc import url_build


def generate_totp(
    secret: str | bytes,
    digits: int,
    period: int,
    _time: int | float | None = None,
) -> str:
    if isinstance(secret, str):
        secret = secret.upper()
        padding = "=" * ((8 - len(secret) % 8) % 8)
        secret = base64.b32decode(secret + padding)

    if _time is None:
        _time = time.time()

    counter = int(_time // period)
    counter_bytes = struct.pack(">Q", counter)

    hmac_digest = hmac.new(secret, counter_bytes, hashlib.sha1).digest()

    offset = hmac_digest[-1] & 0x0F
    code_bytes = hmac_digest[offset : offset + 4]
    code_int = cast(int, struct.unpack(">I", code_bytes)[0] & 0x7FFFFFFF)

    otp = cast(int, code_int % (10**digits))
    return str(otp).zfill(digits)


def get_secret() -> tuple[int, list[int]]:
    # please read https://github.com/librespot-org/librespot/discussions/1562#discussioncomment-14659870
    # sudo docker run --rm misiektoja/spotify-secrets-grabber --secretbytes
    return (
        61,
        [
            44,
            55,
            47,
            42,
            70,
            40,
            34,
            114,
            76,
            74,
            50,
            111,
            120,
            97,
            75,
            76,
            94,
            102,
            43,
            69,
            49,
            120,
            118,
            80,
            64,
            78,
        ],
    )


def get_server_time() -> int:
    response = requests.get("https://open.spotify.com/api/server-time")
    response.raise_for_status()
    return cast(int, response.json()["serverTime"])


def create_otp_auth_url() -> str:
    version, secret = get_secret()
    transformed = [e ^ ((t % 33) + 9) for t, e in enumerate(secret)]
    joined = "".join(str(num) for num in transformed)
    hex_str = joined.encode().hex()
    secret32 = base64.b32encode(bytes.fromhex(hex_str)).decode().rstrip("=")

    server_time = get_server_time()
    otp = generate_totp(secret32, 6, 30, server_time)

    return url_build(
        "https://open.spotify.com/api/token",
        reason="init",
        productType="web-player",
        totp=otp,
        totpServer=otp,
        totpVer=version,
    )
