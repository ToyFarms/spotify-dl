# pyright: reportAny=false, reportExplicitAny=false

# TODO: persistent state management
# TODO: persistent download (allow for resuming interrupted download)

# NOTE: spotify download is currently not working (for free user only i think), because of some change in their backend, i cannot get the audio key, nothing i can do about it unless someone finds a way around it
# Issues: https://github.com/Googolplexed0/zotify/issues/86, https://github.com/DraftKinner/zotify/issues/95, https://github.com/kokarare1212/librespot-python/issues/315

import atexit
import json
import os
from pprint import pprint
import readline
import argparse
import shlex
import logging
import subprocess
import yt_dlp

from typing import Any, Callable, TypedDict, cast, override
from pathlib import Path
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from yt_dlp.utils import DownloadError

from spotify_dl.api.internal.spotify_client import SpotifyClient
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.cli import CLI
from spotify_dl.downloader import (
    SpotifyDownloadParam,
    SpotifyDownloadManager,
)
from spotify_dl.format import AudioCodec, AudioFormat, AudioQuality
from spotify_dl.metadata import apply_metadata
from spotify_dl.track import Track

from spotify_dl.utils.terminal import print_table
from spotify_dl.utils.ytdl import choose_best_audio_format


def get_username(auth: SpotifyAuthPKCE) -> str:
    if auth.require_login():
        return "Logged Out"

    res = auth.session.get("https://api.spotify.com/v1/me")

    if res.status_code != 200:
        print(
            f"Failed to get username ({res.status_code}): {res.json()['error']['message']}"
        )
        return "?"

    return cast(dict[str, str], res.json()).get("display_name", "?")


def prompt[T, K](
    prompt: str,
    items: Iterable[T],
    default: K | None = None,
    repr_fun: Callable[[T, int], str] = lambda x, _: str(x),
) -> T | K | None:
    items = list(items)

    for i, item in enumerate(items, 1):
        print(f"{i:>3} : {repr_fun(item, i - 1)}")

    try:
        while True:
            ans = input(prompt)

            if ans == "":
                return default

            if not ans.isnumeric():
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


@dataclass
class AppState:
    auth: SpotifyAuthPKCE
    name: str | None = None
    client: SpotifyClient | None = None
    running: bool = True
    last_json_output: Mapping[str, object] = field(default_factory=lambda: dict())
    dir: Path | None = None
    download_manager: SpotifyDownloadManager = field(
        default_factory=lambda: SpotifyDownloadManager(concurrent_download=2)
    )
    volume: float = 100


HISTORY_FILE = Path(".spotifydl_history")


