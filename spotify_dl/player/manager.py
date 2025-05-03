import threading
import time

from queue import Queue

from spotify_dl.player.backend.base import BaseAudioBackend
from spotify_dl.player.backend.mpv_backend import MPVAudioBackend


class MultiAudioManager:
    def __init__(self, backend: type[BaseAudioBackend] = MPVAudioBackend) -> None:
        self._backend: type[BaseAudioBackend] = backend
        self.streams: list[BaseAudioBackend] = []
        self.master_volume: float = 100.0

        self._running: bool = False
        self._thread: threading.Thread = threading.Thread(
            target=self._update_thread, daemon=True
        )
        self._thread.start()

    def add_stream(self) -> Queue[bytes]:
        backend = self._backend()
        self.streams.append(backend)

        buffer: Queue[bytes] = Queue()
        backend.play(buffer)

        return buffer

    def shutdown(self) -> None:
        self._running = False
        self._thread.join()
        for b in self.streams:
            b.close()
        self.streams.clear()

    # TODO: better way of managing active & inactive stream
    def _update_thread(self) -> None:
        self._running = True

        while self._running:
            for backend in list(self.streams):
                if backend.finished:
                    backend.close()
                    self.streams.remove(backend)

            if not self.streams:
                time.sleep(0.1)
                continue

            active = self.streams[0]
            active.set_volume(self.master_volume, duration=1.0)

            for bk in self.streams[1:]:
                bk.set_volume(0.0, duration=1.0)

            time.sleep(0.1)
