from typing import TypedDict, Literal

from spotify_dl.model.shared import URL, SpotifyURI


class ImageSource(TypedDict):
    url: URL
    width: int
    height: int


class ExtractedColorRaw(TypedDict):
    hex: str


class ExtractedColors(TypedDict):
    colorRaw: ExtractedColorRaw


class CoverArt(TypedDict):
    extractedColors: ExtractedColors
    sources: list[ImageSource]


class Playability(TypedDict):
    playable: bool
    reason: str | None  # present on trackUnion, absent elsewhere


class Duration(TypedDict):
    totalMilliseconds: int


class ContentRating(TypedDict):
    label: Literal["NONE"]


class DateInfo(TypedDict):
    isoString: str
    precision: Literal["DAY"]
    year: int


class TrackRef(TypedDict):
    uri: SpotifyURI
    trackNumber: int


class TrackRefItem(TypedDict):
    track: TrackRef


class TrackReflist(TypedDict):
    totalCount: int
    items: list[TrackRefItem]


class ArtistProfile(TypedDict):
    name: str


class AvatarImage(TypedDict):
    sources: list[ImageSource]


class ArtistVisuals(TypedDict):
    avatarImage: AvatarImage


class SimpleArtist(TypedDict):
    uri: SpotifyURI
    profile: ArtistProfile


class SimpleArtistItem(TypedDict):
    uri: SpotifyURI
    profile: ArtistProfile


class SimpleArtistlist(TypedDict):
    items: list[SimpleArtistItem]


class AudioPreviewItem(TypedDict):
    url: URL


class AudioPreviewlist(TypedDict):
    items: list[AudioPreviewItem]


class AudioPreviews(TypedDict):
    audioPreviews: AudioPreviewlist


class CopyrightItem(TypedDict):
    text: str
    type: str


class CopyrightField(TypedDict):
    totalCount: int
    items: list[CopyrightItem]


class AlbumOfTrack(TypedDict):
    id: str  # sometimes present
    name: str  # sometimes present
    uri: SpotifyURI  # spotify:album:...
    copyright: CopyrightField
    courtesyLine: str
    type: str
    playability: Playability
    date: DateInfo
    tracks: TrackReflist
    coverArt: CoverArt


class TopTrack(TypedDict):
    artists: SimpleArtistlist
    albumOfTrack: AlbumOfTrack
    playability: Playability
    playcount: str
    previews: AudioPreviews | None
    duration: Duration
    name: str
    uri: SpotifyURI
    id: str


class TopTrackItem(TypedDict):
    track: TopTrack


class TopTracks(TypedDict):
    items: list[TopTrackItem]


class Release(TypedDict):
    name: str
    type: Literal["SINGLE", "EP"]
    uri: SpotifyURI
    playability: Playability
    date: DateInfo
    tracks: TrackReflist
    coverArt: CoverArt


class Releaselist(TypedDict):
    items: list[Release]


class DiscographySingles(TypedDict):
    totalCount: int
    items: list[Releaselist]


class EmptyAlbums(TypedDict):
    totalCount: int
    items: list[None]


class PopularReleasesAlbums(TypedDict):
    items: list[Release]


class Discography(TypedDict):
    singles: DiscographySingles
    albums: EmptyAlbums
    popularReleasesAlbums: PopularReleasesAlbums
    topTracks: TopTracks


class Artist(TypedDict):
    id: str
    uri: SpotifyURI
    visuals: ArtistVisuals
    profile: ArtistProfile
    discography: Discography


class ArtistWithRole(TypedDict):
    role: Literal["MAIN"]
    artist: Artist


class ArtistsWithRoles(TypedDict):
    totalCount: int
    items: list[ArtistWithRole]


class SharingInfo(TypedDict):
    shareUrl: URL  # https://open.spotify.com/track/...
    shareId: str  # YpsqVwxo...


class TrackUnion(TypedDict):
    __typename: Literal["Track"]
    id: str
    uri: SpotifyURI
    name: str
    contentRating: ContentRating
    duration: Duration
    playability: Playability
    trackNumber: int
    playcount: str
    saved: bool
    sharingInfo: SharingInfo
    artistsWithRoles: ArtistsWithRoles
    albumOfTrack: AlbumOfTrack


class Data(TypedDict):
    trackUnion: TrackUnion


class GraphQLResponse(TypedDict):
    data: Data

