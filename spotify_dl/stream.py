# pyright: reportAny=false, reportUnknownMemberType=false
import io
import math
import struct

from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
from typing import Protocol, Self, override
from collections import OrderedDict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from spotify_dl.track import ReplayGain, TrackHeader

# TODO: better separation on provider and reader
# TODO: this is a mess


class BytesStreamProtocol(Protocol):
    size: int

    def read(self, size: int = -1) -> bytes: ...
    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int: ...
    def tell(self) -> int: ...
    def close(self) -> None: ...


class ChunkedBytesStreamProtocol(Protocol):
    size: int
    CHUNK_SIZE: int

    def read(self, size: int = -1) -> bytes: ...
    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int: ...
    def tell(self) -> int: ...
    def close(self) -> None: ...
    def request_chunk(self, chunk_index: int) -> bytes: ...


class ChunkedStream(ChunkedBytesStreamProtocol):
    CHUNK_SIZE: int = 128 * 1024

    def __init__(self, url: str, max_cached_chunks: int = 16):
        self.url: str = url
        self.session: requests.Session = requests.Session()
        retry_strategy = Retry(
            total=5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1,
            raise_on_status=False,
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        res = self.session.get(url, headers={"Range": f"bytes=0-1024"})
        res.raise_for_status()

        self.size: int = int(res.headers["Content-Range"].split("/")[-1])
        self.total_chunks: int = math.ceil(self.size / self.CHUNK_SIZE)

        self._cache: OrderedDict[int, bytes] = OrderedDict()
        self.max_cached_chunks: int = max_cached_chunks

        self.pos: int = 0
        self.closed: bool = False

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        self.close()

    @override
    def request_chunk(self, chunk_index: int) -> bytes:
        if not (0 <= chunk_index < self.total_chunks):
            raise IndexError(f"Chunk index {chunk_index} out of range")

        if chunk_index in self._cache:
            self._cache.move_to_end(chunk_index)
            return self._cache[chunk_index]

        start = chunk_index * self.CHUNK_SIZE
        end = min(start + self.CHUNK_SIZE, self.size) - 1
        resp = self.session.get(self.url, headers={"Range": f"bytes={start}-{end}"})
        resp.raise_for_status()
        data = resp.content

        self._cache[chunk_index] = data
        if self.max_cached_chunks > 0 and len(self._cache) > self.max_cached_chunks:
            _ = self._cache.popitem(last=False)

        return data

    @override
    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            new_pos = offset
        elif whence == io.SEEK_CUR:
            new_pos = self.pos + offset
        elif whence == io.SEEK_END:
            new_pos = self.size + offset
        else:
            raise ValueError(f"Invalid whence: {whence}")

        if not (0 <= new_pos <= self.size):
            raise ValueError(f"Seek out of bounds: {new_pos}")
        self.pos = new_pos
        return self.pos

    @override
    def tell(self) -> int:
        return self.pos

    @override
    def read(self, size: int = -1) -> bytes:
        if self.closed:
            raise IOError("I/O operation on closed file.")

        if size < 0:
            size = self.size - self.pos

        if self.pos >= self.size or size == 0:
            return b""

        to_read = min(size, self.size - self.pos)
        start_chunk = self.pos // self.CHUNK_SIZE
        end_chunk = (self.pos + to_read - 1) // self.CHUNK_SIZE

        parts = bytearray()
        remaining = to_read
        offset = self.pos

        for chunk_index in range(start_chunk, end_chunk + 1):
            chunk_data = self.request_chunk(chunk_index)

            chunk_start = max(0, offset - chunk_index * self.CHUNK_SIZE)
            chunk_end = min(len(chunk_data), chunk_start + remaining)
            parts.extend(chunk_data[chunk_start:chunk_end])

            read_len = chunk_end - chunk_start
            remaining -= read_len
            offset += read_len

        self.pos += to_read
        return bytes(parts)

    @override
    def close(self) -> None:
        if not self.closed:
            self.session.close()
            self._cache.clear()
            self.closed = True


class EncryptedStream(ChunkedStream):
    def __init__(
        self,
        url: str,
        key: bytes,
        iv: int,
        max_cached_chunks: int = 16,
    ) -> None:
        super().__init__(url, max_cached_chunks)

        self.key: bytes = key
        self.decrypted_chunk_buffer: OrderedDict[int, bytes] = OrderedDict()
        self.iv: int = iv

    def decrypt_chunk(self, chunk: int, encrypted: bytes) -> bytes:
        if not self.key:
            return encrypted

        blocks_before = (chunk * self.CHUNK_SIZE) // AES.block_size
        ctr = Counter.new(128, initial_value=self.iv + blocks_before)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(encrypted)

    @override
    def request_chunk(self, chunk_index: int) -> bytes:
        encrypted = super().request_chunk(chunk_index)
        if chunk_index in self.decrypted_chunk_buffer:
            return self.decrypted_chunk_buffer[chunk_index]

        plaintext = self.decrypt_chunk(chunk_index, encrypted)
        self.decrypted_chunk_buffer[chunk_index] = plaintext

        return plaintext


class DecryptedSpotifyStream(EncryptedStream):
    AUDIO_IV: int = 152697175058892756956149811227012566419

    def __init__(self, url: str, key: bytes, max_cached_chunks: int = 16) -> None:
        super().__init__(url, key, self.AUDIO_IV, max_cached_chunks=max_cached_chunks)

    def _read_rg(self) -> ReplayGain:
        pos = self.pos
        _ = self.seek(144)
        rg = ReplayGain(
            track_gain_db=struct.unpack("<f", self.read(4))[0],
            track_peak=struct.unpack("<f", self.read(4))[0],
            album_gain_db=struct.unpack("<f", self.read(4))[0],
            album_peak=struct.unpack("<f", self.read(4))[0],
        )

        _ = self.seek(pos)
        return rg

    def read_header(self) -> TrackHeader:
        return TrackHeader(
            replaygain=self._read_rg(),
        )


class EncryptedSpotifyStream(ChunkedStream):
    def __init__(self, url: str, max_cached_chunks: int = 16) -> None:
        super().__init__(url, max_cached_chunks=max_cached_chunks)


class ChunkedStreamReader:
    def __init__(self, source: ChunkedBytesStreamProtocol, offset: int = 0) -> None:
        if not (0 <= offset <= source.size):
            raise ValueError(f"Invalid offset: {offset}")
        self.source: ChunkedBytesStreamProtocol = source
        self.offset: int = offset
        self.pos: int = 0
        self.closed: bool = False

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            new_pos = offset
        elif whence == io.SEEK_CUR:
            new_pos = self.pos + offset
        elif whence == io.SEEK_END:
            new_pos = self.source.size - self.offset + offset
        else:
            raise ValueError(f"Invalid whence: {whence}")

        if not (0 <= new_pos <= self.source.size - self.offset):
            raise ValueError(f"Seek out of bounds: {new_pos}")
        self.pos = new_pos
        return self.pos

    def tell(self) -> int:
        return self.pos

    def read(self, size: int = -1) -> bytes:
        if self.closed:
            raise IOError("I/O operation on closed reader")

        logical_end = self.source.size - self.offset
        if size < 0 or self.pos + size > logical_end:
            size = logical_end - self.pos

        if self.pos >= logical_end or size == 0:
            return b""

        to_read = size
        start_byte = self.offset + self.pos
        end_byte = start_byte + to_read

        start_chunk = start_byte // self.source.CHUNK_SIZE
        end_chunk = (end_byte - 1) // self.source.CHUNK_SIZE

        parts = bytearray()
        remaining = to_read
        offset = start_byte

        for chunk_index in range(start_chunk, end_chunk + 1):
            chunk_data = self.source.request_chunk(chunk_index)

            chunk_start = max(0, offset - chunk_index * self.source.CHUNK_SIZE)
            chunk_end = min(len(chunk_data), chunk_start + remaining)
            parts.extend(chunk_data[chunk_start:chunk_end])

            read_len = chunk_end - chunk_start
            remaining -= read_len
            offset += read_len

        self.pos += to_read
        return bytes(parts)

    def close(self) -> None:
        self.closed = True
