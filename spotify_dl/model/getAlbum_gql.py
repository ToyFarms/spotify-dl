from typing import Literal, TypedDict

from spotify_dl.model.shared import URL, SpotifyURI


class ImageSource(TypedDict):
    url: URL
    width: int
    height: int


class ColorHex(TypedDict):
    hex: str


class ExtractedColors(TypedDict):
    colorRaw: ColorHex
    colorLight: ColorHex
    colorDark: ColorHex


class CoverArt(TypedDict):
    extractedColors: ExtractedColors
    sources: list[ImageSource]


class ArtistProfile(TypedDict):
    name: str


class AvatarImage(TypedDict):
    sources: list[ImageSource]


class ArtistVisuals(TypedDict):
    avatarImage: AvatarImage


class AlbumArtist(TypedDict):
    id: str
    uri: SpotifyURI
    profile: ArtistProfile
    visuals: ArtistVisuals
    sharingInfo: "SharingInfo"


class AlbumArtists(TypedDict):
    totalCount: int
    items: list[AlbumArtist]


class SharingInfo(TypedDict):
    shareUrl: URL
    shareId: str


class AlbumDate(TypedDict):
    isoString: str
    precision: Literal["DAY"]


class AlbumYearDate(TypedDict):
    year: int


class Playability(TypedDict):
    playable: bool
    reason: Literal["PLAYABLE"] | None


class DiscTracks(TypedDict):
    totalCount: int


class Disc(TypedDict):
    number: int
    tracks: DiscTracks


class Discs(TypedDict):
    totalCount: int
    items: list[Disc]


class CopyrightItem(TypedDict):
    type: Literal["C", "P"]
    text: str


class Copyright(TypedDict):
    totalCount: int
    items: list[CopyrightItem]


class TrackArtist(TypedDict):
    uri: SpotifyURI
    profile: ArtistProfile


class TrackArtists(TypedDict):
    items: list[TrackArtist]


class ContentRating(TypedDict):
    label: Literal["NONE"]


class Duration(TypedDict):
    totalMilliseconds: int


class AlbumTrack(TypedDict):
    saved: bool
    uri: SpotifyURI
    name: str
    playcount: str
    discNumber: int
    trackNumber: int
    contentRating: ContentRating
    relinkingInformation: None
    duration: Duration
    playability: Playability
    artists: TrackArtists


class AlbumTrackItem(TypedDict):
    uid: str
    track: AlbumTrack


class AlbumTracks(TypedDict):
    totalCount: int
    items: list[AlbumTrackItem]


class Releases(TypedDict):
    totalCount: int
    items: list[None]


class DiscographyAlbum(TypedDict):
    id: str
    uri: SpotifyURI
    name: str
    date: AlbumYearDate
    coverArt: CoverArt
    playability: Playability
    sharingInfo: SharingInfo
    type: Literal["SINGLE", "EP"]


class PopularReleasesAlbums(TypedDict):
    items: list[DiscographyAlbum]


class Discography(TypedDict):
    popularReleasesAlbums: PopularReleasesAlbums


class MoreAlbumsByArtistItem(TypedDict):
    discography: Discography


class MoreAlbumsByArtist(TypedDict):
    items: list[MoreAlbumsByArtistItem]


class AlbumUnion(TypedDict):
    __typename: Literal["Album"]
    uri: SpotifyURI
    name: str
    artists: AlbumArtists
    coverArt: CoverArt
    discs: Discs
    releases: Releases
    type: Literal["EP"]
    date: AlbumDate
    playability: Playability
    label: str
    copyright: Copyright
    courtesyLine: str
    saved: bool
    sharingInfo: SharingInfo
    tracks: AlbumTracks
    moreAlbumsByArtist: MoreAlbumsByArtist


class Data(TypedDict):
    albumUnion: AlbumUnion


class GraphQLResponse(TypedDict):
    data: Data


