# pyright: reportAny=false, reportUnknownMemberType=false, reportExplicitAny=false

import binascii
import logging
import threading
import time

from pathlib import Path
from dataclasses import dataclass
from queue import PriorityQueue, Queue
import traceback
from typing import Any, Callable
from requests import HTTPError

from spotify_dl.api.internal.widevine import WidevineClient
from spotify_dl.api.web.storage_resolve import storage_resolve
from spotify_dl.key_provider import KeyProvider
from spotify_dl.api.internal.spotify_client import SpotifyClient
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.metadata import apply_metadata
from spotify_dl.stream import (
    ChunkedStream,
    DecryptedSpotifyStream,
    EncryptedSpotifyStream,
)
from spotify_dl.track import Track
from spotify_dl.format import AudioCodec, AudioFormat


class SpotifyDownloader:
    logger: logging.Logger = logging.getLogger("spdl:downloader")
    OGG_HEADER_SKIP: int = 167
    _KEY_CACHE: dict[str, bytes] = {}

    def __init__(
        self,
        track: Track,
        auth: SpotifyAuthPKCE,
        key_provider: KeyProvider,
    ) -> None:
        self.track: Track = track

        if not track.format:
            raise ValueError("Track format is not set")
        self.format: AudioFormat = track.format
        self.auth: SpotifyAuthPKCE = auth
        self.key_provider: KeyProvider = key_provider

        cdn_urls, fileid = self._resolve(track.format.file_id)

        key = SpotifyDownloader._KEY_CACHE.get(track.format.gid)
        if key is None:
            key = self.key_provider.get_audio_key(
                binascii.unhexlify(track.format.gid),
                (
                    binascii.unhexlify(track.format.file_id)
                    if not isinstance(self.key_provider, WidevineClient)
                    else fileid.encode()
                ),
            )
            self.logger.info(f"key: {key}")
            if key:
                SpotifyDownloader._KEY_CACHE[track.format.gid] = key

        self.stream: DecryptedSpotifyStream | EncryptedSpotifyStream
        for cdn in cdn_urls:
            try:
                if key:
                    self.stream = DecryptedSpotifyStream(cdn, key, max_cached_chunks=-1)
                else:
                    self.stream = EncryptedSpotifyStream(cdn, max_cached_chunks=-1)
                break
            except HTTPError:
                self.logger.debug(f"Could not connect to {cdn}, trying next")

        if not self.stream:
            raise HTTPError(f"Tried all ({len(cdn_urls)}) cdn's, none of them worked")

        self.duration_ms: float | None = self.track.get_metadata_internal(
            self.auth
        ).duration
        self.finished_event: threading.Event = threading.Event()

    def _resolve(self, file_id: str) -> tuple[list[str], str]:
        res = storage_resolve(self.auth.session, file_id)
        cdn_urls: list[str] = res.get("cdnurl", [])
        self.logger.debug(f"cdn for {file_id}: {cdn_urls}")

        if not cdn_urls:
            raise ValueError(f"No cdn url for {file_id}")

        return cdn_urls, res["fileid"]

    def get_percentage(self) -> float:
        """returns downloaded / size"""
        return self.stream.pos / self.stream.size if self.stream.size != 0 else 0

    def download(
        self,
        output: str,
        emulate_playback: bool = False,
        player_buffer: Queue[bytes] | None = None,
    ) -> None:
        path = Path(output)

        bps = (
            (self.stream.size / (self.duration_ms / 1000.0))
            if self.duration_ms
            else None
        )
        if bps is None:
            self.logger.error("Could not determine bps because duration_ms is None")
            return

        buffer: Queue[bytes] = Queue()
        buffer_bytes = 3 * bps

        f = None
        try:
            # TODO: determine if output points to file/directory (based on the filename alone)
            path.absolute().parent.mkdir(parents=True, exist_ok=True)

            if self.format.get_codec() == AudioCodec.OGG_VORBIS:
                _ = self.stream.seek(self.OGG_HEADER_SKIP)

            f = open(path, "wb")
            while True:
                # TODO: better way of buffering
                while buffer.qsize() * bps < buffer_bytes or (
                    player_buffer and player_buffer.qsize() * bps < buffer_bytes
                ):
                    data = self.stream.read(self.stream.CHUNK_SIZE)
                    if not data:
                        if player_buffer:
                            player_buffer.put(b"")
                        buffer.put(b"")
                        break

                    if player_buffer:
                        player_buffer.put(data)
                    buffer.put(data)

                data = buffer.get()
                if not data:
                    break

                _ = f.write(data)

                if emulate_playback:
                    time.sleep(len(data) / bps)
        finally:
            if f:
                f.close()
            self.stream.close()
            self.finished_event.set()


@dataclass
class SpotifyDownloadParam:
    track: Track
    auth: SpotifyAuthPKCE
    key_provider: KeyProvider
    output: str
    emulate_playback: bool


@dataclass
class SpotifyDownloadState:
    download: SpotifyDownloader
    param: SpotifyDownloadParam
    buffer: Queue[bytes] | None


class SpotifyDownloadManager:
    logger: logging.Logger = logging.getLogger("spdl:download_manager")

    def __init__(
        self,
        concurrent_download: int = 1,
        download_cb: Callable[[SpotifyDownloadState], Any] | None = None,
    ) -> None:
        self.queue: Queue[SpotifyDownloadParam] = Queue()
        self.threads: list[threading.Thread] = []
        self._active: PriorityQueue[tuple[str, SpotifyDownloadState]] = PriorityQueue()
        self._cond: threading.Condition = threading.Condition()
        self.download_cb: Callable[[SpotifyDownloadState], Queue[bytes]] | None = (
            download_cb
        )

        for i in range(concurrent_download):
            tid = threading.Thread(
                target=self._consumer_thread,
                name=f"download_worker:{i}",
                daemon=True,
            )
            tid.start()
            self.threads.append(tid)

    def enqueue(self, param: SpotifyDownloadParam) -> None:
        self.queue.put(param)

    def _consumer_thread(self) -> None:
        while True:
            param = self.queue.get()
            thread_name = threading.current_thread().name

            try:
                dl = SpotifyDownloader(param.track, param.auth, param.key_provider)

                state = SpotifyDownloadState(dl, param, None)
                state.buffer = (
                    self.download_cb(state)
                    if self.download_cb
                    and isinstance(dl.stream, DecryptedSpotifyStream)
                    else None
                )

                with self._cond:
                    self._active.put((thread_name, state))
                    self._cond.notify_all()

                header = dl.stream.read_header()
                self.logger.info(
                    f"Now downloading: {param.track.get_metadata(param.auth)['name']}",
                )
                dl.download(
                    param.output,
                    param.emulate_playback,
                    state.buffer,
                )
                self.logger.info(f"Download finished, saved in: {param.output!r}")

                apply_metadata(
                    param.track,
                    str(param.output),
                    param.auth,
                    replaygain=header.replaygain,
                )

                self.logger.info(
                    f"Finished adding metadata, saved in: {param.output!r}"
                )
            except Exception as e:
                traceback.print_exc()
                self.logger.error(f"Error while downloading: {e}")
            finally:
                self.queue.task_done()

    def get_active(self) -> list[tuple[SpotifyDownloader, SpotifyDownloadParam]]:
        with self._cond:
            return [(s.download, s.param) for _, s in self._active.queue]

    def get_queued(self) -> list[SpotifyDownloadParam]:
        return list(self.queue.queue)
