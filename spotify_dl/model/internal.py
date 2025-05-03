from typing import TypedDict

from spotify_dl.model.shared import SpotifyURI


class ContentAuthorizationAttributes(TypedDict, total=False):
    pass  # no fields currently defined


class ArtistSummary(TypedDict):
    gid: str  # 86359aa4e2234d3c94303f21a249cdca
    name: str  # milet


class ExternalIDItem(TypedDict):
    type: str  # isrc
    id: str  # JPU902403965


class FileItem(TypedDict):
    file_id: str  # 33ea75ac9ebeffdd01f77cd387d981f5e309363a
    format: str  # OGG_VORBIS_320


class PreviewItem(TypedDict):
    file_id: str  # 51df8178db0c9d6f902125c59a64d764b054dc5b
    format: str  # MP3_96


class ArtistWithRoleItem(TypedDict):
    artist_gid: str  # 86359aa4e2234d3c94303f21a249cdca
    artist_name: str  # milet
    role: str  # ARTIST_ROLE_MAIN_ARTIST


class OriginalAudioFormat(TypedDict):
    uuid: str  # b3c6857790274da3aeaf1361e31ae605
    format: str  # AUDIO_FORMAT_STEREO


class AudioFormatItem(TypedDict):
    original_audio: OriginalAudioFormat


class AlbumDate(TypedDict):
    year: int  # 2025
    month: int  # 1
    day: int  # 31


class CoverImage(TypedDict):
    file_id: str  # ab67616d00001e026e3bc3119c92983a429e51e4
    size: str  # DEFAULT
    width: int  # 300
    height: int  # 300


class CoverGroup(TypedDict):
    image: list[CoverImage]  # list of cover images


class AlbumArtist(TypedDict):
    gid: str  # 86359aa4e2234d3c94303f21a249cdca
    name: str  # milet


class Licensor(TypedDict):
    uuid: str  # aa9468539d19400ca4c32fdc159926a9


class Album(TypedDict):
    gid: str  # 09317aa49a25401387992443b2e8e7fb
    name: str  # I still
    label: str  # Sony Music Labels Inc.
    artist: list[AlbumArtist]
    date: AlbumDate
    cover_group: CoverGroup
    licensor: Licensor


class TrackMetadata(TypedDict):
    gid: str  # f8c666a0a1fe43ffaaded197ab0838df
    name: str  # I still
    number: int  # 1
    disc_number: int  # 1
    duration: int  # 267436 (milliseconds)
    popularity: int  # 65
    earliest_live_timestamp: int  # 1738234800 (Unix timestamp)
    has_lyrics: bool
    original_title: str  # I still
    canonical_uri: SpotifyURI
    content_authorization_attributes: ContentAuthorizationAttributes
    artist: list[ArtistSummary]
    external_id: list[ExternalIDItem]
    file: list[FileItem] | None
    alternative: list[FileItem] | None
    preview: list[PreviewItem]
    language_of_performance: list[str]  # ["ja"]
    artist_with_role: list[ArtistWithRoleItem]
    audio_formats: list[AudioFormatItem]
    album: Album
    licensor: Licensor
    original_audio: OriginalAudioFormat
