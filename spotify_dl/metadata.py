# pyright: reportUnknownMemberType=false, reportAny=false, reportPrivateImportUsage=false
import io
import logging
import base64

from mutagen.id3 import (
    ID3,
    TIT2,
    TPE1,
    TALB,
    TDRC,
    TRCK,
    TPOS,
    TSRC,
    POPM,
    APIC,
    TXXX,
    USLT,
    SYLT,
)
from mutagen.mp4 import MP4, AtomDataType, MP4Cover, MP4FreeForm, MP4Tags
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import Picture as FLACPicture
from functools import reduce
from typing import Callable, Protocol, cast, override
from PIL import Image
from pathlib import Path
from urllib.request import urlopen
from enum import Enum, auto
from urllib.parse import quote

from spotify_dl.api.musicbrainz.mbid import MBID
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.format import AudioCodec
from spotify_dl.model.id3 import ID3PictureType
from spotify_dl.model.web import ArtistMetadata
from spotify_dl.track import ReplayGain, Track
from spotify_dl.api.musicbrainz.cover import CoverArts
from spotify_dl.utils.misc import url_build


class MetadataFormat(Enum):
    UNKNOWN = auto()
    ID3 = auto()
    ATOMS = auto()
    VORBIS_COMMENT = auto()
    RIFF_INFO = auto()

    @staticmethod
    def from_codec(codec: AudioCodec) -> "MetadataFormat":
        match codec:
            case AudioCodec.OGG_VORBIS:
                return MetadataFormat.VORBIS_COMMENT
            case AudioCodec.MP3:
                return MetadataFormat.ID3
            case AudioCodec.AAC:
                return MetadataFormat.ATOMS
            case AudioCodec.FLAC:
                return MetadataFormat.VORBIS_COMMENT
            case AudioCodec.MP4:
                return MetadataFormat.ATOMS
            case AudioCodec.UNKNOWN:
                return MetadataFormat.UNKNOWN


class MetadataProtocol(Protocol):
    def save(self) -> None: ...
    def title(self, x: str | None) -> None: ...
    def artists(self, x: list[str] | None) -> None: ...
    def album_name(self, x: str | None) -> None: ...
    def recording_time(self, x: str | None) -> None: ...
    def track_number(self, x: str | None) -> None: ...
    def disc_number(self, x: str | None) -> None: ...
    def isrc(self, x: str | None) -> None: ...
    def popularity(self, x: int | None) -> None: ...
    def picture(
        self,
        img_data: bytes | None,
        desc: str | None,
        type: int | ID3PictureType | None,
    ) -> None: ...
    def lyrics_synced(self, x: list[tuple[str, int]], lang_iso3: str) -> None: ...
    def lyrics(self, x: list[str], lang_iso3: str) -> None: ...


class ReplayGainProtocol(Protocol):
    def track_gain(self, x: float | None) -> None: ...
    def track_peak(self, x: float | None) -> None: ...
    def album_gain(self, x: float | None) -> None: ...
    def album_peak(self, x: float | None) -> None: ...


class BaseMetadataProvider:
    def __init__(self, file: str, codec: AudioCodec | None) -> None:
        self.file: str = file
        self.codec: AudioCodec = codec or AudioCodec.from_extension(
            Path(file).suffix[1:]
        )

    def _to_timestamp(self, ms: int) -> str:
        h = ms // 3_600_000
        m = (ms % 3_600_000) // 60_000
        s = (ms % 60_000) / 1000

        return f"{h:02d}:{m:02d}:{s:06.3f}"

    def _build_ttml_format(self, lyrics: list[tuple[str, int]]) -> str:
        # <p begin="00:30.000" end="00:35.000">First line</p>
        formatted_lyrics: list[str] = []

        for i, (lyric, start_ms) in enumerate(lyrics):
            end_ms = lyrics[i + 1][1] if i + 1 < len(lyrics) else start_ms + 2000

            formatted_lyrics.append(
                f'<p begin="{self._to_timestamp(start_ms)}" end={self._to_timestamp(end_ms)}>{lyric}</p>'
            )

        return """<lyrics xmlns="http://www.w3.org/ns/ttml" 
xmlns:itunes="http://www.apple.com/itunes/lyrics">
    <div itunes:song-part="Verse">
        {}
    </div>
</lyrics>""".format(
            "\n".join(formatted_lyrics)
        )


