from __future__ import annotations
from enum import Enum, auto
from typing import Self


class AudioCodec(Enum):
    UNKNOWN = auto()
    OGG_VORBIS = auto()
    MP3 = auto()
    AAC = auto()
    FLAC = auto()
    MP4 = auto()

    @staticmethod
    def from_format(format: AudioFormat.Type) -> "AudioCodec":
        if format in (
            AudioFormat.Type.OGG_VORBIS_96,
            AudioFormat.Type.OGG_VORBIS_160,
            AudioFormat.Type.OGG_VORBIS_320,
        ):
            return AudioCodec.OGG_VORBIS
        elif format in (
            AudioFormat.Type.MP3_96,
            AudioFormat.Type.MP3_160,
            AudioFormat.Type.MP3_160_ENC,
            AudioFormat.Type.MP3_256,
            AudioFormat.Type.MP3_320,
        ):
            return AudioCodec.MP3
        elif format in (
            AudioFormat.Type.AAC_24,
            AudioFormat.Type.AAC_48,
            AudioFormat.Type.AAC_160,
            AudioFormat.Type.AAC_320,
            AudioFormat.Type.XHE_AAC_12,
            AudioFormat.Type.XHE_AAC_16,
            AudioFormat.Type.XHE_AAC_24,
        ):
            return AudioCodec.AAC
        elif format in (AudioFormat.Type.FLAC_FLAC, AudioFormat.Type.FLAC_FLAC_24BIT):
            return AudioCodec.FLAC
        elif format in (
            AudioFormat.Type.MP4_128,
            AudioFormat.Type.MP4_256,
            AudioFormat.Type.MP4_128_DUAL,
            AudioFormat.Type.MP4_256_DUAL,
        ):
            return AudioCodec.MP4

        return AudioCodec.UNKNOWN

    @staticmethod
    def get_extension(codec: AudioCodec) -> str:
        if codec == AudioCodec.OGG_VORBIS:
            return "ogg"
        elif codec == AudioCodec.AAC:
            return "aac"
        elif codec == AudioCodec.FLAC:
            return "flac"
        elif codec == AudioCodec.MP3:
            return "mp3"
        elif codec == AudioCodec.MP4:
            return "mp4"

        return "bin"

    @classmethod
    def from_extension(cls, extension: str) -> AudioCodec:
        match extension.lower():
            case "ogg" | ".ogg":
                return AudioCodec.OGG_VORBIS
            case "aac" | ".aac":
                return AudioCodec.AAC
            case "flac" | ".flac":
                return AudioCodec.FLAC
            case "mp3" | ".mp3":
                return AudioCodec.MP3
            case "mp4" | ".mp4":
                return AudioCodec.MP4
            case _:
                return AudioCodec.UNKNOWN

    def to_mime(self) -> str:
        # TODO: convert staticmethod of get_* to class function
        # TODO: convert if statement to dictionary mapping
        return {
            AudioCodec.UNKNOWN: "application/octet-stream",
            AudioCodec.OGG_VORBIS: "audio/ogg",
            AudioCodec.MP3: "audio/mpeg",
            AudioCodec.AAC: "audio/aac",
            AudioCodec.FLAC: "audio/flac",
            AudioCodec.MP4: "audio/mp4",
        }.get(self, "application/octet-stream")


class AudioQuality(Enum):
    UNKNOWN = auto()
    NORMAL = auto()
    HIGH = auto()
    HIFI = auto()

    @staticmethod
    def from_format(format: AudioFormat.Type) -> "AudioQuality":
        if format in (
            AudioFormat.Type.MP3_96,
            AudioFormat.Type.OGG_VORBIS_96,
            AudioFormat.Type.XHE_AAC_12,
            AudioFormat.Type.MP4_128,
            AudioFormat.Type.MP4_128_DUAL,
        ):
            return AudioQuality.NORMAL
        elif format in (
            AudioFormat.Type.MP3_160,
            AudioFormat.Type.MP3_256,
            AudioFormat.Type.MP3_160_ENC,
            AudioFormat.Type.OGG_VORBIS_160,
            AudioFormat.Type.XHE_AAC_16,
            AudioFormat.Type.AAC_24,
            AudioFormat.Type.MP4_256,
            AudioFormat.Type.MP4_256_DUAL,
        ):
            return AudioQuality.NORMAL
        elif format in (
            AudioFormat.Type.MP3_320,
            AudioFormat.Type.OGG_VORBIS_320,
            AudioFormat.Type.AAC_48,
            AudioFormat.Type.AAC_160,
            AudioFormat.Type.AAC_320,
            AudioFormat.Type.XHE_AAC_24,
        ):
            return AudioQuality.HIFI
        return AudioQuality.UNKNOWN


class AudioFormat:
    class Type(Enum):
        UNKNOWN = auto()
        OGG_VORBIS_96 = auto()
        OGG_VORBIS_160 = auto()
        OGG_VORBIS_320 = auto()
        MP3_256 = auto()
        MP3_320 = auto()
        MP3_160 = auto()
        MP3_96 = auto()
        MP3_160_ENC = auto()
        AAC_24 = auto()
        AAC_48 = auto()
        FLAC_FLAC = auto()
        XHE_AAC_24 = auto()
        XHE_AAC_16 = auto()
        XHE_AAC_12 = auto()
        FLAC_FLAC_24BIT = auto()
        AAC_160 = auto()
        AAC_320 = auto()
        MP4_128 = auto()
        MP4_256 = auto()
        MP4_256_DUAL = auto()
        MP4_128_DUAL = auto()

    def __init__(self, type: AudioFormat.Type, file_id: str, gid: str) -> None:
        self.type: AudioFormat.Type = type
        self.file_id: str = file_id
        self.gid: str = gid

    def get_quality(self) -> AudioQuality:
        return AudioQuality.from_format(self.type)

    def get_codec(self) -> AudioCodec:
        return AudioCodec.from_format(self.type)

    # TODO: check for each format if it requires premium
    @classmethod
    def from_codec(cls, codec: AudioCodec, quality: AudioQuality) -> Self:
        for format in AudioFormat.Type:
            fcodec = AudioCodec.from_format(format)
            fquality = AudioQuality.from_format(format)

            if fcodec == codec and fquality == quality:
                return cls(format, "", "")

        return cls(AudioFormat.Type.UNKNOWN, "", "")
