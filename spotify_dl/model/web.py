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
