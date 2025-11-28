import ctypes
from pathlib import Path

path = Path(__file__).parent / "playplay.so"
playplay: ctypes.CDLL | None = None


def playplay_decrypt(key: bytes, file_id: bytes) -> bytes:
    global playplay

    if playplay is None:
        if not path.exists():
            print("PlayPlay not compiled, compile using make in the playplay directory")
            return b""
        playplay = ctypes.CDLL(str(path))

    # TODO: this could potentially be outdated
    # https://github.com/devgianlu/go-librespot/issues/23
    ret = bytes(16)
    playplay.decrypt_main(key, ret)

    ret2 = bytes(16)
    playplay.bind_key(ret, file_id, ret2)

    return ret2
