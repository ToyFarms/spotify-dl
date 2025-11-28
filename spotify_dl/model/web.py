from typing import Literal, TypedDict

from spotify_dl.model.shared import URL, SpotifyURI, ISO3166_2


class ExternalURL(TypedDict):
    spotify: URL  # https://open.spotify.com/track/3jpWkQQUpwHe8m741B7bIO


class ExternalID(TypedDict):
    isrc: str  # JPU902403966
    ean: str
    upc: str


class Artist(TypedDict):
    external_urls: ExternalURL  # https://open.spotify.com/artist/45ft4DyTCEJfQwTBHXpdhM
    href: URL  # https://api.spotify.com/v1/artists/45ft4DyTCEJfQwTBHXpdhM
    id: str  # 45ft4DyTCEJfQwTBHXpdhM
    name: str  # milet
    type: str  # artist
    uri: SpotifyURI  # spotify:artist:45ft4DyTCEJfQwTBHXpdhM


class Image(TypedDict):
    url: URL  # https://i.scdn.co/image/ab67616d0000b273820ddfa86b8179c11d5b3c94
    width: int  # 640
    height: int  # 640


class Album(TypedDict):
    artists: list[Artist]
    available_markets: list[ISO3166_2]
    images: list[Image]
    external_urls: ExternalURL  # https://open.spotify.com/album/4OeZlhYN40oXF6bUfJTl1A
    album_type: str  # single
    href: URL  # https://api.spotify.com/v1/albums/4OeZlhYN40oXF6bUfJTl1A
    id: str  # 4OeZlhYN40oXF6bUfJTl1A
    name: str  # I still / Nobody Knows
    release_date: str  # 2025-02-26
    release_date_precision: str  # day
    type: Literal["album"]
    uri: SpotifyURI  # spotify:album:4OeZlhYN40oXF6bUfJTl1A
    total_tracks: int  # 2


class TrackMetadata(TypedDict):
    artists: list[Artist]
    available_markets: list[ISO3166_2]
    album: Album
    external_ids: ExternalID
    external_urls: ExternalURL
    disc_number: int  # 1
    duration_ms: int  # 216429
    popularity: int  # 54
    track_number: int  # 2
    explicit: bool  # False
    is_local: bool  # False
    href: URL  # https://api.spotify.com/v1/tracks/3jpWkQQUpwHe8m741B7bIO
    id: str  # 3jpWkQQUpwHe8m741B7bIO
    name: str  # Nobody Knows
    preview_url: URL  # https://p.scdn.co/mp3-preview/704566bae456a73dd3be16d4e7684906e6b109e9?cid=65b708073fc0480ea92a077233ca87bd
    type: str  # track
    uri: SpotifyURI  # spotify:track:3jpWkQQUpwHe8m741B7bIO


class ArtistFollower(TypedDict):
    href: URL | None  # null
    total: int  # 21928194


class ArtistMetadata(TypedDict):
    external_urls: ExternalURL
    followers: ArtistFollower
    genres: list[str]  # [progressive rock, rock, ...]
    href: URL  # https://api.spotify.com/v1/artists/0k17h0D3J5VfsdmQ1iZtE9
    id: str  # 0k17h0D3J5VfsdmQ1iZtE9
    images: list[Image]
    name: str  # Pink Floyd
    popularity: int  # 82
    type: Literal["artist"]
    uri: SpotifyURI


class ManifestFileMP4(TypedDict):
    bitrate: int  # 256000
    file_id: str  # 05c72a33...
    file_url: URL | None  # null or URL
    impression_urls: list[URL] | None  # null or list of URLs
    track_type: str  # AUDIO
    format: str  # 11 or 10
    audio_quality: str  # VERY_HIGH, HIGH
    hifi_status: str | None  # NONE
    gain_db: float | None  # null
    expires_at: str | None  # null or timestamp
    average_bitrate: int | None  # 260280


class Manifest(TypedDict):
    file_ids_mp4: list[ManifestFileMP4]


class Author(TypedDict):
    name: str
    uri: SpotifyURI


class ItemMetadata(TypedDict):
    uri: SpotifyURI  # spotify:track:...
    linked_from_uri: SpotifyURI | None  # null
    context_description: str | None  # null
    context_uri: SpotifyURI | None  # spotify:track:...
    name: str
    group_name: str | None
    group_uri: SpotifyURI | None  # spotify:album:...
    authors: list[Author]
    duration: int  # 274796
    images: list[Image]
    episode_content_type: str | None  # null
    show_content_type: str | None  # null
    playback_platform_context_id: str | None  # null
    playback_platform_generated_audio: str | None  # null
    is_explicit: bool  # False


class Item(TypedDict):
    metadata: ItemMetadata
    manifest: Manifest
    audio_id: str | None  # null
    track_type: Literal["AUDIO"]
    ms_played_until_update: int  # 30000
    ms_playing_update_interval: int  # 0
    content_type: Literal["TRACK"]


class MediaEntry(TypedDict):
    item: Item


class MediaResponse(TypedDict):
    media: dict[SpotifyURI, MediaEntry]
