# pyright: reportAny=false, reportUnknownMemberType=false, reportExplicitAny=false

import binascii
import logging
import os
import platform
import shlex
import shutil
import subprocess
import threading
import time

from pathlib import Path
from dataclasses import dataclass
from queue import Queue
import traceback
from typing import Any, Callable
import uuid
from requests import HTTPError

from spotify_dl.api.internal.widevine import WidevineClient
from spotify_dl.api.web.storage_resolve import storage_resolve
from spotify_dl.key_provider import KeyProvider
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.metadata import apply_metadata
from spotify_dl.stream import (
    DecryptedSpotifyStream,
    EncryptedSpotifyStream,
)
from spotify_dl.track import ReplayGain, Track
from spotify_dl.format import AudioCodec, AudioFormat


class SpotifyDownloader:
    logger: logging.Logger = logging.getLogger("spdl:downloader")
    OGG_HEADER_SKIP: int = 167
    _KEY_CACHE: dict[str, bytes] = {}

    def __init__(
        self,
        track: Track,
        auth: SpotifyAuthPKCE,
        key_provider: KeyProvider | None,
    ) -> None:
        self.track: Track = track

        if not track.format:
            raise ValueError("Track format is not set")
        self.format: AudioFormat = track.format
        self.auth: SpotifyAuthPKCE = auth
        self.key_provider: KeyProvider | None = key_provider

        cdn_urls, fileid = self._resolve(track.format.file_id)

        self.key: bytes | None = SpotifyDownloader._KEY_CACHE.get(track.format.gid)
        if self.key_provider:
            if self.key is None:
                self.key = self.key_provider.get_audio_key(
                    binascii.unhexlify(track.format.gid),
                    (
                        binascii.unhexlify(track.format.file_id)
                        if not isinstance(self.key_provider, WidevineClient)
                        else fileid.encode()
                    ),
                )
                self.logger.info(f"key: {self.key!r}")
                if self.key:
                    SpotifyDownloader._KEY_CACHE[track.format.gid] = self.key

        self.stream: DecryptedSpotifyStream | EncryptedSpotifyStream
        for cdn in cdn_urls:
            try:
                # TODO: decrypt ourself
                if self.key and not isinstance(self.key_provider, WidevineClient):
                    self.stream = DecryptedSpotifyStream(
                        cdn, self.key, max_cached_chunks=-1
                    )
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
    key_provider: KeyProvider | None
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
        self._active: Queue[tuple[str, SpotifyDownloadState]] = Queue()
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

                self.logger.info(
                    f"Now downloading: {param.track.get_metadata()['name']}",
                )
                dl.download(
                    param.output,
                    param.emulate_playback,
                    state.buffer,
                )
                self.logger.info(f"Download finished, saved in: {param.output!r}")

                # TODO: just pass the key source

                add_metadata = isinstance(dl.stream, DecryptedSpotifyStream)

                if isinstance(dl.stream, EncryptedSpotifyStream) and dl.key:
                    self.logger.info("File is encrypted, decrypting...")
                    # dl.key is [KID:KEY, ...] separated with space
                    k = dl.key.decode().split(" ")
                    keys = [
                        val
                        for pair in zip(("--key" for _ in range(len(k))), k)
                        for val in pair
                    ]
                    enc_file = Path(param.output)
                    dec_file = Path(param.output).with_stem(enc_file.stem + "_dec")

                    suffix = ""
                    if platform.system() == "Windows":
                        suffix = ".exe"

                    mp4dec: Path | None = None
                    if p := shutil.which("mp4decrypt"):
                        mp4dec = Path(p).with_suffix(suffix)
                    else:
                        mp4dec = (
                            Path(__file__).parent.parent
                            / f"binaries/mp4decrypt{suffix}"
                        )

                    if mp4dec.exists() and mp4dec.is_file():
                        print(
                            f"Running mp4decrypt {mp4dec!r} with args {keys} {enc_file} {dec_file}"
                        )

                        tmp_input = enc_file.with_name(f"tmp_{uuid.uuid4().hex}.mp4")
                        tmp_output = enc_file.with_name(
                            f"tmp_{uuid.uuid4().hex}_out.mp4"
                        )

                        try:
                            # workaround for unicode issues with windows
                            os.replace(enc_file, tmp_input)

                            _ = subprocess.run(
                                [mp4dec, *keys, tmp_input, tmp_output], check=True
                            )

                            os.replace(tmp_input, enc_file)
                            os.replace(tmp_output, enc_file)

                            add_metadata = True
                        except Exception as e:
                            self.logger.error(f"mp4decrypt failed: {e}")
                            if tmp_input.exists():
                                os.replace(tmp_input, enc_file)

                            if tmp_output.exists():
                                tmp_output.unlink()

                            raise

                    else:
                        self.logger.warning(
                            "mp4decrypt is required for widevine stream. download it from 'https://www.bento4.com/downloads' or build it with 'python script.py build-bento4'"
                        )
                        self.logger.info(
                            "call the following command to decrypt the already downloaded file:"
                        )
                        self.logger.info(
                            f"\tmp4decrypt {' '.join(keys)} {shlex.quote(str(enc_file))} {shlex.quote(str(dec_file))}"
                        )

                if add_metadata:
                    self.logger.info("Adding metadata")
                    rg: ReplayGain | None = None
                    if (
                        param.track.format
                        and param.track.format.get_codec() == AudioCodec.OGG_VORBIS
                        and isinstance(dl.stream, DecryptedSpotifyStream)
                    ):
                        header = dl.stream.read_header()
                        rg = header.replaygain
                    else:
                        self.logger.debug("Track does not have replaygain info")

                    apply_metadata(
                        param.track,
                        str(param.output),
                        param.auth,
                        replaygain=rg,
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
