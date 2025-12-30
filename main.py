# pyright: reportAny=false, reportExplicitAny=false, reportUnknownVariableType=false

# TODO: persistent state management
# TODO: persistent download (allow for resuming interrupted download)

"""
OGG_VORBIS_96 = 0; // playplay
OGG_VORBIS_160 = 1; // playplay
OGG_VORBIS_320 = 2; // playplay
AAC_24 = 8; // playplay
MP4_128 = 10; // widevine
MP4_256 = 11; // widevine
MP4_128_DUAL = 12; // playready / widevine
MP4_256_DUAL = 13; // playready / widevine
MP4_128_CBCS = 14; // fairplay
MP4_256_CBCS = 15; // fairplay
FLAC_FLAC = 16; // playplay
MP4_FLAC = 17; // widevine
FLAC_FLAC_24BIT = 22; // playplay
"""

import atexit
from enum import StrEnum
import glob
import json
import os
import readline
import argparse
import shlex
import logging
import subprocess
import curl_cffi
import yt_dlp
from faker import Faker

from spotify_dl.auth.clienttoken import ClientToken
from spotify_dl.auth.login5 import Login5Auth
from spotify_dl.auth.spdc import SpDCAuth
from spotify_dl.state import state

fake = Faker()

import requests

requests.utils.default_user_agent = lambda: fake.user_agent()

from typing import Any, Callable, Literal, TypedDict, cast, overload, override
from pathlib import Path
from collections.abc import Iterable

from yt_dlp.utils import DownloadError

from spotify_dl.api.internal.playplay import PlayPlay
from spotify_dl.api.internal.spotify_client import SpotifyClient
from spotify_dl.api.internal.widevine import WidevineClient
from spotify_dl.auth.internal_auth import SpotifyInternalAuth
from spotify_dl.auth.web_auth import SpotifyAuthPKCE

# TODO: cli is unreliable
# from spotify_dl.cli import CLI
from spotify_dl.downloader import (
    SpotifyDownloadParam,
)
from spotify_dl.format import AudioCodec, AudioFormat, AudioQuality
from spotify_dl.metadata import apply_metadata
from spotify_dl.track import Track

from spotify_dl.utils.terminal import print_table
from spotify_dl.utils.ytdl import choose_best_audio_format


# TODO: create a general key provider class so its not handled here
class KeySource(StrEnum):
    CLIENT = "Client"
    PLAYPLAY = "PlayPlay"
    WIDEVINE = "Widevine"
    NONE = "None"


def get_username(auth: SpotifyAuthPKCE) -> str:
    if auth.require_login():
        return "Logged Out"

    res = curl_cffi.post(
        "https://api-partner.spotify.com/pathfinder/v2/query",
        json={
            "variables": {},
            "operationName": "profileAttributes",
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "53bcb064f6cd18c23f752bc324a791194d20df612d8e1239c735144ab0399ced",
                }
            },
        },
        headers={
            "authorization": f"Bearer {state.auth.token}",
            "client-token": state.ensure_clienttoken().token,
        },
        impersonate="chrome",
    )
    res.raise_for_status()

    if res.status_code != 200:
        try:
            print(
                f"Failed to get username ({res.status_code}): {res.json()['error']['message']}"  # pyright: ignore[reportUnknownMemberType]
            )
        finally:
            return "?"

    return cast(dict[str, str], res.json()).get("data", {}).get("me", {}).get("profile", {}).get("name", "?")  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]


@overload
def prompt[T](
    prompt: str,
    items: Iterable[T],
    default: T | None = None,
    repr_fun: Callable[[T, int | None], str] = ...,
    greedy: Literal[False] = False,
) -> T | None: ...


@overload
def prompt[T](
    prompt: str,
    items: Iterable[T],
    default: T | None = None,
    repr_fun: Callable[[T, int | None], str] = ...,
    greedy: Literal[True] = True,
) -> T | str | None: ...


