# pyright: reportPrivateImportUsage=false, reportPossiblyUnboundVariable=false
import atexit
import logging
import os
import sys
import tempfile

from pathlib import Path
from typing import IO, Literal, Protocol, cast, override

if sys.platform == "win32":
    import _win32typing  # pyright: ignore[reportMissingModuleSource]
    import win32file  # pyright: ignore[reportMissingModuleSource]
    import win32pipe  # pyright: ignore[reportMissingModuleSource]
    import pywintypes  # pyright: ignore[reportMissingModuleSource]


class SupportsStr(Protocol):
    @override
    def __str__(self) -> str: ...


class Fifo:
    logger: logging.Logger = logging.getLogger("spdl:fifo")
    _TO_BE_DELETED: set[str] = set()
    atexit_registered: bool = False

    def __init__(
        self,
        name: SupportsStr | None = None,
        mode: Literal["r", "w"] = "r",
        bufsize: int = 4096,
    ) -> None:
        if mode not in ("r", "w"):
            raise ValueError(
                f"mode must be 'r' or 'w', not {mode!r}"
            )  # pyright: ignore[reportUnreachable]

        self.mode: str = mode
        self.bufsize: int = bufsize

        self._base: str
        self.path: str
        self.name: str = str(name) if name is not None else f"fifo_{id(self)}"
        if sys.platform == "win32":
            self._base = r"\\.\pipe"
            self.path = f"{self._base}\\{self.name}"
        else:
            self._base = tempfile.gettempdir()
            self.path = f"{self._base}/{self.name}"

        self._fd: IO[bytes] | None = None
        self._handle: int | _win32typing.PyHANDLE | None = None

        if not Fifo.atexit_registered and sys.platform == "linux":

            def delete_files():
                for file in Fifo._TO_BE_DELETED:
                    if not os.path.exists(file):
                        continue

                    os.unlink(file)

            _ = atexit.register(lambda: delete_files())
            Fifo.atexit_registered = True

    def open(self, nonblocking: bool = False) -> IO[bytes]:
        if sys.platform == "win32":
            fd = self._open_windows()
        else:
            fd = self._open_posix(nonblocking=nonblocking)
        Fifo._TO_BE_DELETED.add(self.path)
        return fd

    def close(self) -> None:
        if self._fd:
            try:
                self._fd.close()
            except Exception:
                pass
            self._fd = None

        if sys.platform == "win32":
            if self._handle is not None:
                try:
                    if isinstance(self._handle, int):
                        win32file.CloseHandle(self._handle)
                    else:
                        self._handle.Close()
                except Exception:
                    pass
                self._handle = None
        else:
            try:
                self.logger.debug(
                    f"Removing FIFO: {self.path!r}, {len(Fifo._TO_BE_DELETED) - 1} left"
                )
                os.unlink(self.path)
            except FileNotFoundError as e:
                self.logger.warning(f"Cannot remove FIFO file: {e}")

        try:
            Fifo._TO_BE_DELETED.remove(self.path)
        except KeyError:
            if os.path.exists(self.path):
                self.logger.error(
                    "File does not exists in to be deleted list, but still exists on disk"
                )

    def _open_posix(self, nonblocking: bool) -> IO[bytes]:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

        try:
            os.mkfifo(self.path)
        except FileExistsError:
            pass

        flags = os.O_RDONLY if self.mode == "r" else os.O_WRONLY
        if nonblocking:
            flags |= os.O_NONBLOCK

        fd = os.open(self.path, flags)
        self._fd = os.fdopen(
            fd,
            "rb" if self.mode == "r" else "wb",
            buffering=self.bufsize,
        )

        return self._fd

    def _open_windows(self) -> IO[bytes]:
        if self.mode == "r":
            self._handle = win32pipe.CreateNamedPipe(
                self.path,
                win32pipe.PIPE_ACCESS_INBOUND,
                win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT,
                1,  # max instances
                self.bufsize,  # out buffer
                self.bufsize,  # in buffer
                0,  # default timeout
                None,  # default security
            )
            win32pipe.ConnectNamedPipe(self._handle, None)
            raw_fd = cast(int, cast(pywintypes.HANDLE, self._handle).Detach())
            self._fd = os.fdopen(raw_fd, "rb", buffering=self.bufsize)
        else:
            handle = win32file.CreateFile(
                self.path,
                win32file.GENERIC_WRITE,
                0,  # no sharing
                None,  # default security
                win32file.OPEN_EXISTING,
                0,
                None,
            )

            raw_fd = handle.Detach()
            self._fd = os.fdopen(raw_fd, "wb", buffering=self.bufsize)
            self._handle = handle

        return self._fd