# {
#   "data": {
#     "trackUnion": {
#       "__typename": "Track",
#       "id": "2VClA4MCgCKVdcjQEDbHyh",
#       "uri": "spotify:track:2VClA4MCgCKVdcjQEDbHyh",
#       "name": "\\u00e3\\u0082\\u00a2\\u00e3\\u0083\\u00b3\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00a9\\u00e3\\u0083\\u00b3\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0096\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u00b3\\u00e3\\u0083\\u0089",
#       "contentRating": {
#         "label": "NONE"
#       },
#       "duration": {
#         "totalMilliseconds": 321613
#       },
#       "playability": {
#         "playable": true,
#         "reason": "PLAYABLE"
#       },
#       "trackNumber": 4,
#       "playcount": "4336773",
#       "saved": false,
#       "sharingInfo": {
#         "shareUrl": "https://open.spotify.com/track/2VClA4MCgCKVdcjQEDbHyh?si=YpsqVwxoTiaP6PGcyIIaVg",
#         "shareId": "YpsqVwxoTiaP6PGcyIIaVg"
#       },
#       "artistsWithRoles": {
#         "totalCount": 1,
#         "items": [
#           {
#             "role": "MAIN",
#             "artist": {
#               "id": "47MRpWYlFaneZAlaXrt9bu",
#               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#               "visuals": {
#                 "avatarImage": {
#                   "sources": [
#                     {
#                       "width": 640,
#                       "height": 640,
#                       "url": "https://i.scdn.co/image/ab6761610000e5eb8eb92d88b11fdb10da14d101"
#                     },
#                     {
#                       "width": 160,
#                       "height": 160,
#                       "url": "https://i.scdn.co/image/ab6761610000f1788eb92d88b11fdb10da14d101"
#                     },
#                     {
#                       "width": 320,
#                       "height": 320,
#                       "url": "https://i.scdn.co/image/ab676161000051748eb92d88b11fdb10da14d101"
#                     }
#                   ]
#                 }
#               },
#               "profile": {
#                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#               },
#               "discography": {
#                 "singles": {
#                   "totalCount": 16,
#                   "items": [
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "\\u00e5\\u0083\\u0095\\u00e3\\u0081\\u00a0\\u00e3\\u0081\\u0091\\u00e3\\u0081\\u00ae\\u00e7\\u009f\\u009b\\u00e7\\u009b\\u00be",
#                             "type": "SINGLE",
#                             "uri": "spotify:album:2H2lOVsdIvonip4PmKqFfW",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2025-12-03T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2025
#                             },
#                             "tracks": {
#                               "totalCount": 1,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:0JbdUM8Bx8ax24Q50EHzB4",
#                                     "trackNumber": 1
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#481800"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e0223f704862ed3b1adf3bc6da7",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000485123f704862ed3b1adf3bc6da7",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b27323f704862ed3b1adf3bc6da7",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0087\\u00e3\\u0082\\u00a4",
#                             "type": "SINGLE",
#                             "uri": "spotify:album:6cqJocSJ2QmCWHePaVbAUy",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2025-11-05T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2025
#                             },
#                             "tracks": {
#                               "totalCount": 1,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:0MUuGBksODh4qIiFK9kWHG",
#                                     "trackNumber": 1
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#E02018"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e0247fd58342bec8142e43dfe82",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000485147fd58342bec8142e43dfe82",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b27347fd58342bec8142e43dfe82",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "\\u00e3\\u0083\\u00a9\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u008f\\u00e3\\u0083\\u00b3\\u00e3\\u0083\\u0081",
#                             "type": "SINGLE",
#                             "uri": "spotify:album:4DLVL2qXMTDgBheakg1Yid",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2025-08-06T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2025
#                             },
#                             "tracks": {
#                               "totalCount": 1,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:4KtMd7F50HwIseHuJpbFt4",
#                                     "trackNumber": 1
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#C86800"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e02aa8e7c2d8bbe902076a1e53c",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00004851aa8e7c2d8bbe902076a1e53c",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b273aa8e7c2d8bbe902076a1e53c",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "UNITY",
#                             "type": "SINGLE",
#                             "uri": "spotify:album:6bnf6dgi1gDKHwg4YeCpbf",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2025-05-07T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2025
#                             },
#                             "tracks": {
#                               "totalCount": 1,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:1ii9uwB3yTRDAyIpWauE5v",
#                                     "trackNumber": 1
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#087038"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e02a65c28ae22eff345486dda7c",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00004851a65c28ae22eff345486dda7c",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b273a65c28ae22eff345486dda7c",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "\\u00e3\\u0082\\u00a2\\u00e3\\u0083\\u008a\\u00e3\\u0082\\u00b6\\u00e3\\u0083\\u00bc\\u00e3\\u0083\\u0080\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b7\\u00e3\\u0083\\u0086\\u00e3\\u0082\\u00a3",
#                             "type": "EP",
#                             "uri": "spotify:album:7DsLGDK8qjjgQTMO8iLHkz",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2025-01-22T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2025
#                             },
#                             "tracks": {
#                               "totalCount": 5,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:3y2f9PVJjgGDxS0qFYIdJe",
#                                     "trackNumber": 1
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:2XNMG5FlJvFSnn6PiHnvjk",
#                                     "trackNumber": 2
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:7djLEVjWkMP0i9kGbE8q3X",
#                                     "trackNumber": 3
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:2VClA4MCgCKVdcjQEDbHyh",
#                                     "trackNumber": 4
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:5WwfaCqpE2sUOCNzOKSn1K",
#                                     "trackNumber": 5
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#C01828"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e02ace3691d801acd4c2ede4189",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00004851ace3691d801acd4c2ede4189",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b273ace3691d801acd4c2ede4189",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "\\u00e3\\u0083\\u00af\\u00e3\\u0083\\u00b3\\u00e3\\u0082\\u00bf\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u00a0\\u00e3\\u0082\\u00a8\\u00e3\\u0083\\u0094\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b0",
#                             "type": "SINGLE",
#                             "uri": "spotify:album:4yuDiUMUIfaEItFEyTWcme",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2025-01-08T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2025
#                             },
#                             "tracks": {
#                               "totalCount": 1,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:5ihqyte3hZEibOp2xFDAkm",
#                                     "trackNumber": 1
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#C01828"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e025a70688e706fb5c9114a243e",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d000048515a70688e706fb5c9114a243e",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b2735a70688e706fb5c9114a243e",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "Unbalanced Blend",
#                             "type": "SINGLE",
#                             "uri": "spotify:album:6j3FsUUi3dVuIalzgUCAFz",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2024-10-09T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2024
#                             },
#                             "tracks": {
#                               "totalCount": 1,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:06pT8zW7GZ90rR2YQy8ebY",
#                                     "trackNumber": 1
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#502018"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e02fa9382c4da739c6643e5793c",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00004851fa9382c4da739c6643e5793c",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b273fa9382c4da739c6643e5793c",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "Syodo",
#                             "type": "SINGLE",
#                             "uri": "spotify:album:3AnRxoaEYEMi2BVavaGDdT",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2024-06-05T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2024
#                             },
#                             "tracks": {
#                               "totalCount": 1,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:58GTF7lC2zbGalY77jEg3y",
#                                     "trackNumber": 1
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#501848"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e0257d5fa18886a7203864d5b88",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000485157d5fa18886a7203864d5b88",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b27357d5fa18886a7203864d5b88",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "Lonely Paradox",
#                             "type": "SINGLE",
#                             "uri": "spotify:album:6Qlte9o32U238sw3gElTtF",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2024-01-10T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2024
#                             },
#                             "tracks": {
#                               "totalCount": 3,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:4dmyhFotHSwyVsKCbvekEU",
#                                     "trackNumber": 1
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:2lTxqpxOhd1dlngjRi944j",
#                                     "trackNumber": 2
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:1GNglKJA1jHncpbyFP9awo",
#                                     "trackNumber": 3
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#58A0D8"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e0220195b5e327bac3024de3c06",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000485120195b5e327bac3024de3c06",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b27320195b5e327bac3024de3c06",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "releases": {
#                         "items": [
#                           {
#                             "name": "Lonely Paradox",
#                             "type": "EP",
#                             "uri": "spotify:album:3cUllXtHAkPuR9VTWz0OGg",
#                             "playability": {
#                               "playable": true
#                             },
#                             "date": {
#                               "isoString": "2024-01-10T00:00:00Z",
#                               "precision": "DAY",
#                               "year": 2024
#                             },
#                             "tracks": {
#                               "totalCount": 6,
#                               "items": [
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:0aN84pd1P3r9eSqZA9pLv9",
#                                     "trackNumber": 1
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:3GH1gOpqx2nH8I1JHq2eM4",
#                                     "trackNumber": 2
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:5DTtGU7ej7VVQbGPqtrYPo",
#                                     "trackNumber": 3
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:3hUBT0r2xUCYB6gZoh4Q1t",
#                                     "trackNumber": 4
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:0jNkjdqED0Aq6fTqvPVdFK",
#                                     "trackNumber": 5
#                                   }
#                                 },
#                                 {
#                                   "track": {
#                                     "uri": "spotify:track:5v7N3hgOSoRCA5UZEwWvtS",
#                                     "trackNumber": 6
#                                   }
#                                 }
#                               ]
#                             },
#                             "coverArt": {
#                               "extractedColors": {
#                                 "colorRaw": {
#                                   "hex": "#58A0D8"
#                                 }
#                               },
#                               "sources": [
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d00001e021643ff34d5e534fd62321a01",
#                                   "width": 300,
#                                   "height": 300
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d000048511643ff34d5e534fd62321a01",
#                                   "width": 64,
#                                   "height": 64
#                                 },
#                                 {
#                                   "url": "https://i.scdn.co/image/ab67616d0000b2731643ff34d5e534fd62321a01",
#                                   "width": 640,
#                                   "height": 640
#                                 }
#                               ]
#                             }
#                           }
#                         ]
#                       }
#                     }
#                   ]
#                 },
#                 "albums": {
#                   "totalCount": 0,
#                   "items": []
#                 },
#                 "popularReleasesAlbums": {
#                   "items": [
#                     {
#                       "name": "\\u00e5\\u0083\\u0095\\u00e3\\u0081\\u00a0\\u00e3\\u0081\\u0091\\u00e3\\u0081\\u00ae\\u00e7\\u009f\\u009b\\u00e7\\u009b\\u00be",
#                       "type": "SINGLE",
#                       "uri": "spotify:album:2H2lOVsdIvonip4PmKqFfW",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2025-12-03T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2025
#                       },
#                       "tracks": {
#                         "totalCount": 1,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:0JbdUM8Bx8ax24Q50EHzB4",
#                               "trackNumber": 1
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#481800"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e0223f704862ed3b1adf3bc6da7",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000485123f704862ed3b1adf3bc6da7",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b27323f704862ed3b1adf3bc6da7",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0087\\u00e3\\u0082\\u00a4",
#                       "type": "SINGLE",
#                       "uri": "spotify:album:6cqJocSJ2QmCWHePaVbAUy",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2025-11-05T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2025
#                       },
#                       "tracks": {
#                         "totalCount": 1,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:0MUuGBksODh4qIiFK9kWHG",
#                               "trackNumber": 1
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#E02018"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e0247fd58342bec8142e43dfe82",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000485147fd58342bec8142e43dfe82",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b27347fd58342bec8142e43dfe82",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "\\u00e3\\u0082\\u00a2\\u00e3\\u0083\\u008a\\u00e3\\u0082\\u00b6\\u00e3\\u0083\\u00bc\\u00e3\\u0083\\u0080\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b7\\u00e3\\u0083\\u0086\\u00e3\\u0082\\u00a3",
#                       "type": "EP",
#                       "uri": "spotify:album:7DsLGDK8qjjgQTMO8iLHkz",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2025-01-22T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2025
#                       },
#                       "tracks": {
#                         "totalCount": 5,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:3y2f9PVJjgGDxS0qFYIdJe",
#                               "trackNumber": 1
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:2XNMG5FlJvFSnn6PiHnvjk",
#                               "trackNumber": 2
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:7djLEVjWkMP0i9kGbE8q3X",
#                               "trackNumber": 3
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:2VClA4MCgCKVdcjQEDbHyh",
#                               "trackNumber": 4
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:5WwfaCqpE2sUOCNzOKSn1K",
#                               "trackNumber": 5
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#C01828"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e02ace3691d801acd4c2ede4189",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00004851ace3691d801acd4c2ede4189",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b273ace3691d801acd4c2ede4189",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "\\u00e3\\u0083\\u00a9\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u008f\\u00e3\\u0083\\u00b3\\u00e3\\u0083\\u0081",
#                       "type": "SINGLE",
#                       "uri": "spotify:album:4DLVL2qXMTDgBheakg1Yid",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2025-08-06T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2025
#                       },
#                       "tracks": {
#                         "totalCount": 1,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:4KtMd7F50HwIseHuJpbFt4",
#                               "trackNumber": 1
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#C86800"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e02aa8e7c2d8bbe902076a1e53c",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00004851aa8e7c2d8bbe902076a1e53c",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b273aa8e7c2d8bbe902076a1e53c",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "UNITY",
#                       "type": "SINGLE",
#                       "uri": "spotify:album:6bnf6dgi1gDKHwg4YeCpbf",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2025-05-07T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2025
#                       },
#                       "tracks": {
#                         "totalCount": 1,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:1ii9uwB3yTRDAyIpWauE5v",
#                               "trackNumber": 1
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#087038"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e02a65c28ae22eff345486dda7c",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00004851a65c28ae22eff345486dda7c",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b273a65c28ae22eff345486dda7c",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "\\u00e3\\u0083\\u00af\\u00e3\\u0083\\u00b3\\u00e3\\u0082\\u00bf\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u00a0\\u00e3\\u0082\\u00a8\\u00e3\\u0083\\u0094\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b0",
#                       "type": "SINGLE",
#                       "uri": "spotify:album:4yuDiUMUIfaEItFEyTWcme",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2025-01-08T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2025
#                       },
#                       "tracks": {
#                         "totalCount": 1,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:5ihqyte3hZEibOp2xFDAkm",
#                               "trackNumber": 1
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#C01828"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e025a70688e706fb5c9114a243e",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d000048515a70688e706fb5c9114a243e",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b2735a70688e706fb5c9114a243e",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "Lonely Paradox",
#                       "type": "EP",
#                       "uri": "spotify:album:3cUllXtHAkPuR9VTWz0OGg",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2024-01-10T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2024
#                       },
#                       "tracks": {
#                         "totalCount": 6,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:0aN84pd1P3r9eSqZA9pLv9",
#                               "trackNumber": 1
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:3GH1gOpqx2nH8I1JHq2eM4",
#                               "trackNumber": 2
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:5DTtGU7ej7VVQbGPqtrYPo",
#                               "trackNumber": 3
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:3hUBT0r2xUCYB6gZoh4Q1t",
#                               "trackNumber": 4
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:0jNkjdqED0Aq6fTqvPVdFK",
#                               "trackNumber": 5
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:5v7N3hgOSoRCA5UZEwWvtS",
#                               "trackNumber": 6
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#58A0D8"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e021643ff34d5e534fd62321a01",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d000048511643ff34d5e534fd62321a01",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b2731643ff34d5e534fd62321a01",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "Headliner",
#                       "type": "SINGLE",
#                       "uri": "spotify:album:209bUB4Yw8SiUB5F3t252c",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2023-08-16T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2023
#                       },
#                       "tracks": {
#                         "totalCount": 1,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:5wYXXFzzelTMEbVOGoZ3Q0",
#                               "trackNumber": 1
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#406828"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e02be3e73efa86c87f10ab0d436",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00004851be3e73efa86c87f10ab0d436",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b273be3e73efa86c87f10ab0d436",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "Unbalanced Blend",
#                       "type": "SINGLE",
#                       "uri": "spotify:album:6j3FsUUi3dVuIalzgUCAFz",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2024-10-09T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2024
#                       },
#                       "tracks": {
#                         "totalCount": 1,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:06pT8zW7GZ90rR2YQy8ebY",
#                               "trackNumber": 1
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#502018"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e02fa9382c4da739c6643e5793c",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00004851fa9382c4da739c6643e5793c",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b273fa9382c4da739c6643e5793c",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     },
#                     {
#                       "name": "Lonely Paradox",
#                       "type": "SINGLE",
#                       "uri": "spotify:album:6Qlte9o32U238sw3gElTtF",
#                       "playability": {
#                         "playable": true
#                       },
#                       "date": {
#                         "isoString": "2024-01-10T00:00:00Z",
#                         "precision": "DAY",
#                         "year": 2024
#                       },
#                       "tracks": {
#                         "totalCount": 3,
#                         "items": [
#                           {
#                             "track": {
#                               "uri": "spotify:track:4dmyhFotHSwyVsKCbvekEU",
#                               "trackNumber": 1
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:2lTxqpxOhd1dlngjRi944j",
#                               "trackNumber": 2
#                             }
#                           },
#                           {
#                             "track": {
#                               "uri": "spotify:track:1GNglKJA1jHncpbyFP9awo",
#                               "trackNumber": 3
#                             }
#                           }
#                         ]
#                       },
#                       "coverArt": {
#                         "extractedColors": {
#                           "colorRaw": {
#                             "hex": "#58A0D8"
#                           }
#                         },
#                         "sources": [
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d00001e0220195b5e327bac3024de3c06",
#                             "width": 300,
#                             "height": 300
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000485120195b5e327bac3024de3c06",
#                             "width": 64,
#                             "height": 64
#                           },
#                           {
#                             "url": "https://i.scdn.co/image/ab67616d0000b27320195b5e327bac3024de3c06",
#                             "width": 640,
#                             "height": 640
#                           }
#                         ]
#                       }
#                     }
#                   ]
#                 },
#                 "topTracks": {
#                   "items": [
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "Headliner",
#                           "uri": "spotify:album:209bUB4Yw8SiUB5F3t252c",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#406828"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e02be3e73efa86c87f10ab0d436",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00004851be3e73efa86c87f10ab0d436",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b273be3e73efa86c87f10ab0d436",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "5267707",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/311e0727a5450553796e2383d504285ffef7fc16"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 234566
#                         },
#                         "name": "Headliner",
#                         "uri": "spotify:track:5wYXXFzzelTMEbVOGoZ3Q0",
#                         "id": "5wYXXFzzelTMEbVOGoZ3Q0"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "Unbalanced Blend",
#                           "uri": "spotify:album:6j3FsUUi3dVuIalzgUCAFz",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#502018"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e02fa9382c4da739c6643e5793c",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00004851fa9382c4da739c6643e5793c",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b273fa9382c4da739c6643e5793c",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "4336773",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/019ae548d652f81ce31317dc97b7298e1cb3b0fe"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 319623
#                         },
#                         "name": "Unbalanced Blend",
#                         "uri": "spotify:track:06pT8zW7GZ90rR2YQy8ebY",
#                         "id": "06pT8zW7GZ90rR2YQy8ebY"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0087\\u00e3\\u0082\\u00a4",
#                           "uri": "spotify:album:6cqJocSJ2QmCWHePaVbAUy",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#E02018"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e0247fd58342bec8142e43dfe82",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000485147fd58342bec8142e43dfe82",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b27347fd58342bec8142e43dfe82",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "405901",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/9e8cbe5a900da7071a163381d662b2be4ff3785d"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 324484
#                         },
#                         "name": "\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0087\\u00e3\\u0082\\u00a4",
#                         "uri": "spotify:track:0MUuGBksODh4qIiFK9kWHG",
#                         "id": "0MUuGBksODh4qIiFK9kWHG"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "\\u00e5\\u0083\\u0095\\u00e3\\u0081\\u00a0\\u00e3\\u0081\\u0091\\u00e3\\u0081\\u00ae\\u00e7\\u009f\\u009b\\u00e7\\u009b\\u00be",
#                           "uri": "spotify:album:2H2lOVsdIvonip4PmKqFfW",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#481800"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e0223f704862ed3b1adf3bc6da7",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000485123f704862ed3b1adf3bc6da7",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b27323f704862ed3b1adf3bc6da7",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "181881",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/a1c2fbb25c7622a0de6b16d4f820a2e578e38da4"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 254104
#                         },
#                         "name": "\\u00e5\\u0083\\u0095\\u00e3\\u0081\\u00a0\\u00e3\\u0081\\u0091\\u00e3\\u0081\\u00ae\\u00e7\\u009f\\u009b\\u00e7\\u009b\\u00be",
#                         "uri": "spotify:track:0JbdUM8Bx8ax24Q50EHzB4",
#                         "id": "0JbdUM8Bx8ax24Q50EHzB4"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "\\u00e3\\u0083\\u00a9\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u008f\\u00e3\\u0083\\u00b3\\u00e3\\u0083\\u0081",
#                           "uri": "spotify:album:4DLVL2qXMTDgBheakg1Yid",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#C86800"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e02aa8e7c2d8bbe902076a1e53c",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00004851aa8e7c2d8bbe902076a1e53c",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b273aa8e7c2d8bbe902076a1e53c",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "1272258",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/e7048c8c212afdfd85e0d14adc22732be138f805"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 250453
#                         },
#                         "name": "\\u00e3\\u0083\\u00a9\\u00e3\\u0082\\u00b9\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u008f\\u00e3\\u0083\\u00b3\\u00e3\\u0083\\u0081",
#                         "uri": "spotify:track:4KtMd7F50HwIseHuJpbFt4",
#                         "id": "4KtMd7F50HwIseHuJpbFt4"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "UNITY",
#                           "uri": "spotify:album:6bnf6dgi1gDKHwg4YeCpbf",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#087038"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e02a65c28ae22eff345486dda7c",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00004851a65c28ae22eff345486dda7c",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b273a65c28ae22eff345486dda7c",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "1495058",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/fa93c45244af84cd3345e1445080daefc1804f76"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 278678
#                         },
#                         "name": "UNITY",
#                         "uri": "spotify:track:1ii9uwB3yTRDAyIpWauE5v",
#                         "id": "1ii9uwB3yTRDAyIpWauE5v"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "\\u00e3\\u0083\\u00af\\u00e3\\u0083\\u00b3\\u00e3\\u0082\\u00bf\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u00a0\\u00e3\\u0082\\u00a8\\u00e3\\u0083\\u0094\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b0",
#                           "uri": "spotify:album:4yuDiUMUIfaEItFEyTWcme",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#C01828"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e025a70688e706fb5c9114a243e",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d000048515a70688e706fb5c9114a243e",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b2735a70688e706fb5c9114a243e",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "1128272",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/f125c2fb9bf36ac3c858b22ea17f8bf1b78df90a"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 214222
#                         },
#                         "name": "\\u00e3\\u0083\\u00af\\u00e3\\u0083\\u00b3\\u00e3\\u0082\\u00bf\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u00a0\\u00e3\\u0082\\u00a8\\u00e3\\u0083\\u0094\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b0",
#                         "uri": "spotify:track:5ihqyte3hZEibOp2xFDAkm",
#                         "id": "5ihqyte3hZEibOp2xFDAkm"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "Lonely Paradox",
#                           "uri": "spotify:album:3cUllXtHAkPuR9VTWz0OGg",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#58A0D8"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e021643ff34d5e534fd62321a01",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d000048511643ff34d5e534fd62321a01",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b2731643ff34d5e534fd62321a01",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "1832919",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/d59d4af9a10dbd5d1676cfc3d7715ebb4343c724"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 248098
#                         },
#                         "name": "Tomodachi",
#                         "uri": "spotify:track:0aN84pd1P3r9eSqZA9pLv9",
#                         "id": "0aN84pd1P3r9eSqZA9pLv9"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "\\u00e3\\u0082\\u00a2\\u00e3\\u0083\\u008a\\u00e3\\u0082\\u00b6\\u00e3\\u0083\\u00bc\\u00e3\\u0083\\u0080\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b7\\u00e3\\u0083\\u0086\\u00e3\\u0082\\u00a3",
#                           "uri": "spotify:album:7DsLGDK8qjjgQTMO8iLHkz",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#C01828"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e02ace3691d801acd4c2ede4189",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00004851ace3691d801acd4c2ede4189",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b273ace3691d801acd4c2ede4189",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "1467310",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/a8a3e75c720bc6133f63814e7586428ed5e11bf6"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 227360
#                         },
#                         "name": "\\u00e3\\u0082\\u00ab\\u00e3\\u0083\\u0086\\u00e3\\u0082\\u00b4\\u00e3\\u0083\\u00a9\\u00e3\\u0082\\u00a4\\u00e3\\u0082\\u00ba",
#                         "uri": "spotify:track:2XNMG5FlJvFSnn6PiHnvjk",
#                         "id": "2XNMG5FlJvFSnn6PiHnvjk"
#                       }
#                     },
#                     {
#                       "track": {
#                         "artists": {
#                           "items": [
#                             {
#                               "uri": "spotify:artist:47MRpWYlFaneZAlaXrt9bu",
#                               "profile": {
#                                 "name": "\\u00e3\\u0083\\u00ac\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00aa\\u00e3\\u0083\\u00ad\\u00e3\\u0083\\u00b3"
#                               }
#                             }
#                           ]
#                         },
#                         "albumOfTrack": {
#                           "name": "Shin'ya 6-ji",
#                           "uri": "spotify:album:0fQOqoTxovUB2hIVjGgGNK",
#                           "coverArt": {
#                             "extractedColors": {
#                               "colorRaw": {
#                                 "hex": "#D898A8"
#                               }
#                             },
#                             "sources": [
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d00001e028ab50058078c72fb0ae4457f",
#                                 "width": 300,
#                                 "height": 300
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d000048518ab50058078c72fb0ae4457f",
#                                 "width": 64,
#                                 "height": 64
#                               },
#                               {
#                                 "url": "https://i.scdn.co/image/ab67616d0000b2738ab50058078c72fb0ae4457f",
#                                 "width": 640,
#                                 "height": 640
#                               }
#                             ]
#                           }
#                         },
#                         "playability": {
#                           "playable": true
#                         },
#                         "playcount": "1575624",
#                         "previews": {
#                           "audioPreviews": {
#                             "items": [
#                               {
#                                 "url": "https://p.scdn.co/mp3-preview/abe402d58e578682af34830fc71e147ae3f2ec0e"
#                               }
#                             ]
#                           }
#                         },
#                         "duration": {
#                           "totalMilliseconds": 279928
#                         },
#                         "name": "Shin'ya 6-ji",
#                         "uri": "spotify:track:4OCIpuigIlufkPyZ9uRlcY",
#                         "id": "4OCIpuigIlufkPyZ9uRlcY"
#                       }
#                     }
#                   ]
#                 }
#               }
#             }
#           }
#         ]
#       },
#       "albumOfTrack": {
#         "id": "7DsLGDK8qjjgQTMO8iLHkz",
#         "copyright": {
#           "totalCount": 2,
#           "items": [
#             {
#               "text": "\\u00c2\\u00a9 2025 RETRORIRON / Lastrum Music Entertainment",
#               "type": "C"
#             },
#             {
#               "text": "\\u00e2\\u0084\\u0097 2025 RETRORIRON / Lastrum Music Entertainment",
#               "type": "P"
#             }
#           ]
#         },
#         "courtesyLine": "",
#         "name": "\\u00e3\\u0082\\u00a2\\u00e3\\u0083\\u008a\\u00e3\\u0082\\u00b6\\u00e3\\u0083\\u00bc\\u00e3\\u0083\\u0080\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u0090\\u00e3\\u0083\\u00bc\\u00e3\\u0082\\u00b7\\u00e3\\u0083\\u0086\\u00e3\\u0082\\u00a3",
#         "type": "EP",
#         "uri": "spotify:album:7DsLGDK8qjjgQTMO8iLHkz",
#         "playability": {
#           "playable": true
#         },
#         "date": {
#           "isoString": "2025-01-22T00:00:00Z",
#           "precision": "DAY",
#           "year": 2025
#         },
#         "tracks": {
#           "totalCount": 5,
#           "items": [
#             {
#               "track": {
#                 "uri": "spotify:track:3y2f9PVJjgGDxS0qFYIdJe",
#                 "trackNumber": 1
#               }
#             },
#             {
#               "track": {
#                 "uri": "spotify:track:2XNMG5FlJvFSnn6PiHnvjk",
#                 "trackNumber": 2
#               }
#             },
#             {
#               "track": {
#                 "uri": "spotify:track:7djLEVjWkMP0i9kGbE8q3X",
#                 "trackNumber": 3
#               }
#             },
#             {
#               "track": {
#                 "uri": "spotify:track:2VClA4MCgCKVdcjQEDbHyh",
#                 "trackNumber": 4
#               }
#             },
#             {
#               "track": {
#                 "uri": "spotify:track:5WwfaCqpE2sUOCNzOKSn1K",
#                 "trackNumber": 5
#               }
#             }
#           ]
#         },
#         "coverArt": {
#           "extractedColors": {
#             "colorRaw": {
#               "hex": "#C01828"
#             }
#           },
#           "sources": [
#             {
#               "url": "https://i.scdn.co/image/ab67616d00001e02ace3691d801acd4c2ede4189",
#               "width": 300,
#               "height": 300
#             },
#             {
#               "url": "https://i.scdn.co/image/ab67616d00004851ace3691d801acd4c2ede4189",
#               "width": 64,
#               "height": 64
#             },
#             {
#               "url": "https://i.scdn.co/image/ab67616d0000b273ace3691d801acd4c2ede4189",
#               "width": 640,
#               "height": 640
#             }
#           ]
#         }
#       }
#     }
#   }
# }
