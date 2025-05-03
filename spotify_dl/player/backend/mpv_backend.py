# pyright: reportUnknownMemberType=false
import logging
import threading

from queue import Empty, Queue
from typing import override

from spotify_dl.player.backend.base import BaseAudioBackend
from spotify_dl.player.vendor.mpv import MPV, ShutdownError
from spotify_dl.utils.fifo import Fifo
from spotify_dl.utils.interpolator import (
    EasingFunction,
    interpolate,
    interpolate_remove,
)
from spotify_dl.utils.misc import close_enough


class MPVAudioBackend(BaseAudioBackend):
    logger: logging.Logger = logging.getLogger("spdl:audio:mpv")

    def __init__(self) -> None:
        def my_log(loglevel: str, component: str, message: str) -> None:
            print("[{}] {}: {}".format(loglevel, component, message), end="")

        self.mpv: MPV = MPV(log_handler=my_log, loglevel="debug")
        self.buffer: Queue[bytes] = Queue()

        self.start_event: threading.Event = threading.Event()
        self.exit_event: threading.Event = threading.Event()
        self._lock: threading.Lock = threading.Lock()
        self.volume: float = 100
        self.finished: bool = False

        self.fifo: Fifo = Fifo(mode="w")

        threading.Thread(target=self._feed_thread, daemon=True).start()

    def _feed_thread(self) -> None:
        with self.fifo.open() as f:
            self.start_event.set()
            while True:
                data = self.buffer.get()
                if not data:
                    break

                _ = f.write(data)
                f.flush()

        self.mpv.wait_for_playback()

        self.finished = True
        self.fifo.close()
        self.exit_event.set()

    @override
    def play(self, buffer: Queue[bytes]) -> None:
        if self.start_event.is_set():
            self.stop()

        self.start_event.clear()
        self.exit_event.clear()

        self.buffer = buffer
        self.mpv.play(self.fifo.path)

        if not self.start_event.wait(timeout=1.0):
            self.logger.warning("MPV stream callback never fired")

    @override
    def stop(self) -> None:
        self.start_event.clear()

        with self._lock:
            self._clear_queue(self.buffer)
        self.buffer.put(b"")

        _ = self.exit_event.wait(timeout=3)
        self.mpv.stop()

    @override
    def close(self) -> None:
        interpolate_remove(f"volinterp{id(self)}")
        self.fifo.close()
        self.stop()
        self.mpv.terminate()

    @override
    def set_volume(self, volume: float, duration: float = 1.0) -> None:
        def set_vol(x: float) -> None:
            try:
                self.mpv.check_core_alive()
            except ShutdownError:
                return

            if isinstance(self.mpv.volume, float) and close_enough(self.mpv.volume, x):
                return

            self.mpv.volume = x

        interpolate(
            self.volume,
            volume,
            duration,
            set_vol,
            EasingFunction.ease_in_out_quad,
            key=f"volinterp{id(self)}",
        )
        self.volume = volume

    def _clear_queue[T](self, q: Queue[T]) -> None:
        try:
            while True:
                _ = q.get_nowait()
                q.task_done()
        except Empty:
            pass
