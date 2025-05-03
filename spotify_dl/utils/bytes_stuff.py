import binascii
import os

from typing import Literal


def to_bytes(
    n: int,
    byteorder: Literal["little", "big"] = "big",
    signed: bool = False,
) -> bytes:
    if n == 0:
        return b"\x00"

    if signed and n < 0:
        bit_length = n.bit_length() + 1
    else:
        bit_length = n.bit_length()

    byte_length = (bit_length + 7) // 8

    return n.to_bytes(byte_length, byteorder, signed=signed)


def random_hex_string(length: int) -> str:
    buffer = os.urandom(int(length / 2))
    return binascii.hexlify(buffer).decode()
