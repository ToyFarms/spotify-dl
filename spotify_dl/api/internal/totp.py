import base64
import hashlib
import hmac
import struct
import time
from typing import cast

import curl_cffi

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


def get_secret() -> tuple[str, list[int]]:
    # please read https://github.com/librespot-org/librespot/discussions/1562#discussioncomment-14659870
    # sudo docker run --rm misiektoja/spotify-secrets-grabber --secretbytes

    # TODO: do this ourself
    # {"59":[123,105,79,70,110,59,52,125,60,49,80,70,89,75,80,86,63,53,123,37,117,49,52,93,77,62,47,86,48,104,68,72],"60":[79,109,69,123,90,65,46,74,94,34,58,48,70,71,92,85,122,63,91,64,87,87],"61":[44,55,47,42,70,40,34,114,76,74,50,111,120,97,75,76,94,102,43,69,49,120,118,80,64,78]}
    # def fetch_and_update_secrets():
    #     global SECRET_CIPHER_DICT
    #
    #     if not SECRET_CIPHER_DICT_URL:
    #         return False
    #
    #     try:
    #         if SECRET_CIPHER_DICT_URL.startswith("file:"):
    #             import os
    #             from urllib.parse import urlparse, unquote
    #
    #             parsed = urlparse(SECRET_CIPHER_DICT_URL)
    #
    #             if parsed.netloc:
    #                 raw_path = f"/{parsed.netloc}{parsed.path or ''}"
    #             else:
    #                 if SECRET_CIPHER_DICT_URL.startswith("file://"):
    #                     raw_path = parsed.path or SECRET_CIPHER_DICT_URL[len("file://"):]
    #                 else:
    #                     raw_path = parsed.path or SECRET_CIPHER_DICT_URL[len("file:"):]
    #
    #             raw_path = unquote(raw_path)
    #
    #             if raw_path.startswith("/~"):
    #                 raw_path = raw_path[1:]
    #
    #             if not raw_path.startswith("/") and not raw_path.startswith("~"):
    #                 raw_path = "/" + raw_path
    #
    #             path = os.path.expanduser(os.path.expandvars(raw_path))
    #
    #             print(f"Loading Spotify web-player TOTP secrets from file: {path}")
    #             with open(path, "r", encoding="utf-8") as f:
    #                 secrets = json.load(f)
    #             print("─" * HORIZONTAL_LINE)
    #         else:
    #             print(f"Fetching Spotify web-player TOTP secrets from URL: {SECRET_CIPHER_DICT_URL}")
    #             response = req.get(SECRET_CIPHER_DICT_URL, timeout=FUNCTION_TIMEOUT, verify=VERIFY_SSL)
    #             response.raise_for_status()
    #             secrets = response.json()
    #             print("─" * HORIZONTAL_LINE)
    #
    #         if not isinstance(secrets, dict) or not secrets:
    #             raise ValueError("fetch_and_update_secrets(): Fetched payload not a non-empty dict")
    #
    #         for key, value in secrets.items():
    #             if not isinstance(key, str) or not key.isdigit():
    #                 raise ValueError(f"fetch_and_update_secrets(): Invalid key format: {key}")
    #             if not isinstance(value, list) or not all(isinstance(x, int) for x in value):
    #                 raise ValueError(f"fetch_and_update_secrets(): Invalid value format for key {key}")
    #
    #         SECRET_CIPHER_DICT = secrets
    #         return True
    #
    #     except Exception as e:
    #         print(f"fetch_and_update_secrets(): Failed to get new secrets: {e}")
    #         return False
    secret: dict[str, list[int]] = curl_cffi.get(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        "https://raw.githubusercontent.com/xyloflake/spot-secrets-go/refs/heads/main/secrets/secretDict.json"
    ).json()
    return max(secret.items(), key=lambda x: int(x[0]))  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]


def get_server_time() -> int:
    response = curl_cffi.get(
        "https://open.spotify.com/api/server-time", impersonate="chrome"
    )
    response.raise_for_status()
    return cast(int, response.json()["serverTime"])  # pyright: ignore[reportUnknownMemberType]


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
