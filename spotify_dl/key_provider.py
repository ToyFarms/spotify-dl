from typing import Protocol


class KeyProvider(Protocol):
    def get_audio_key(self, gid: bytes, file_id: bytes) -> bytes | None:
        pass
