import threading

from queue import Queue
from typing import Protocol


class BaseAudioBackend(Protocol):
    start_event: threading.Event
    exit_event: threading.Event
    finished: bool

    def play(self, buffer: Queue[bytes]) -> None: ...
    def stop(self) -> None: ...
    def close(self) -> None: ...
    def set_volume(self, volume: float, duration: float = 1.0) -> None: ...
