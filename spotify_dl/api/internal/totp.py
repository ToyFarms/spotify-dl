import base64
import hashlib
import hmac
import struct
import time
import requests

from datetime import datetime

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
    code_int: int = struct.unpack(">I", code_bytes)[0] & 0x7FFFFFFF

    otp: int = code_int % (10**digits)
    return str(otp).zfill(digits)


def create_otp_auth_url() -> str:
    MAGIC = "GU2TANZRGQ2TQNJTGQ4DONBZHE2TSMRSGQ4DMMZQGMZDSMZUG4"

    res = requests.get("https://open.spotify.com/server-time")
    res.raise_for_status()

    server_time: int = res.json()["serverTime"]
    client_time = int(time.time())

    server_otp = generate_totp(MAGIC, 6, 30, server_time * 1000)
    client_otp = generate_totp(MAGIC, 6, 30, client_time)

    return url_build(
        "https://open.spotify.com/get_access_token",
        reason="init",
        productType="web-player",
        totp=client_otp,
        totpServer=server_otp,
        totpVer=5,
        sTime=server_time,
        cTime=client_time,
        buildVer="web-player_2025-04-15_1744718071728_74d63e8",
        buildDate=datetime.now().strftime("%Y-%m-%d"),
    )
