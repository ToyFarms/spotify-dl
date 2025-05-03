import io
import logging
import socket
import struct

from typing import Literal, Protocol, cast
from collections.abc import Buffer


class BufferSized(Buffer, Protocol):
    def __len__(self) -> int: ...


SizeLiteral = Literal["i8", "u8", "i16", "u16", "i32", "u32"]


class SocketConnection:
    logger: logging.Logger = logging.getLogger("spdl:socket")

    def __init__(self, addr: str, port: int) -> None:
        self.sock: socket.socket = socket.socket()
        self.sock.connect((addr, port))
        self.buf: io.BytesIO = io.BytesIO()

    def flush(self) -> None:
        _ = self.buf.seek(0)
        buf = self.buf.read()
        self.logger.debug(f"SEND [{len(buf):<5}]: {buf}")
        _ = self.sock.send(buf)

        self.clear_buf()

    def set_timeout(self, timeout: int) -> None:
        if timeout == 0:
            self.sock.settimeout(None)
        else:
            self.sock.settimeout(timeout)

    def read(self, length: int) -> bytes:
        buf = self.sock.recv(length)

        self.logger.debug(f"RECV [{len(buf):>5} of {length:<5} requested]: {buf}")

        return buf

    def write(self, data: BufferSized) -> None:
        self.logger.debug(
            f"BUFWRITE [{self.bufsize() + len(data):>5}/{len(data):<5}]: {data}"
        )
        _ = self.buf.write(bytes(data))

    def _size_lit_to_struct(self, size: SizeLiteral) -> tuple[str, int]:
        return {
            "i8": (">b", 1),
            "u8": (">B", 1),
            "i16": (">h", 2),
            "u16": (">H", 2),
            "i32": (">i", 4),
            "u32": (">I", 4),
        }[size]

    def read_sized(self, size: SizeLiteral) -> int:
        fmt, byte = self._size_lit_to_struct(size)
        return cast(int, struct.unpack(fmt, self.read(byte))[0])

    def write_sized(self, n: int, size: SizeLiteral) -> None:
        fmt, _ = self._size_lit_to_struct(size)

        self.write(struct.pack(fmt, n))

    def copy_buf(self) -> bytes:
        self.logger.debug(f"COPY BUFFER WITH SIZE {self.bufsize()}")

        pos = self.buf.tell()

        _ = self.buf.seek(0)
        buf = self.buf.read()
        _ = self.buf.seek(pos)

        return buf

    def clear_buf(self) -> None:
        self.logger.debug(f"BUFCLEAR ({self.bufsize()})")

        _ = self.buf.seek(0)
        _ = self.buf.truncate(0)

    def bufsize(self) -> int:
        pos = self.buf.tell()

        _ = self.buf.seek(0, io.SEEK_END)
        size = self.buf.tell()
        _ = self.buf.seek(pos)

        return size