def prompt[T](
    prompt: str,
    items: Iterable[T],
    default: T | None = None,
    repr_fun: Callable[[T, int | None], str] = lambda x, _: str(x),
    greedy: bool = False,
) -> object:
    items = list(items)

    for i, item in enumerate(items, 1):
        print(f"{i:>3} : {repr_fun(item, i - 1)}")

    try:
        while True:
            ans = input(
                f"{prompt}{f' (default={repr_fun(default, None)})' if default else ''}: "
            )

            if ans == "":
                return default

            if not ans.isnumeric():
                if greedy:
                    return cast(T, ans)

                print(f"Invalid index")
                continue

            idx = int(ans)
            if idx > len(items) or idx < 1:
                print(f"Out of bound (1 - {len(items)})")
                continue

            return items[idx - 1]
    except Exception as e:
        print(e)
        return None


class CommandParser(argparse.ArgumentParser):
    args_list: list[str] = []

    def with_args(self, args: list[str]) -> "CommandParser":
        self.args_list = args

        return self

    def parse(self) -> argparse.Namespace:
        return self.parse_args(self.args_list)

    @override
    def add_argument(  #  pyright: ignore[reportIncompatibleMethodOverride]
        self,
        *args: Any,
        **kwargs: Any,
    ) -> "CommandParser":
        _ = super().add_argument(*args, **kwargs)
        return self


HISTORY_FILE = Path(".spotifydl_history")


OPTIONS = [
    "login",
    "connect",
    "con",
    "info",
    "info2",
    "dl",
    "as raw",
    "exit",
    "quit",
    "yt-download",
    "ytdl",
    "download",
    "dl",
    "metadata",
    "req",
    "verbose",
    "out",
    "volume",
]


def completer(text: str, state: int) -> str | None:
    matches = [o for o in OPTIONS if o.startswith(text)]
    try:
        return matches[state]
    except IndexError:
        return None


