import time
from Cryptodome.Hash import SHA1
from google.protobuf.duration_pb2 import Duration
from spotify_dl.api.internal.proto.spotify.login5.v3.challenges.hashcash_pb2 import (
    HashcashChallenge,
    HashcashSolution,
)


def _trailing_zeros8(b: int) -> int:
    b &= 0xFF
    if b == 0:
        return 8
    tz = 0
    while (b & 1) == 0:
        tz += 1
        b >>= 1
    return tz


def _check_hashcash(digest: bytes, length: int) -> bool:
    idx = len(digest) - 1
    while idx >= 0:
        zeros = _trailing_zeros8(digest[idx])
        if zeros >= length:
            return True
        elif zeros < 8:
            return False
        length -= 8
        idx -= 1
    return False


def _increment_hashcash(data: bytearray, idx: int, offset: int) -> None:
    i = idx + offset
    while i >= offset:
        data[i] = (data[i] + 1) & 0xFF
        if data[i] != 0:
            break
        i -= 1


def solve_hash_cash(
    login_context: bytes, hashcash: HashcashChallenge
) -> HashcashSolution:
    suffix = bytearray(16)
    suffix[:8] = SHA1.new(login_context).digest()[12:20]

    hash = SHA1.new()
    start = time.time_ns()

    while True:
        hash.update(hashcash.prefix)
        hash.update(suffix)

        if _check_hashcash(hash.digest(), hashcash.length):
            elapsed = time.time_ns() - start
            return HashcashSolution(
                suffix=bytes(suffix),
                duration=Duration(
                    seconds=int(elapsed / 1e9),
                    nanos=int(elapsed % 1e9),
                ),
            )

        _increment_hashcash(suffix, idx=7, offset=0)
        _increment_hashcash(suffix, idx=7, offset=8)