# {
#     "data": {
#         "albumUnion": {
#             "__typename": "Album",
#             "uri": "spotify:album:7DsLGDK8qjjgQTMO8iLHkz",
#             "name": "\\u30a2\\u30ca\\u30b6\\u30fc\\u30c0\\u30a4\\u30d0\\u30fc\\u30b7\\u30c6\\u30a3",
#             "artists": {
#                 "totalCount": 1,
#                 "items": [
#                     {
#                         "id": "47MRpWYlFaneZAlaXrt9bu",
#                         "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                         "profile": {
#                             "name": "\\u30ec\\u30c8\\u30ed\\u30ea\\u30ed\\u30f3"
#                         },
#                         "visuals": {
#                             "avatarImage": {
#                                 "sources": [
#                                     {
#                                         "url": "https://i.scdn.co/image/ab6761610000e5eb8eb92d88b11fdb10da14d101",
#                                         "width": 640,
#                                         "height": 640,
#                                     },
#                                     {
#                                         "url": "https://i.scdn.co/image/ab6761610000f1788eb92d88b11fdb10da14d101",
#                                         "width": 160,
#                                         "height": 160,
#                                     },
#                                     {
#                                         "url": "https://i.scdn.co/image/ab676161000051748eb92d88b11fdb10da14d101",
#                                         "width": 320,
#                                         "height": 320,
#                                     },
#                                 ]
#                             }
#                         },
#                         "sharingInfo": {
#                             "shareUrl": "https://open.spotify.com/artist/47MRpWYlFaneZAlaXrt9bu?si=Q7FETGrPT6eZzSBCVeFknA"
#                         },
#                     }
#                 ],
#             },
#             "coverArt": {
#                 "extractedColors": {
#                     "colorRaw": {"hex": "#C01828"},
#                     "colorLight": {"hex": "#E91D31"},
#                     "colorDark": {"hex": "#C01828"},
#                 },
#                 "sources": [
#                     {
#                         "url": "https://i.scdn.co/image/ab67616d00001e02ace3691d801acd4c2ede4189",
#                         "width": 300,
#                         "height": 300,
#                     },
#                     {
#                         "url": "https://i.scdn.co/image/ab67616d00004851ace3691d801acd4c2ede4189",
#                         "width": 64,
#                         "height": 64,
#                     },
#                     {
#                         "url": "https://i.scdn.co/image/ab67616d0000b273ace3691d801acd4c2ede4189",
#                         "width": 640,
#                         "height": 640,
#                     },
#                 ],
#             },
#             "discs": {
#                 "totalCount": 1,
#                 "items": [{"number": 1, "tracks": {"totalCount": 5}}],
#             },
#             "releases": {"totalCount": 0, "items": []},
#             "type": "EP",
#             "date": {"isoString": "2025-01-22T00:00:00Z", "precision": "DAY"},
#             "playability": {"playable": true, "reason": "PLAYABLE"},
#             "label": "RETRORIRON / Lastrum Music Entertainment",
#             "copyright": {
#                 "totalCount": 2,
#                 "items": [
#                     {
#                         "type": "C",
#                         "text": "\\u00a9 2025 RETRORIRON / Lastrum Music Entertainment",
#                     },
#                     {
#                         "type": "P",
#                         "text": "\\u2117 2025 RETRORIRON / Lastrum Music Entertainment",
#                     },
#                 ],
#             },
#             "courtesyLine": "",
#             "saved": false,
#             "sharingInfo": {
#                 "shareUrl": "https://open.spotify.com/album/7DsLGDK8qjjgQTMO8iLHkz?si=fYRJvcQ3QxWRe0Mhu2m29g",
#                 "shareId": "fYRJvcQ3QxWRe0Mhu2m29g",
#             },
#             "tracks": {
#                 "totalCount": 5,
#                 "items": [
#                     {
#                         "uid": "93520f451a4ba5f61c2e",
#                         "track": {
#                             "saved": false,
#                             "uri": "spotify:track:3y2f9PVJjgGDxS0qFYIdJe",
#                             "name": "\\u30ef\\u30f3\\u30bf\\u30a4\\u30e0\\u30a8\\u30d4\\u30ed\\u30fc\\u30b0",
#                             "playcount": "1128272",
#                             "discNumber": 1,
#                             "trackNumber": 1,
#                             "contentRating": {"label": "NONE"},
#                             "relinkingInformation": null,
#                             "duration": {"totalMilliseconds": 214200},
#                             "playability": {"playable": true},
#                             "artists": {
#                                 "items": [
#                                     {
#                                         "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                                         "profile": {
#                                             "name": "\\u30ec\\u30c8\\u30ed\\u30ea\\u30ed\\u30f3"
#                                         },
#                                     }
#                                 ]
#                             },
#                         },
#                     }
#                 ],
#             },
#             "moreAlbumsByArtist": {
#                 "items": [
#                     {
#                         "discography": {
#                             "popularReleasesAlbums": {
#                                 "items": [
#                                     {
#                                         "id": "2H2lOVsdIvonip4PmKqFfW",
#                                         "uri": "spotify:album:2H2lOVsdIvonip4PmKqFfW",
#                                         "name": "\\u50d5\\u3060\\u3051\\u306e\\u77db\\u76fe",
#                                         "date": {"year": 2025},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e0223f704862ed3b1adf3bc6da7",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000485123f704862ed3b1adf3bc6da7",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b27323f704862ed3b1adf3bc6da7",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "-WQNOV_FSF2xEMUksbSNBg",
#                                             "shareUrl": "https://open.spotify.com/album/2H2lOVsdIvonip4PmKqFfW?si=-WQNOV_FSF2xEMUksbSNBg",
#                                         },
#                                         "type": "SINGLE",
#                                     },
#                                     {
#                                         "id": "6cqJocSJ2QmCWHePaVbAUy",
#                                         "uri": "spotify:album:6cqJocSJ2QmCWHePaVbAUy",
#                                         "name": "\\u30d0\\u30fc\\u30b9\\u30c7\\u30a4",
#                                         "date": {"year": 2025},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e0247fd58342bec8142e43dfe82",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000485147fd58342bec8142e43dfe82",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b27347fd58342bec8142e43dfe82",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "IrVQTMlORBa94MsojgJiOA",
#                                             "shareUrl": "https://open.spotify.com/album/6cqJocSJ2QmCWHePaVbAUy?si=IrVQTMlORBa94MsojgJiOA",
#                                         },
#                                         "type": "SINGLE",
#                                     },
#                                     {
#                                         "id": "7DsLGDK8qjjgQTMO8iLHkz",
#                                         "uri": "spotify:album:7DsLGDK8qjjgQTMO8iLHkz",
#                                         "name": "\\u30a2\\u30ca\\u30b6\\u30fc\\u30c0\\u30a4\\u30d0\\u30fc\\u30b7\\u30c6\\u30a3",
#                                         "date": {"year": 2025},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e02ace3691d801acd4c2ede4189",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00004851ace3691d801acd4c2ede4189",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b273ace3691d801acd4c2ede4189",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "kqD3KxLVSFqmkqEap7-EKw",
#                                             "shareUrl": "https://open.spotify.com/album/7DsLGDK8qjjgQTMO8iLHkz?si=kqD3KxLVSFqmkqEap7-EKw",
#                                         },
#                                         "type": "EP",
#                                     },
#                                     {
#                                         "id": "4DLVL2qXMTDgBheakg1Yid",
#                                         "uri": "spotify:album:4DLVL2qXMTDgBheakg1Yid",
#                                         "name": "\\u30e9\\u30b9\\u30c8\\u30cf\\u30f3\\u30c1",
#                                         "date": {"year": 2025},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e02aa8e7c2d8bbe902076a1e53c",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00004851aa8e7c2d8bbe902076a1e53c",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b273aa8e7c2d8bbe902076a1e53c",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "LmEipX5MQjCtsqhryqqv9A",
#                                             "shareUrl": "https://open.spotify.com/album/4DLVL2qXMTDgBheakg1Yid?si=LmEipX5MQjCtsqhryqqv9A",
#                                         },
#                                         "type": "SINGLE",
#                                     },
#                                     {
#                                         "id": "6bnf6dgi1gDKHwg4YeCpbf",
#                                         "uri": "spotify:album:6bnf6dgi1gDKHwg4YeCpbf",
#                                         "name": "UNITY",
#                                         "date": {"year": 2025},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e02a65c28ae22eff345486dda7c",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00004851a65c28ae22eff345486dda7c",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b273a65c28ae22eff345486dda7c",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "e4cJrqgGQfqBxn_IrVtoqw",
#                                             "shareUrl": "https://open.spotify.com/album/6bnf6dgi1gDKHwg4YeCpbf?si=e4cJrqgGQfqBxn_IrVtoqw",
#                                         },
#                                         "type": "SINGLE",
#                                     },
#                                     {
#                                         "id": "4yuDiUMUIfaEItFEyTWcme",
#                                         "uri": "spotify:album:4yuDiUMUIfaEItFEyTWcme",
#                                         "name": "\\u30ef\\u30f3\\u30bf\\u30a4\\u30e0\\u30a8\\u30d4\\u30ed\\u30fc\\u30b0",
#                                         "date": {"year": 2025},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e025a70688e706fb5c9114a243e",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d000048515a70688e706fb5c9114a243e",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b2735a70688e706fb5c9114a243e",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "cKk3lEp1RnimL8A68IbX7A",
#                                             "shareUrl": "https://open.spotify.com/album/4yuDiUMUIfaEItFEyTWcme?si=cKk3lEp1RnimL8A68IbX7A",
#                                         },
#                                         "type": "SINGLE",
#                                     },
#                                     {
#                                         "id": "3cUllXtHAkPuR9VTWz0OGg",
#                                         "uri": "spotify:album:3cUllXtHAkPuR9VTWz0OGg",
#                                         "name": "Lonely Paradox",
#                                         "date": {"year": 2024},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e021643ff34d5e534fd62321a01",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d000048511643ff34d5e534fd62321a01",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b2731643ff34d5e534fd62321a01",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "CvEWuJUIQeaSFjfCgFxsHw",
#                                             "shareUrl": "https://open.spotify.com/album/3cUllXtHAkPuR9VTWz0OGg?si=CvEWuJUIQeaSFjfCgFxsHw",
#                                         },
#                                         "type": "EP",
#                                     },
#                                     {
#                                         "id": "209bUB4Yw8SiUB5F3t252c",
#                                         "uri": "spotify:album:209bUB4Yw8SiUB5F3t252c",
#                                         "name": "Headliner",
#                                         "date": {"year": 2023},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e02be3e73efa86c87f10ab0d436",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00004851be3e73efa86c87f10ab0d436",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b273be3e73efa86c87f10ab0d436",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "cjuEOWVARfuSuAS_f3xvLw",
#                                             "shareUrl": "https://open.spotify.com/album/209bUB4Yw8SiUB5F3t252c?si=cjuEOWVARfuSuAS_f3xvLw",
#                                         },
#                                         "type": "SINGLE",
#                                     },
#                                     {
#                                         "id": "6j3FsUUi3dVuIalzgUCAFz",
#                                         "uri": "spotify:album:6j3FsUUi3dVuIalzgUCAFz",
#                                         "name": "Unbalanced Blend",
#                                         "date": {"year": 2024},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e02fa9382c4da739c6643e5793c",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00004851fa9382c4da739c6643e5793c",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b273fa9382c4da739c6643e5793c",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "DjxVBM9yQb6b7XaB6Ft-6Q",
#                                             "shareUrl": "https://open.spotify.com/album/6j3FsUUi3dVuIalzgUCAFz?si=DjxVBM9yQb6b7XaB6Ft-6Q",
#                                         },
#                                         "type": "SINGLE",
#                                     },
#                                     {
#                                         "id": "6Qlte9o32U238sw3gElTtF",
#                                         "uri": "spotify:album:6Qlte9o32U238sw3gElTtF",
#                                         "name": "Lonely Paradox",
#                                         "date": {"year": 2024},
#                                         "coverArt": {
#                                             "sources": [
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d00001e0220195b5e327bac3024de3c06",
#                                                     "width": 300,
#                                                     "height": 300,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000485120195b5e327bac3024de3c06",
#                                                     "width": 64,
#                                                     "height": 64,
#                                                 },
#                                                 {
#                                                     "url": "https://i.scdn.co/image/ab67616d0000b27320195b5e327bac3024de3c06",
#                                                     "width": 640,
#                                                     "height": 640,
#                                                 },
#                                             ]
#                                         },
#                                         "playability": {
#                                             "playable": true,
#                                             "reason": "PLAYABLE",
#                                         },
#                                         "sharingInfo": {
#                                             "shareId": "W9P7bayWSxe22mYsnGHVow",
#                                             "shareUrl": "https://open.spotify.com/album/6Qlte9o32U238sw3gElTtF?si=W9P7bayWSxe22mYsnGHVow",
#                                         },
#                                         "type": "SINGLE",
#                                     },
#                                 ]
#                             }
#                         }
#                     }
#                 ]
#             },
#         }
#     }
# }
