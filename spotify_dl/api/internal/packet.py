import logging
import os

from typing import override


class PacketType:
    PACKET_TYPE_NAMES: dict[bytes, str] = {
        b"\x02": "secret_block",
        b"\x04": "ping",
        b"\x08": "stream_chunk",
        b"\x09": "stream_chunk_res",
        b"\x0a": "channel_error",
        b"\x0b": "channel_abort",
        b"\x0c": "request_key",
        b"\x0d": "aes_key",
        b"\x0e": "aes_key_error",
        b"\x19": "image",
        b"\x1b": "country_code",
        b"\x49": "pong",
        b"\x4a": "pong_ack",
        b"\x4b": "pause",
        b"\x50": "product_info",
        b"\x69": "legacy_welcome",
        b"\x76": "license_version",
        b"\xab": "login",
        b"\xac": "ap_welcome",
        b"\xad": "auth_failure",
        b"\xb2": "mercury_req",
        b"\xb3": "mercury_sub",
        b"\xb4": "mercury_unsub",
        b"\xb5": "mercury_event",
        b"\x82": "track_ended_time",
        b"\x1f": "unknown_data_all_zeros",
        b"\x74": "preferred_locale",
        b"\x4f": "unknown_0x4f",
        b"\x0f": "unknown_0x0f",
        b"\x10": "unknown_0x10",
    }

    secret_block: bytes = b"\x02"
    ping: bytes = b"\x04"
    stream_chunk: bytes = b"\x08"
    stream_chunk_res: bytes = b"\x09"
    channel_error: bytes = b"\x0a"
    channel_abort: bytes = b"\x0b"
    request_key: bytes = b"\x0c"
    aes_key: bytes = b"\x0d"
    aes_key_error: bytes = b"\x0e"
    image: bytes = b"\x19"
    country_code: bytes = b"\x1b"
    pong: bytes = b"\x49"
    pong_ack: bytes = b"\x4a"
    pause: bytes = b"\x4b"
    product_info: bytes = b"\x50"
    legacy_welcome: bytes = b"\x69"
    license_version: bytes = b"\x76"
    login: bytes = b"\xab"
    ap_welcome: bytes = b"\xac"
    auth_failure: bytes = b"\xad"
    mercury_req: bytes = b"\xb2"
    mercury_sub: bytes = b"\xb3"
    mercury_unsub: bytes = b"\xb4"
    mercury_event: bytes = b"\xb5"
    track_ended_time: bytes = b"\x82"
    unknown_data_all_zeros: bytes = b"\x1f"
    preferred_locale: bytes = b"\x74"
    unknown_0x4f: bytes = b"\x4f"
    unknown_0x0f: bytes = b"\x0f"
    unknown_0x10: bytes = b"\x10"

    @staticmethod
    def get_name(val: bytes | None) -> str:
        return PacketType.PACKET_TYPE_NAMES.get(val if val else b"", "Unknown")


class Packet:
    def __init__(self, type: bytes, payload: bytes):
        self.type: bytes = type
        self.payload: bytes = payload

    @override
    def __repr__(self) -> str:
        name = PacketType.get_name(self.type)
        try:
            truncate_length = os.get_terminal_size().columns
        except:
            truncate_length = 64

        if logging.getLogger().level >= logging.DEBUG:
            truncated = False
            s = slice(None, None)
        else:
            truncated = len(self.payload) > truncate_length
            s = slice(None, truncate_length)

        return f"Packet(name={name}, payload={self.payload[s]}{f'... ({len(self.payload) - truncate_length})' if truncated else ''})"