class MetadataProviderID3(MetadataProtocol, ReplayGainProtocol, BaseMetadataProvider):
    logger: logging.Logger = logging.getLogger("spdl:metadata:id3")

    def __init__(self, file: str, codec: AudioCodec | None) -> None:
        super().__init__(file, codec)

        self.tags: ID3 = ID3(file)

    @override
    def save(self) -> None:
        self.tags.save(v2_version=3)

    @override
    def lyrics_synced(self, x: list[tuple[str, int]], lang_iso3: str) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have lyrics_synced")
            return

        self.tags.add(SYLT(encoding=3, lang=lang_iso3, format=2, type=1, text=x))

    @override
    def lyrics(self, x: list[str], lang_iso3: str) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have lyrics")
            return

        self.tags.add(USLT(encoding=3, lang=lang_iso3, text=x))

    @override
    def track_gain(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track_gain")
            return

        self.tags.add(TXXX(encoding=3, text=f"REPLAYGAIN_TRACK_GAIN={x}"))

    @override
    def track_peak(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track_peak")
            return

        self.tags.add(TXXX(encoding=3, text=f"REPLAYGAIN_TRACK_PEAK={x}"))

    @override
    def album_gain(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album_gain")
            return

        self.tags.add(TXXX(encoding=3, text=f"REPLAYGAIN_ALBUM_GAIN={x}"))

    @override
    def album_peak(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album_peak")
            return

        self.tags.add(TXXX(encoding=3, text=f"REPLAYGAIN_ALBUM_PEAK={x}"))

    @override
    def title(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have title")
            return

        self.tags.add(TIT2(encoding=3, text=x))

    @override
    def artists(self, x: list[str] | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have artists")
            return

        self.tags.add(TPE1(encoding=3, text=x))

    @override
    def album_name(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album_name")
            return

        self.tags.add(TALB(encoding=3, text=x))

    @override
    def recording_time(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have recording_time")
            return

        self.tags.add(TDRC(encoding=3, text=x))

    @override
    def track_number(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track_number")
            return

        self.tags.add(TRCK(encoding=3, text=x))

    @override
    def disc_number(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have disc_number")
            return

        self.tags.add(TPOS(encoding=3, text=x))

    @override
    def isrc(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have isrc")
            return

        self.tags.add(TSRC(encoding=3, text=x))

    @override
    def popularity(self, x: int | None) -> None:
        if x is None:
            self.logger.warning(f"{self.file!r} does not have popularity")
            return

        self.tags.add(POPM(email="spotify", rating=x, data=b""))

    @override
    def picture(
        self,
        img_data: bytes | None,
        desc: str | None,
        type: int | ID3PictureType | None,
    ) -> None:
        if not img_data or not type:
            self.logger.warning(f"{self.file!r} does not have picture {desc}: {type}")
            return

        img = Image.open(io.BytesIO(img_data))

        if not img.format:
            self.logger.error("Could not get image format")
            return
        elif img.format not in Image.MIME:
            self.logger.error(f"Could not determine image MIME: {img.format}")
            return

        self.tags.add(
            APIC(
                encoding=3,
                mime=Image.MIME[img.format],
                type=type if isinstance(type, int) else type.value,
                desc=desc,
                data=img_data,
            )
        )


class MetadataProviderAtoms(MetadataProtocol, ReplayGainProtocol, BaseMetadataProvider):
    logger: logging.Logger = logging.getLogger("spdl:metadata:atoms")

    def __init__(self, file: str, codec: AudioCodec | None) -> None:
        super().__init__(file, codec)
        self.tags: MP4 = MP4(file)

        self._pending_picture: list[MP4Cover] = []

    @override
    def save(self) -> None:
        if not self.tags.tags:
            return

        if self._pending_picture:
            self.tags.tags["covr"] = self._pending_picture

        self.tags.save()

    @override
    def lyrics_synced(self, x: list[tuple[str, int]], lang_iso3: str) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have lyrics_synced")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()

        self.tags.tags["----:com.apple.iTunes:lyrics"] = [
            MP4FreeForm(
                self._build_ttml_format(x).encode("utf-8"),
                dataformat=AtomDataType.XML,
            )
        ]

    @override
    def lyrics(self, x: list[str], lang_iso3: str) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have lyrics")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()

        self.tags.tags["\xa9lyr"] = ["\n".join(x)]

    @override
    def track_gain(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track_gain")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()

        self.tags.tags["REPLAYGAIN_TRACK_GAIN"] = [str(x)]

    @override
    def track_peak(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track_peak")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()

        self.tags.tags["REPLAYGAIN_TRACK_PEAK"] = [str(x)]

    @override
    def album_gain(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album_gain")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()

        self.tags.tags["REPLAYGAIN_ALBUM_GAIN"] = [str(x)]

    @override
    def album_peak(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album_peak")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()

        self.tags.tags["REPLAYGAIN_ALBUM_PEAK"] = [str(x)]

    @override
    def title(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have title")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        self.tags.tags["\u00a9nam"] = [x]

    @override
    def artists(self, x: list[str] | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have artists")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        self.tags.tags["\u00a9ART"] = x

    @override
    def album_name(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album name")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        self.tags.tags["\u00a9alb"] = [x]

    @override
    def recording_time(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have recording time")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        self.tags.tags["\u00a9day"] = [x]

    @override
    def track_number(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track number")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        num, total = x.split("/")
        self.tags.tags["trkn"] = [(int(num), int(total))]

    @override
    def disc_number(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have disc number")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        num, total = x.split("/")
        self.tags.tags["disk"] = [(int(num), int(total))]

    @override
    def isrc(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have ISRC")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        self.tags.tags["isrc"] = [x]

    @override
    def popularity(self, x: int | None) -> None:
        if x is None:
            self.logger.warning(f"{self.file!r} does not have popularity")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        self.tags.tags["tmpo"] = [x]

    @override
    def picture(
        self,
        img_data: bytes | None,
        desc: str | None,
        type: int | ID3PictureType | None,
    ) -> None:
        if not img_data:
            self.logger.warning(f"{self.file!r} does not have picture {desc}: {type}")
            return
        if not self.tags.tags:
            self.tags.tags = MP4Tags()
        img = Image.open(io.BytesIO(img_data))
        fmt = MP4Cover.FORMAT_PNG if img.format == "PNG" else MP4Cover.FORMAT_JPEG
        cover = MP4Cover(img_data, imageformat=fmt)

        self._pending_picture.append(cover)


class MetadataProviderVorbisComment(
    MetadataProtocol, ReplayGainProtocol, BaseMetadataProvider
):
    logger: logging.Logger = logging.getLogger("spdl:metadata:vorbis")

    def __init__(self, file: str, codec: AudioCodec | None) -> None:
        super().__init__(file, codec)
        self.tags: OggVorbis = OggVorbis(file)

        self._pending_picture: list[str] = []

    @override
    def save(self) -> None:
        if self._pending_picture:
            self.tags["METADATA_BLOCK_PICTURE"] = self._pending_picture
        self.tags.save()

    @override
    def lyrics_synced(self, x: list[tuple[str, int]], lang_iso3: str) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have lyrics_synced")
            return
        lyrics: list[str] = []
        for lyric, start_ms in x:
            lyrics.append(f"[{self._to_timestamp(start_ms)}]{lyric}")

        self.tags["LYRICS"] = ["\n".join(lyrics)]

    @override
    def lyrics(self, x: list[str], lang_iso3: str) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have lyrics")
            return

        self.tags["LYRICS"] = ["\n".join(x)]

    @override
    def track_gain(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track_gain")
            return

        self.tags["REPLAYGAIN_TRACK_GAIN"] = [str(x)]

    @override
    def track_peak(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track_peak")
            return

        self.tags["REPLAYGAIN_TRACK_PEAK"] = [str(x)]

    @override
    def album_gain(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album_gain")
            return

        self.tags["REPLAYGAIN_ALBUM_GAIN"] = [str(x)]

    @override
    def album_peak(self, x: float | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album_peak")
            return

        self.tags["REPLAYGAIN_ALBUM_PEAK"] = [str(x)]

    @override
    def title(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have title")
            return
        self.tags["TITLE"] = [x]

    @override
    def artists(self, x: list[str] | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have artists")
            return
        self.tags["ARTIST"] = x

    @override
    def album_name(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have album name")
            return
        self.tags["ALBUM"] = [x]

    @override
    def recording_time(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have recording time")
            return
        self.tags["DATE"] = [x]

    @override
    def track_number(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have track number")
            return
        self.tags["TRACKNUMBER"] = [x]

    @override
    def disc_number(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have disc number")
            return
        self.tags["DISCNUMBER"] = [x]

    @override
    def isrc(self, x: str | None) -> None:
        if not x:
            self.logger.warning(f"{self.file!r} does not have ISRC")
            return
        self.tags["ISRC"] = [x]

    @override
    def popularity(self, x: int | None) -> None:
        if x is None:
            self.logger.warning(f"{self.file!r} does not have popularity")
            return
        self.tags["POPULARITY"] = [str(x)]

    @override
    def picture(
        self,
        img_data: bytes | None,
        desc: str | None,
        type: int | ID3PictureType | None,
    ) -> None:
        if not img_data or not type:
            self.logger.warning(f"{self.file!r} missing picture metadata")
            return

        img = Image.open(io.BytesIO(img_data))

        pic = FLACPicture()
        mode_to_bpp = {
            "1": 1,
            "L": 8,
            "P": 8,
            "RGB": 24,
            "RGBA": 32,
            "CMYK": 32,
            "YCbCr": 24,
            "I": 32,
            "F": 32,
        }

        pic.data = img_data
        pic.mime = Image.MIME.get(img.format or "PNG", "image/png")
        pic.type = type if isinstance(type, int) else type.value
        pic.desc = desc
        pic.depth = mode_to_bpp[img.mode]
        pic.width = img.width
        pic.height = img.height

        b64 = base64.b64encode(pic.write()).decode("ascii")

        self._pending_picture.append(b64)


MetadataMapping = {
    MetadataFormat.ID3: MetadataProviderID3,
    MetadataFormat.ATOMS: MetadataProviderAtoms,
    MetadataFormat.VORBIS_COMMENT: MetadataProviderVorbisComment,
    MetadataFormat.RIFF_INFO: None,
    MetadataFormat.UNKNOWN: None,
}


def apply_metadata(
    track: Track, path: str, auth: SpotifyAuthPKCE, replaygain: ReplayGain | None = None
) -> None:
    logger = logging.getLogger("spdl:metadata")

    if not track.format:
        raise ValueError("Track format is not set")

    codec = track.format.get_codec()
    if codec == AudioCodec.UNKNOWN:
        print(f"Could not get codec, {track.format} ({path})")
        return

    format = MetadataFormat.from_codec(codec)
    provider_cls = MetadataMapping[format]
    if not provider_cls:
        raise NotImplementedError(
            f"Metadata for codec {codec.name} is not implemented",
        )

    provider = provider_cls(path, codec)

    meta = track.get_metadata(auth)
    meta2 = track.get_metadata_internal(auth)

    provider.title(meta.get("name"))
    provider.artists(list(map(lambda x: x["name"], meta.get("artists", []))))

    album = meta.get("album")
    isrc = meta.get("external_ids", {}).get("isrc")
    if album:
        provider.album_name(album.get("name"))
        provider.recording_time(album.get("release_date"))

        track_number = meta.get("track_number", 1)
        total_track = album.get("total_tracks", 1)
        disc_number = meta.get("disc_number", 1)
        total_disc = album.get("total_discs", 1)

        provider.track_number(f"{track_number}/{total_track}")
        provider.disc_number(f"{disc_number}/{total_disc}")

        # use_mb = cast(str | None, isrc) is not None
        use_mb = False  # see TODO

        if use_mb:
            arts = CoverArts(MBID.from_isrc(isrc))
            images = list(arts.get_images())

            if not images:
                use_mb = False

            for art in images:
                data = art.fetch("1200")
                provider.picture(
                    data,
                    art.data["comment"] or art.type.name.title(),
                    art.type_as_id3.value,
                )

        if not use_mb:
            images = album.get("images", [])
            cover = _get_highest_resolution(
                images, key=lambda x: (x["width"], x["height"])
            )
            if cover:
                data = urlopen(cover["url"])
                provider.picture(data.read(), "Cover", ID3PictureType.FRONT_COVER)

        if meta2.has_lyrics and album.get("images"):
            url = url_build(
                (
                    "https://spclient.wg.spotify.com/color-lyrics/v2/track/"
                    f"{track.id_b62}/image/{quote(album['images'][0]['url'], safe='')}"
                ),
                format="json",
                vocalRemoval="false",
                market="from_token",
            )
            res = auth.session.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                    "app-platform": "WebPlayer",
                },
            )
            if res.status_code == 200:
                json = res.json().get("lyrics")
                if json:
                    type = json.get("syncType")

                    if type == "LINE_SYNCED":
                        lyrics_synced: list[tuple[str, int]] = [
                            (line["words"], int(line["startTimeMs"]))
                            for line in json.get("lines", [])
                        ]

                        provider.lyrics_synced(lyrics_synced, "xxx")
                    else:
                        lyrics: list[str] = [
                            line["words"] for line in json.get("lines", [])
                        ]
                        provider.lyrics(lyrics, "xxx")
                else:
                    logger.error("Expecting lyrics but found NONE")

            else:
                logger.error(
                    f"Failed to fetch lyric from {url!r} ({res.status_code}): {res.reason}"
                )
    else:
        logger.warning("No album info found")

    for artist in meta.get("artists", []):
        artist_meta: ArtistMetadata = auth.session.get(artist["href"]).json()
        images = artist_meta.get("images", [])
        cover = _get_highest_resolution(images, key=lambda x: (x["width"], x["height"]))
        if cover:
            data = urlopen(cover["url"])
            provider.picture(data.read(), artist_meta["name"], ID3PictureType.ARTIST)

    provider.isrc(isrc)
    if meta.get("popularity", 0) != 0:
        provider.popularity(int(meta.get("popularity", 0) * 2.55))

    if replaygain:
        provider.track_gain(replaygain.track_gain_db)
        provider.track_peak(replaygain.track_peak)
        provider.album_gain(replaygain.album_gain_db)
        provider.album_peak(replaygain.album_peak)

    # TODO: sometimes fail because of header something something
    provider.save()


def _get_highest_resolution[T](
    res: list[T],
    key: Callable[[T], tuple[int, int]] | None = None,
) -> T | None:
    if not res:
        return None

    def get(item: T) -> tuple[int, int]:
        if isinstance(item, (tuple, list)) and item.__len__() > 2:
            return int(cast(int, item[0])), int(cast(int, item[1]))

        raise ValueError("Expected a sequence of (width, height)")

    key = key or get

    try:
        return max(res, key=lambda item: reduce(lambda a, b: a * b, key(item)))
    except Exception:
        return None
