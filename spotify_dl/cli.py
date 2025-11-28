# pyright: reportAny=false, reportExplicitAny=false
import sys
import threading
import time
import readline
from typing import Any, BinaryIO, Callable, TextIO, final

from spotify_dl.downloader import SpotifyDownloadManager


class ThreadSafeBinaryBuffer:
    def __init__(
        self,
        orig_text_stream: TextIO,
        orig_buffer: BinaryIO,
        console_lock: threading.Lock,
        get_status_text: Callable[[], str],
        is_prompting: Callable[[], bool],
    ):
        self._text: TextIO = orig_text_stream
        self._buffer: BinaryIO = orig_buffer
        self._lock: threading.Lock = console_lock
        self._get_status_text: Callable[[], str] = get_status_text
        self._is_prompting: Callable[[], bool] = is_prompting
        self._status_printed: bool = False

    def write(self, data: object) -> int:
        if not isinstance(data, (bytes, bytearray)):
            data = str(data).encode(
                getattr(self._text, "encoding", "utf-8"), errors="replace"
            )

        with self._lock:
            if self._status_printed:
                try:
                    _ = self._text.write("\x1b[s\x1b[1A\x1b[2K\x1b[u")
                    self._text.flush()
                except Exception:
                    pass
                self._status_printed = False

            written = 0
            try:
                written = self._buffer.write(data)
                try:
                    self._buffer.flush()
                except Exception:
                    pass
            except Exception:
                try:
                    _ = self._text.write(
                        data.decode(
                            getattr(self._text, "encoding", "utf-8"), errors="replace"
                        )
                    )
                    self._text.flush()
                    written = len(data)
                except Exception:
                    written = 0

            if self._is_prompting():
                if not data.endswith(b"\n"):
                    try:
                        try:
                            _ = self._buffer.write(b"\n")
                            try:
                                self._buffer.flush()
                            except Exception:
                                pass
                        except Exception:
                            _ = self._text.write("\n")
                            self._text.flush()
                    except Exception:
                        pass

                try:
                    status = self._get_status_text()
                    _ = self._text.write("\x1b[s\x1b[1A\x1b[2K")
                    _ = self._text.write(status + "\n")
                    _ = self._text.write("\x1b[u")
                    self._text.flush()
                    self._status_printed = True
                    try:
                        readline.redisplay()
                    except Exception:
                        pass
                except Exception:
                    self._status_printed = False
            else:
                self._status_printed = False

            return written

    def flush(self):
        try:
            self._buffer.flush()
        except Exception:
            pass

    def __getattr__(self, name: str) -> Any:
        return getattr(self._buffer, name)