def main() -> None:
    _ = atexit.register(lambda: readline.write_history_file(HISTORY_FILE))
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    if HISTORY_FILE.exists() and HISTORY_FILE.is_file():
        readline.read_history_file(HISTORY_FILE)

    parser = argparse.ArgumentParser()
    _ = parser.add_argument("-c", "--command", default=None, help="Command")
    _ = parser.add_argument(
        "-v", "--verbose", action="store_true", help="Logging set to DEBUG"
    )

    program_args = parser.parse_args()

    if program_args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    state.iauth = SpotifyInternalAuth()

    state.name = get_username(state.auth)
    # cli = CLI(state.download_manager)

    while state.running:
        print()

        # cli.prompting = True
        if program_args.command:
            commands: list[str] = shlex.split(program_args.command)
            state.running = False
        else:
            try:
                commands = shlex.split(input(f"{state.name} > "))
            except (EOFError, KeyboardInterrupt):
                print()
                break
            # finally:
            #     cli.prompting = False

        match commands:
            case ["login", *_]:
                if not state.auth.is_token_valid():
                    print("Waiting for user to authenticate...")
                    state.auth.authenticate()

                    state.name = get_username(state.auth)
                    print(f"Authentication successful! Logged in as {state.name}")
            case ["connect" | "con", *_]:
                if state.auth.require_login():
                    print("Not logged in")
                    continue

                print("Connecting to Spotify...")
                state.client = SpotifyClient.random_ap(state.auth)
                state.client.authenticate()
                print(
                    f"Successfully connected to {state.client.addr}:{state.client.port}"
                )
            case ["info", uri]:
                if state.auth.require_login():
                    print("Not logged in")
                    continue

                try:
                    track = Track.probe(uri)
                    meta = track.get_metadata()
                    print_table(meta)
                    state.last_json_output = meta
                except Exception as e:
                    print(e)
            case ["info2", uri]:
                if state.auth.require_login():
                    print("Not logged in")
                    continue

                try:
                    track = Track.probe(uri)
                    meta = track.get_metadata_internal(state.auth)
                    print_table(meta)
                    state.last_json_output = repr(meta)
                except Exception as e:
                    print(e)
            case ["as", "raw", *_]:
                print(json.dumps(state.last_json_output, ensure_ascii=False, indent=4))
            case ["exit" | "quit", *_]:
                state.running = False
            case ["yt-download" | "ytdl", uri]:
                if state.auth.require_login():
                    print("Not logged in")
                    continue

                track = Track.probe(uri)
                meta = track.get_metadata_internal(state.auth)
                print(
                    f"Downloading {meta.name!r} from the album {meta.album.name!r} (duration={meta.duration}) featuring {len(meta.artist)} artists: ",
                    end="",
                )
                for i, artist in enumerate(meta.artist):
                    if i != 0:
                        print(", ", end="")
                    print(f"{artist.name}", end="")
                print()

                ydl_opts = {
                    "noplaylist": True,
                    "quiet": True,
                    "skip_download": True,
                    "postprocessors": [],
                    "postprocessor_args": {},
                    "addmetadata": False,
                    "embed_metadata": False,
                    "embedthumbnail": False,
                    "writethumbnail": False,
                    "writeinfojson": False,
                    "xattrs": False,
                    "no_warnings": True,
                }

                class Entry(TypedDict):
                    artist: str
                    title: str
                    duration: int
                    views: int
                    url: str
                    formats: list[dict[str, object]]

                def search(n: int) -> list[Entry]:
                    ret: list[Entry] = []
                    with yt_dlp.YoutubeDL(cast(Any, ydl_opts)) as ydl:
                        artists = " ".join(artist.name for artist in meta.artist)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType, reportAttributeAccessIssue]
                        info = ydl.extract_info(
                            f"ytsearch{n}:{artists} {meta.name}", download=False  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
                        )

                        for entry in cast(
                            list[dict[str, object]], info.get("entries", [])
                        ):
                            artist = (
                                entry.get("artist")
                                or entry.get("uploader")
                                or entry.get("uploader_id")
                                or "Unknown Artist"
                            )
                            title = entry.get("title", "Unknown Title")
                            duration = entry.get("duration", 0)
                            views = entry.get("view_count", 0)
                            url = (
                                entry.get("webpage_url")
                                or entry.get("url")
                                or f"ytsearch:{title}"
                            )
                            formats = entry.get("formats", [])

                            ret.append(
                                {
                                    "artist": cast(str, artist),
                                    "title": cast(str, title),
                                    "duration": cast(int, duration),
                                    "views": cast(int, views),
                                    "url": cast(str, url),
                                    "formats": cast(list[dict[str, object]], formats),
                                }
                            )

                    return ret

                n = 15
                formatted = search(n)
                while True:
                    entry = prompt(
                        "Select the video",
                        formatted,
                        default=formatted[0],
                        greedy=True,
                        repr_fun=lambda x, _: f"{x['artist']} - {x['title']} (duration={x['duration']:_} views={x['views']:_})",
                    )

                    if isinstance(entry, str) and entry.startswith("!next"):
                        n *= 2
                        formatted = search(n)
                    else:
                        break

                if not entry:
                    continue

                fmt = choose_best_audio_format(entry["formats"])  # pyright: ignore[reportArgumentType]

                out_name = (
                    f"{', '.join(a.name for a in meta.artist)} - {meta.name}.%(ext)s"
                )
                path = Path(out_name)
                if state.dir:
                    path = state.dir.expanduser().absolute() / path
                outtmpl = str(path)

                def hook(d: dict[str, object]) -> None:
                    if d.get("status") == "finished":
                        downloaded = cast(
                            str | None,
                            (
                                d.get("filename")
                                or cast(dict[str, object], d.get("info_dict", {})).get(
                                    "_filename"
                                )
                                or cast(dict[str, object], d.get("info_dict", {})).get(
                                    "filepath"
                                )
                            ),
                        )
                        if not downloaded:
                            print(
                                "Warning: finished hook called but no filename was reported by yt-dlp."
                            )
                            return

                        downloaded_path = Path(downloaded)

                        if downloaded_path.suffix.lower() not in (".ogg", ".opus"):
                            out = downloaded_path.with_suffix(".ogg")
                            ffmpeg_cmd = [
                                "ffmpeg",
                                "-y",
                                "-i",
                                str(downloaded_path),
                                "-c:a",
                                "libvorbis",
                                "-q:a",
                                "6",
                                str(out),
                            ]
                            try:
                                _ = subprocess.run(
                                    ffmpeg_cmd,
                                    check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                )
                            except subprocess.CalledProcessError as e:
                                print(
                                    f"Failed to convert to oggvorbis: {e.stderr.decode(errors='ignore')}"
                                )
                                downloaded_path = downloaded_path
                            else:
                                try:
                                    os.remove(downloaded_path)
                                except OSError:
                                    pass
                                downloaded_path = out

                        track.set_format(
                            AudioFormat.from_codec(
                                AudioCodec.from_file(
                                    str(downloaded_path), extension_fallback=True
                                ),
                                AudioQuality.NORMAL,
                            )
                        )
                        apply_metadata(track, str(downloaded_path), state.auth)

                ydl_download_opts = {
                    "format": (fmt["format_id"] if fmt else "bestaudio"),
                    "outtmpl": outtmpl,
                    "noplaylist": True,
                    "quiet": False,
                    "progress_hooks": [hook],
                    "postprocessors": [],
                    "postprocessor_args": {},
                    "addmetadata": False,
                    "embed_metadata": False,
                    "embedthumbnail": False,
                    "writethumbnail": False,
                    "writeinfojson": False,
                    "xattrs": False,
                }

                try:
                    with yt_dlp.YoutubeDL(cast(Any, ydl_download_opts)) as ydl2:
                        ydl2.download([entry["url"]])  # pyright: ignore[reportArgumentType]
                except DownloadError as e:
                    print(
                        f"Requested format not available, falling back to 'bestaudio'. Error: {e}"
                    )
                    ydl_download_opts["format"] = "bestaudio"
                    with yt_dlp.YoutubeDL(cast(Any, ydl_download_opts)) as ydl2:
                        ydl2.download([entry["url"]])  # pyright: ignore[reportArgumentType]

            case ["download" | "dl", *rest]:
                if state.auth.require_login():
                    print("Not logged in")
                    continue

                print(
                    "Warning: if you dont have premium account, you can't decrypt the audio stream from spotify client method"
                )

                method = prompt(
                    "choose audio key retrieval method",
                    [
                        KeySource.CLIENT,
                        KeySource.PLAYPLAY,
                        KeySource.WIDEVINE,
                        KeySource.NONE,
                    ],
                    default=KeySource.WIDEVINE,
                    repr_fun=lambda x, _: x.value,
                )
                if method == KeySource.CLIENT:
                    print("Connecting to Spotify...")
                    state.client = SpotifyClient.random_ap(state.auth)
                    state.client.handshake()
                    state.client.authenticate()
                if method == KeySource.PLAYPLAY:
                    if not state.login5:
                        if not state.client:
                            state.client = SpotifyClient.random_ap(state.auth)

                        if not state.clienttoken:
                            state.clienttoken = ClientToken(state.client)

                        state.login5 = Login5Auth(state.client, state.clienttoken)

                    if not state.clienttoken:
                        if not state.client:
                            state.client = SpotifyClient.random_ap(state.auth)
                        state.clienttoken = ClientToken(state.client)

                    state.playplay = PlayPlay(state.login5, state.clienttoken)
                elif method == KeySource.WIDEVINE:
                    print("NOTE: Widevine only supports mp4 format")
                    print(
                        "supply an extracted Widevine license, take a look at https://forum.videohelp.com/threads/408031-Dumping-Your-own-L3-CDM-with-Android-Studio"
                    )
                    wvds = glob.glob("*.wvd", include_hidden=True)
                    wvd = prompt("private key path", wvds, wvds[0], greedy=True)
                    if not wvd:
                        print("No wvd file supplied")
                        continue

                    if not state.clienttoken:
                        if not state.client:
                            state.client = SpotifyClient.random_ap(state.auth)
                        state.clienttoken = ClientToken(state.client)

                    if not state.iauth.is_linked_with_account():
                        sp_dc = SpDCAuth()
                        _ = sp_dc.token  # trigger prompt
                        state.iauth = SpotifyInternalAuth(sp_dc)

                    state.widevine = WidevineClient(state.iauth, state.clienttoken, wvd)

                args = (
                    CommandParser()
                    .with_args(rest)
                    .add_argument("uri")
                    .add_argument("--sim-play", "-p", action="store_true")
                    .add_argument("--output-directory", "-o")
                    .parse()
                )
                if not args:
                    continue

                track = Track.probe(args.uri)
                meta = track.get_metadata_internal(state.auth)
                print(
                    f"Downloading {meta.name!r} from the album {meta.album.name!r} featuring {len(meta.artist)} artists: ",
                    end="",
                )
                for i, artist in enumerate(meta.artist):
                    if i != 0:
                        print(", ", end="")
                    print(f"{artist.name}", end="")
                print()

                default_format_type = None
                if method == KeySource.WIDEVINE:
                    default_format_type = AudioFormat.Type.MP4_128
                elif method in (
                    KeySource.PLAYPLAY,
                    KeySource.CLIENT,
                ):
                    default_format_type = AudioFormat.Type.OGG_VORBIS_160

                default_format = None
                for format in track.get_formats(state.auth):
                    if format.type == default_format_type:
                        default_format = format
                        break

                format = prompt(
                    "Select track format",
                    track.get_formats(state.auth),
                    default=default_format,
                    repr_fun=lambda x, _: x.type.name,
                )
                if not format:
                    continue

                track.set_format(format)

                path = Path(
                    f"{', '.join(a.name for a in meta.artist)} - {meta.name}.{AudioCodec.get_extension(format.get_codec())}"
                )
                if args.output_directory:
                    path = Path(args.output_directory).expanduser().absolute() / path
                elif state.dir:
                    path = state.dir.expanduser().absolute() / path

                if args.sim_play and method == KeySource.WIDEVINE:
                    print("Cannot stream with widevine (yet)")
                    args.sim_play = False

                state.download_manager.enqueue(
                    SpotifyDownloadParam(
                        track=track,
                        auth=state.auth,
                        key_provider=state.playplay or state.widevine or state.client,
                        output=str(path),
                        emulate_playback=args.sim_play,
                    )
                )

            case ["metadata", *rest]:
                if state.auth.require_login():
                    print("Not logged in")
                    continue

                args = (
                    CommandParser()
                    .with_args(rest)
                    .add_argument("uri")
                    .add_argument("file")
                    .parse()
                )
                if not args:
                    continue

                track = Track.probe(args.uri)

                default_codec = AudioCodec.from_extension(Path(args.file).suffix)
                codec = prompt(
                    f"Choose the codec",
                    list(AudioCodec),
                    default=default_codec,
                    repr_fun=lambda x, _: x.name,
                )
                if not codec:
                    continue

                # TODO: probe from the file to choose the correct bitrate (not that it matters anyway)
                track.set_format(AudioFormat.from_codec(codec, AudioQuality.NORMAL))
                apply_metadata(track, str(args.file), state.auth)
            case ["req", *rest]:
                args = (
                    CommandParser()
                    .with_args(rest)
                    .add_argument("url")
                    .add_argument("-H", action="append", nargs=2)
                    .parse()
                )
                if not args:
                    continue

                if state.auth.require_login():
                    print("Not logged in")
                    continue

                res = state.auth.session.get(
                    args.url,
                    headers={k: v for k, v in args.H} if args.H else {},
                )
                if res.status_code != 200:
                    print(res.reason)
                    continue

                if "application/json" in res.headers["Content-Type"]:  # pyright: ignore[reportOperatorIssue]
                    print(json.dumps(res.json(), ensure_ascii=False, indent=4))  # pyright: ignore[reportUnknownMemberType]
                else:
                    print(res.content)
            case ["verbose"]:
                # TODO: i cannot configure logging multiple time
                logging.basicConfig(level=logging.DEBUG)
                print("verbose on")
            case ["out", dir]:
                if not Path(dir).expanduser().absolute().exists():
                    print(f"Path {dir} does not exists")
                    continue

                print(f"Output set to {dir!r}")
                state.dir = Path(dir)
            case ["volume", vol]:
                if not vol.isnumeric():
                    continue

                state.volume = float(vol)
                state.volume = min(max(state.volume, 0), 100)
            case _:
                print("Unknown command")

    readline.write_history_file(HISTORY_FILE)


if __name__ == "__main__":
    main()