def main() -> None:
    # TODO: basicConfig (cant) twice
    # logging.basicConfig(level=logging.INFO)

    _ = atexit.register(lambda: readline.write_history_file(HISTORY_FILE))

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

    state = AppState(
        auth=SpotifyAuthPKCE("user-read-private streaming"),
    )

    state.name = get_username(state.auth)
    cli = CLI(state.download_manager)

    while state.running:
        print()

        cli.prompting = True
        if program_args.command:
            commands: list[str] = shlex.split(program_args.command)
            state.running = False
        else:
            try:
                commands = shlex.split(input(f"{state.name} > "))
            except (EOFError, KeyboardInterrupt):
                print()
                break
            finally:
                cli.prompting = False

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
                state.client = SpotifyClient.random_ap()
                state.client.handshake()
                state.client.authenticate(state.auth.token.encode("utf-8"))

                print(
                    f"Successfully connected to {state.client.addr}:{state.client.port}"
                )
            case ["info", uri]:
                if state.auth.require_login():
                    print("Not logged in")
                    continue

                try:
                    track = Track.probe(uri)
                    meta = track.get_metadata(state.auth)
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
                    state.last_json_output = meta
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
                    f"Downloading {meta['name']!r} from the album {meta['album']['name']!r} (duration={meta['duration']}) featuring {len(meta['artist'])} artists: ",
                    end="",
                )
                for i, artist in enumerate(meta["artist"]):
                    if i != 0:
                        print(", ", end="")
                    print(f"{artist['name']}", end="")
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

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    artists = " ".join(artist["name"] for artist in meta["artist"])
                    info = ydl.extract_info(
                        f"ytsearch5:{artists} {meta['name']}", download=False
                    )

                    class Entry(TypedDict):
                        artist: str
                        title: str
                        duration: int
                        views: int
                        url: str
                        formats: list[dict]

                    formatted: list[Entry] = []
                    for entry in info["entries"]:
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

                        formatted.append(
                            {
                                "artist": artist,
                                "title": title,
                                "duration": duration,
                                "views": views,
                                "url": url,
                                "formats": formats,
                            }
                        )

                    entry = prompt(
                        "Select the video: ",
                        formatted,
                        default=formatted[0],
                        repr_fun=lambda x, _: f"{x['artist']} - {x['title']} (duration={x['duration']:_} views={x['views']:_})",
                    )

                    fmt = choose_best_audio_format(entry["formats"])

                    out_name = f"{meta['name']} - {', '.join(a['name'] for a in meta['artist'])}.%(ext)s"
                    path = Path(out_name)
                    if state.dir:
                        path = state.dir.expanduser().absolute() / path
                    outtmpl = str(path)

                    def hook(d):
                        if d.get("status") == "finished":
                            downloaded = (
                                d.get("filename")
                                or d.get("info_dict", {}).get("_filename")
                                or d.get("info_dict", {}).get("filepath")
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
                                    subprocess.run(
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
                        with yt_dlp.YoutubeDL(ydl_download_opts) as ydl2:
                            ydl2.download([entry["url"]])
                    except DownloadError as e:
                        print(
                            f"Requested format not available, falling back to 'bestaudio'. Error: {e}"
                        )
                        ydl_download_opts["format"] = "bestaudio"
                        with yt_dlp.YoutubeDL(ydl_download_opts) as ydl2:
                            ydl2.download([entry["url"]])

            case ["download" | "dl", *rest]:
                if state.auth.require_login():
                    print("Not logged in")
                    continue

                if not state.client:
                    print("Client not connected (connect/con)")
                    if input("Connect (Y/n)? ").lower() == "n":
                        continue

                    print("Connecting to Spotify...")
                    state.client = SpotifyClient.random_ap()
                    state.client.handshake()
                    state.client.authenticate(state.auth.token.encode("utf-8"))

                    print(
                        f"Successfully connected to {state.client.addr}:{state.client.port}"
                    )

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
                    f"Downloading {meta['name']!r} from the album {meta['album']['name']!r} featuring {len(meta['artist'])} artists: ",
                    end="",
                )
                for i, artist in enumerate(meta["artist"]):
                    if i != 0:
                        print(", ", end="")
                    print(f"{artist['name']}", end="")
                print()

                default_format = None
                for format in track.get_formats(state.auth):
                    if format.type == AudioFormat.Type.OGG_VORBIS_160:
                        default_format = format
                        break

                format = prompt(
                    "Select track format (OGG_VORBIS_160): ",
                    track.get_formats(state.auth),
                    default=default_format,
                    repr_fun=lambda x, _: x.type.name,
                )
                if not format:
                    continue

                track.set_format(format)

                path = Path(
                    f"{meta['name']} - {', '.join(a['name'] for a in meta['artist'])}.{AudioCodec.get_extension(format.get_codec())}"
                )
                if args.output_directory:
                    path = Path(args.output_directory).expanduser().absolute() / path
                elif state.dir:
                    path = state.dir.expanduser().absolute() / path

                state.download_manager.enqueue(
                    SpotifyDownloadParam(
                        track=track,
                        auth=state.auth,
                        client=state.client,
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
                    f"Choose the codec ({default_codec.name}): ",
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

                if "application/json" in res.headers["Content-Type"]:
                    print(json.dumps(res.json(), ensure_ascii=False, indent=4))
                else:
                    print(res.content)
            case ["verbose"]:
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