class ThreadSafeStream:
    def __init__(
        self,
        original: TextIO,
        console_lock: threading.Lock,
        get_status_text: Callable[[], str],
        is_prompting: Callable[[], bool],
    ) -> None:
        self._orig: TextIO = original
        self._lock: threading.Lock = console_lock
        self._get_status_text: Callable[[], str] = get_status_text
        self._is_prompting: Callable[[], bool] = is_prompting
        self._status_printed: bool = False

        orig_buffer: BinaryIO | None = getattr(original, "buffer", None)
        self._buffer_wrapper: ThreadSafeBinaryBuffer | None = None
        if orig_buffer is not None:
            self._buffer_wrapper = ThreadSafeBinaryBuffer(
                original, orig_buffer, console_lock, get_status_text, is_prompting
            )

    def write(self, data: object) -> int:
        if not isinstance(data, str):
            data = str(data)

        with self._lock:
            if self._status_printed:
                try:
                    _ = self._orig.write("\x1b[s\x1b[1A\x1b[2K\x1b[u")
                    self._orig.flush()
                except Exception:
                    pass
                self._status_printed = False

            written = 0
            try:
                written = self._orig.write(data)
                try:
                    self._orig.flush()
                except Exception:
                    pass
            except Exception:
                if self._buffer_wrapper is not None:
                    try:
                        b = data.encode(
                            getattr(self._orig, "encoding", "utf-8"), errors="replace"
                        )
                        written = self._buffer_wrapper.write(b)
                    except Exception:
                        written = 0

            if self._is_prompting():
                try:
                    if not data.endswith("\n"):
                        try:
                            _ = self._orig.write("\n")
                            self._orig.flush()
                        except Exception:
                            if self._buffer_wrapper is not None:
                                try:
                                    _ = self._buffer_wrapper.write(b"\n")
                                except Exception:
                                    pass

                    status = self._get_status_text()
                    _ = self._orig.write("\x1b[s\x1b[1A\x1b[2K")
                    _ = self._orig.write(status + "\n")
                    _ = self._orig.write("\x1b[u")
                    self._orig.flush()
                    self._status_printed = True
                    try:
                        readline.redisplay()
                    except Exception:
                        pass
                except Exception:
                    self._status_printed = False
            else:
                self._status_printed = False

            return written

    def writelines(self, lines: list[object]) -> None:
        for line in lines:
            _ = self.write(line)

    def flush(self) -> None:
        try:
            self._orig.flush()
        except Exception:
            pass

    @property
    def buffer(self):
        return (
            self._buffer_wrapper
            if self._buffer_wrapper is not None
            else getattr(self._orig, "buffer", None)
        )

    @property
    def encoding(self):
        return getattr(self._orig, "encoding", "utf-8")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._orig, name)

    def fileno(self):
        return getattr(self._orig, "fileno", lambda: -1)()

    def isatty(self):
        return getattr(self._orig, "isatty", lambda: False)()


@final
class CLI:
    def __init__(self, download_manager: SpotifyDownloadManager) -> None:
        self.dm = download_manager
        self.prompting = False
        self.heartbeat = True
        self._console_lock = threading.Lock()

        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr

        def get_status_text() -> str:
            return f"({'*' if self.heartbeat else ' '})[{self._collect_status_lines()}]"

        def is_prompting() -> bool:
            return self.prompting

        sys.stdout = ThreadSafeStream(
            self._orig_stdout, self._console_lock, get_status_text, is_prompting
        )
        sys.stderr = ThreadSafeStream(
            self._orig_stderr, self._console_lock, get_status_text, is_prompting
        )

        self._status_thread = threading.Thread(target=self._status_updater, daemon=True)
        self._status_thread.start()

    def restore_streams(self) -> None:
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr

    def _collect_status_lines(self) -> str:
        try:
            active = self.dm.get_active()
            queued = self.dm.get_queued()
        except Exception:
            active, queued = [], []
        status: list[str] = []
        for dl, _ in active:
            try:
                status.append(f"{dl.get_percentage()*100:.0f}%")
            except Exception:
                status.append("??%")
        return f"{len(active)}/{len(queued)}{', ' if status else ''}{'|'.join(status)}"

    def _status_updater(self) -> None:
        interval = 0.2
        while True:
            time.sleep(interval)
            self.heartbeat = not self.heartbeat
            if not self.prompting:
                continue
            with self._console_lock:
                try:
                    _ = self._orig_stdout.write("\x1b[s\x1b[1A\x1b[1G\x1b[2K")
                    _ = self._orig_stdout.write(
                        f"({'*' if self.heartbeat else ' '})[{self._collect_status_lines()}]\n"
                    )
                    _ = self._orig_stdout.write("\x1b[u")
                    _ = self._orig_stdout.flush()
                except Exception:
                    pass
                try:
                    readline.redisplay()
                except Exception:
                    pass

    def prompt(self, prompt_text: str = "") -> str:
        try:
            self.prompting = True
            with self._console_lock:
                try:
                    _ = self._orig_stdout.write(
                        f"({'*' if self.heartbeat else ' '})[{self._collect_status_lines()}]\n"
                    )
                    _ = self._orig_stdout.flush()
                except Exception:
                    pass
            return input(prompt_text)
        finally:
            with self._console_lock:
                try:
                    _ = self._orig_stdout.write("\r\x1b[2K")
                    _ = self._orig_stdout.write("\x1b[1A\x1b[2K")
                    _ = self._orig_stdout.flush()
                except Exception:
                    pass
            self.prompting = False
