from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Artist(_message.Message):
    __slots__ = ("gid", "name", "popularity", "top_track", "album_group", "single_group", "compilation_group", "appears_on_group", "external_id", "portrait", "biography", "activity_period", "restriction", "related", "is_portrait_album_cover", "portrait_group", "sale_period", "availability")
    GID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    POPULARITY_FIELD_NUMBER: _ClassVar[int]
    TOP_TRACK_FIELD_NUMBER: _ClassVar[int]
    ALBUM_GROUP_FIELD_NUMBER: _ClassVar[int]
    SINGLE_GROUP_FIELD_NUMBER: _ClassVar[int]
    COMPILATION_GROUP_FIELD_NUMBER: _ClassVar[int]
    APPEARS_ON_GROUP_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    PORTRAIT_FIELD_NUMBER: _ClassVar[int]
    BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_PERIOD_FIELD_NUMBER: _ClassVar[int]
    RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    RELATED_FIELD_NUMBER: _ClassVar[int]
    IS_PORTRAIT_ALBUM_COVER_FIELD_NUMBER: _ClassVar[int]
    PORTRAIT_GROUP_FIELD_NUMBER: _ClassVar[int]
    SALE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    gid: bytes
    name: str
    popularity: int
    top_track: _containers.RepeatedCompositeFieldContainer[TopTracks]
    album_group: _containers.RepeatedCompositeFieldContainer[AlbumGroup]
    single_group: _containers.RepeatedCompositeFieldContainer[AlbumGroup]
    compilation_group: _containers.RepeatedCompositeFieldContainer[AlbumGroup]
    appears_on_group: _containers.RepeatedCompositeFieldContainer[AlbumGroup]
    external_id: _containers.RepeatedCompositeFieldContainer[ExternalId]
    portrait: _containers.RepeatedCompositeFieldContainer[Image]
    biography: _containers.RepeatedCompositeFieldContainer[Biography]
    activity_period: _containers.RepeatedCompositeFieldContainer[ActivityPeriod]
    restriction: _containers.RepeatedCompositeFieldContainer[Restriction]
    related: _containers.RepeatedCompositeFieldContainer[Artist]
    is_portrait_album_cover: bool
    portrait_group: ImageGroup
    sale_period: _containers.RepeatedCompositeFieldContainer[SalePeriod]
    availability: _containers.RepeatedCompositeFieldContainer[Availability]
    def __init__(self, gid: _Optional[bytes] = ..., name: _Optional[str] = ..., popularity: _Optional[int] = ..., top_track: _Optional[_Iterable[_Union[TopTracks, _Mapping]]] = ..., album_group: _Optional[_Iterable[_Union[AlbumGroup, _Mapping]]] = ..., single_group: _Optional[_Iterable[_Union[AlbumGroup, _Mapping]]] = ..., compilation_group: _Optional[_Iterable[_Union[AlbumGroup, _Mapping]]] = ..., appears_on_group: _Optional[_Iterable[_Union[AlbumGroup, _Mapping]]] = ..., external_id: _Optional[_Iterable[_Union[ExternalId, _Mapping]]] = ..., portrait: _Optional[_Iterable[_Union[Image, _Mapping]]] = ..., biography: _Optional[_Iterable[_Union[Biography, _Mapping]]] = ..., activity_period: _Optional[_Iterable[_Union[ActivityPeriod, _Mapping]]] = ..., restriction: _Optional[_Iterable[_Union[Restriction, _Mapping]]] = ..., related: _Optional[_Iterable[_Union[Artist, _Mapping]]] = ..., is_portrait_album_cover: bool = ..., portrait_group: _Optional[_Union[ImageGroup, _Mapping]] = ..., sale_period: _Optional[_Iterable[_Union[SalePeriod, _Mapping]]] = ..., availability: _Optional[_Iterable[_Union[Availability, _Mapping]]] = ...) -> None: ...

class Album(_message.Message):
    __slots__ = ("gid", "name", "artist", "type", "label", "date", "popularity", "cover", "external_id", "disc", "review", "copyright", "restriction", "related", "sale_period", "cover_group", "original_title", "version_title", "type_str", "availability")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ALBUM: _ClassVar[Album.Type]
        SINGLE: _ClassVar[Album.Type]
        COMPILATION: _ClassVar[Album.Type]
        EP: _ClassVar[Album.Type]
        AUDIOBOOK: _ClassVar[Album.Type]
        PODCAST: _ClassVar[Album.Type]
    ALBUM: Album.Type
    SINGLE: Album.Type
    COMPILATION: Album.Type
    EP: Album.Type
    AUDIOBOOK: Album.Type
    PODCAST: Album.Type
    GID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARTIST_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    POPULARITY_FIELD_NUMBER: _ClassVar[int]
    COVER_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    DISC_FIELD_NUMBER: _ClassVar[int]
    REVIEW_FIELD_NUMBER: _ClassVar[int]
    COPYRIGHT_FIELD_NUMBER: _ClassVar[int]
    RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    RELATED_FIELD_NUMBER: _ClassVar[int]
    SALE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    COVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_TITLE_FIELD_NUMBER: _ClassVar[int]
    VERSION_TITLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_STR_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    gid: bytes
    name: str
    artist: _containers.RepeatedCompositeFieldContainer[Artist]
    type: Album.Type
    label: str
    date: Date
    popularity: int
    cover: _containers.RepeatedCompositeFieldContainer[Image]
    external_id: _containers.RepeatedCompositeFieldContainer[ExternalId]
    disc: _containers.RepeatedCompositeFieldContainer[Disc]
    review: _containers.RepeatedScalarFieldContainer[str]
    copyright: _containers.RepeatedCompositeFieldContainer[Copyright]
    restriction: _containers.RepeatedCompositeFieldContainer[Restriction]
    related: _containers.RepeatedCompositeFieldContainer[Album]
    sale_period: _containers.RepeatedCompositeFieldContainer[SalePeriod]
    cover_group: ImageGroup
    original_title: str
    version_title: str
    type_str: str
    availability: _containers.RepeatedCompositeFieldContainer[Availability]
    def __init__(self, gid: _Optional[bytes] = ..., name: _Optional[str] = ..., artist: _Optional[_Iterable[_Union[Artist, _Mapping]]] = ..., type: _Optional[_Union[Album.Type, str]] = ..., label: _Optional[str] = ..., date: _Optional[_Union[Date, _Mapping]] = ..., popularity: _Optional[int] = ..., cover: _Optional[_Iterable[_Union[Image, _Mapping]]] = ..., external_id: _Optional[_Iterable[_Union[ExternalId, _Mapping]]] = ..., disc: _Optional[_Iterable[_Union[Disc, _Mapping]]] = ..., review: _Optional[_Iterable[str]] = ..., copyright: _Optional[_Iterable[_Union[Copyright, _Mapping]]] = ..., restriction: _Optional[_Iterable[_Union[Restriction, _Mapping]]] = ..., related: _Optional[_Iterable[_Union[Album, _Mapping]]] = ..., sale_period: _Optional[_Iterable[_Union[SalePeriod, _Mapping]]] = ..., cover_group: _Optional[_Union[ImageGroup, _Mapping]] = ..., original_title: _Optional[str] = ..., version_title: _Optional[str] = ..., type_str: _Optional[str] = ..., availability: _Optional[_Iterable[_Union[Availability, _Mapping]]] = ...) -> None: ...

class Track(_message.Message):
    __slots__ = ("gid", "name", "album", "artist", "number", "disc_number", "duration", "popularity", "explicit", "external_id", "restriction", "file", "alternative", "sale_period", "preview", "tags", "earliest_live_timestamp", "has_lyrics", "availability", "licensor", "language_of_performance", "original_audio", "content_rating", "original_title", "version_title", "artist_with_role", "canonical_uri", "original_video")
    GID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALBUM_FIELD_NUMBER: _ClassVar[int]
    ARTIST_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    DISC_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    POPULARITY_FIELD_NUMBER: _ClassVar[int]
    EXPLICIT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    ALTERNATIVE_FIELD_NUMBER: _ClassVar[int]
    SALE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    EARLIEST_LIVE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HAS_LYRICS_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    LICENSOR_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_OF_PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_AUDIO_FIELD_NUMBER: _ClassVar[int]
    CONTENT_RATING_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_TITLE_FIELD_NUMBER: _ClassVar[int]
    VERSION_TITLE_FIELD_NUMBER: _ClassVar[int]
    ARTIST_WITH_ROLE_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_URI_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_VIDEO_FIELD_NUMBER: _ClassVar[int]
    gid: bytes
    name: str
    album: Album
    artist: _containers.RepeatedCompositeFieldContainer[Artist]
    number: int
    disc_number: int
    duration: int
    popularity: int
    explicit: bool
    external_id: _containers.RepeatedCompositeFieldContainer[ExternalId]
    restriction: _containers.RepeatedCompositeFieldContainer[Restriction]
    file: _containers.RepeatedCompositeFieldContainer[AudioFile]
    alternative: _containers.RepeatedCompositeFieldContainer[Track]
    sale_period: _containers.RepeatedCompositeFieldContainer[SalePeriod]
    preview: _containers.RepeatedCompositeFieldContainer[AudioFile]
    tags: _containers.RepeatedScalarFieldContainer[str]
    earliest_live_timestamp: int
    has_lyrics: bool
    availability: _containers.RepeatedCompositeFieldContainer[Availability]
    licensor: Licensor
    language_of_performance: _containers.RepeatedScalarFieldContainer[str]
    original_audio: Audio
    content_rating: _containers.RepeatedCompositeFieldContainer[ContentRating]
    original_title: str
    version_title: str
    artist_with_role: _containers.RepeatedCompositeFieldContainer[ArtistWithRole]
    canonical_uri: str
    original_video: _containers.RepeatedCompositeFieldContainer[Video]
    def __init__(self, gid: _Optional[bytes] = ..., name: _Optional[str] = ..., album: _Optional[_Union[Album, _Mapping]] = ..., artist: _Optional[_Iterable[_Union[Artist, _Mapping]]] = ..., number: _Optional[int] = ..., disc_number: _Optional[int] = ..., duration: _Optional[int] = ..., popularity: _Optional[int] = ..., explicit: bool = ..., external_id: _Optional[_Iterable[_Union[ExternalId, _Mapping]]] = ..., restriction: _Optional[_Iterable[_Union[Restriction, _Mapping]]] = ..., file: _Optional[_Iterable[_Union[AudioFile, _Mapping]]] = ..., alternative: _Optional[_Iterable[_Union[Track, _Mapping]]] = ..., sale_period: _Optional[_Iterable[_Union[SalePeriod, _Mapping]]] = ..., preview: _Optional[_Iterable[_Union[AudioFile, _Mapping]]] = ..., tags: _Optional[_Iterable[str]] = ..., earliest_live_timestamp: _Optional[int] = ..., has_lyrics: bool = ..., availability: _Optional[_Iterable[_Union[Availability, _Mapping]]] = ..., licensor: _Optional[_Union[Licensor, _Mapping]] = ..., language_of_performance: _Optional[_Iterable[str]] = ..., original_audio: _Optional[_Union[Audio, _Mapping]] = ..., content_rating: _Optional[_Iterable[_Union[ContentRating, _Mapping]]] = ..., original_title: _Optional[str] = ..., version_title: _Optional[str] = ..., artist_with_role: _Optional[_Iterable[_Union[ArtistWithRole, _Mapping]]] = ..., canonical_uri: _Optional[str] = ..., original_video: _Optional[_Iterable[_Union[Video, _Mapping]]] = ...) -> None: ...

class ArtistWithRole(_message.Message):
    __slots__ = ("artist_gid", "artist_name", "role")
    class ArtistRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ARTIST_ROLE_UNKNOWN: _ClassVar[ArtistWithRole.ArtistRole]
        ARTIST_ROLE_MAIN_ARTIST: _ClassVar[ArtistWithRole.ArtistRole]
        ARTIST_ROLE_FEATURED_ARTIST: _ClassVar[ArtistWithRole.ArtistRole]
        ARTIST_ROLE_REMIXER: _ClassVar[ArtistWithRole.ArtistRole]
        ARTIST_ROLE_ACTOR: _ClassVar[ArtistWithRole.ArtistRole]
        ARTIST_ROLE_COMPOSER: _ClassVar[ArtistWithRole.ArtistRole]
        ARTIST_ROLE_CONDUCTOR: _ClassVar[ArtistWithRole.ArtistRole]
        ARTIST_ROLE_ORCHESTRA: _ClassVar[ArtistWithRole.ArtistRole]
    ARTIST_ROLE_UNKNOWN: ArtistWithRole.ArtistRole
    ARTIST_ROLE_MAIN_ARTIST: ArtistWithRole.ArtistRole
    ARTIST_ROLE_FEATURED_ARTIST: ArtistWithRole.ArtistRole
    ARTIST_ROLE_REMIXER: ArtistWithRole.ArtistRole
    ARTIST_ROLE_ACTOR: ArtistWithRole.ArtistRole
    ARTIST_ROLE_COMPOSER: ArtistWithRole.ArtistRole
    ARTIST_ROLE_CONDUCTOR: ArtistWithRole.ArtistRole
    ARTIST_ROLE_ORCHESTRA: ArtistWithRole.ArtistRole
    ARTIST_GID_FIELD_NUMBER: _ClassVar[int]
    ARTIST_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    artist_gid: bytes
    artist_name: str
    role: ArtistWithRole.ArtistRole
    def __init__(self, artist_gid: _Optional[bytes] = ..., artist_name: _Optional[str] = ..., role: _Optional[_Union[ArtistWithRole.ArtistRole, str]] = ...) -> None: ...

class Show(_message.Message):
    __slots__ = ("gid", "name", "description", "deprecated_popularity", "publisher", "language", "explicit", "cover_image", "episode", "copyright", "restriction", "keyword", "media_type", "consumption_order", "availability", "trailer_uri", "music_and_talk", "is_audiobook", "is_creator_channel")
    class MediaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MIXED: _ClassVar[Show.MediaType]
        AUDIO: _ClassVar[Show.MediaType]
        VIDEO: _ClassVar[Show.MediaType]
    MIXED: Show.MediaType
    AUDIO: Show.MediaType
    VIDEO: Show.MediaType
    class ConsumptionOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SEQUENTIAL: _ClassVar[Show.ConsumptionOrder]
        EPISODIC: _ClassVar[Show.ConsumptionOrder]
        RECENT: _ClassVar[Show.ConsumptionOrder]
    SEQUENTIAL: Show.ConsumptionOrder
    EPISODIC: Show.ConsumptionOrder
    RECENT: Show.ConsumptionOrder
    GID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_POPULARITY_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    EXPLICIT_FIELD_NUMBER: _ClassVar[int]
    COVER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    EPISODE_FIELD_NUMBER: _ClassVar[int]
    COPYRIGHT_FIELD_NUMBER: _ClassVar[int]
    RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    MEDIA_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_ORDER_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    TRAILER_URI_FIELD_NUMBER: _ClassVar[int]
    MUSIC_AND_TALK_FIELD_NUMBER: _ClassVar[int]
    IS_AUDIOBOOK_FIELD_NUMBER: _ClassVar[int]
    IS_CREATOR_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    gid: bytes
    name: str
    description: str
    deprecated_popularity: int
    publisher: str
    language: str
    explicit: bool
    cover_image: ImageGroup
    episode: _containers.RepeatedCompositeFieldContainer[Episode]
    copyright: _containers.RepeatedCompositeFieldContainer[Copyright]
    restriction: _containers.RepeatedCompositeFieldContainer[Restriction]
    keyword: _containers.RepeatedScalarFieldContainer[str]
    media_type: Show.MediaType
    consumption_order: Show.ConsumptionOrder
    availability: _containers.RepeatedCompositeFieldContainer[Availability]
    trailer_uri: str
    music_and_talk: bool
    is_audiobook: bool
    is_creator_channel: bool
    def __init__(self, gid: _Optional[bytes] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., deprecated_popularity: _Optional[int] = ..., publisher: _Optional[str] = ..., language: _Optional[str] = ..., explicit: bool = ..., cover_image: _Optional[_Union[ImageGroup, _Mapping]] = ..., episode: _Optional[_Iterable[_Union[Episode, _Mapping]]] = ..., copyright: _Optional[_Iterable[_Union[Copyright, _Mapping]]] = ..., restriction: _Optional[_Iterable[_Union[Restriction, _Mapping]]] = ..., keyword: _Optional[_Iterable[str]] = ..., media_type: _Optional[_Union[Show.MediaType, str]] = ..., consumption_order: _Optional[_Union[Show.ConsumptionOrder, str]] = ..., availability: _Optional[_Iterable[_Union[Availability, _Mapping]]] = ..., trailer_uri: _Optional[str] = ..., music_and_talk: bool = ..., is_audiobook: bool = ..., is_creator_channel: bool = ...) -> None: ...

class Episode(_message.Message):
    __slots__ = ("gid", "name", "duration", "audio", "description", "number", "publish_time", "deprecated_popularity", "cover_image", "language", "explicit", "show", "video", "video_preview", "audio_preview", "restriction", "freeze_frame", "keyword", "allow_background_playback", "availability", "external_url", "original_audio", "type", "music_and_talk", "content_rating", "is_audiobook_chapter", "is_podcast_short")
    class EpisodeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FULL: _ClassVar[Episode.EpisodeType]
        TRAILER: _ClassVar[Episode.EpisodeType]
        BONUS: _ClassVar[Episode.EpisodeType]
    FULL: Episode.EpisodeType
    TRAILER: Episode.EpisodeType
    BONUS: Episode.EpisodeType
    GID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_TIME_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_POPULARITY_FIELD_NUMBER: _ClassVar[int]
    COVER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    EXPLICIT_FIELD_NUMBER: _ClassVar[int]
    SHOW_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    VIDEO_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    AUDIO_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    FREEZE_FRAME_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    ALLOW_BACKGROUND_PLAYBACK_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_URL_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_AUDIO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MUSIC_AND_TALK_FIELD_NUMBER: _ClassVar[int]
    CONTENT_RATING_FIELD_NUMBER: _ClassVar[int]
    IS_AUDIOBOOK_CHAPTER_FIELD_NUMBER: _ClassVar[int]
    IS_PODCAST_SHORT_FIELD_NUMBER: _ClassVar[int]
    gid: bytes
    name: str
    duration: int
    audio: _containers.RepeatedCompositeFieldContainer[AudioFile]
    description: str
    number: int
    publish_time: Date
    deprecated_popularity: int
    cover_image: ImageGroup
    language: str
    explicit: bool
    show: Show
    video: _containers.RepeatedCompositeFieldContainer[VideoFile]
    video_preview: _containers.RepeatedCompositeFieldContainer[VideoFile]
    audio_preview: _containers.RepeatedCompositeFieldContainer[AudioFile]
    restriction: _containers.RepeatedCompositeFieldContainer[Restriction]
    freeze_frame: ImageGroup
    keyword: _containers.RepeatedScalarFieldContainer[str]
    allow_background_playback: bool
    availability: _containers.RepeatedCompositeFieldContainer[Availability]
    external_url: str
    original_audio: Audio
    type: Episode.EpisodeType
    music_and_talk: bool
    content_rating: _containers.RepeatedCompositeFieldContainer[ContentRating]
    is_audiobook_chapter: bool
    is_podcast_short: bool
    def __init__(self, gid: _Optional[bytes] = ..., name: _Optional[str] = ..., duration: _Optional[int] = ..., audio: _Optional[_Iterable[_Union[AudioFile, _Mapping]]] = ..., description: _Optional[str] = ..., number: _Optional[int] = ..., publish_time: _Optional[_Union[Date, _Mapping]] = ..., deprecated_popularity: _Optional[int] = ..., cover_image: _Optional[_Union[ImageGroup, _Mapping]] = ..., language: _Optional[str] = ..., explicit: bool = ..., show: _Optional[_Union[Show, _Mapping]] = ..., video: _Optional[_Iterable[_Union[VideoFile, _Mapping]]] = ..., video_preview: _Optional[_Iterable[_Union[VideoFile, _Mapping]]] = ..., audio_preview: _Optional[_Iterable[_Union[AudioFile, _Mapping]]] = ..., restriction: _Optional[_Iterable[_Union[Restriction, _Mapping]]] = ..., freeze_frame: _Optional[_Union[ImageGroup, _Mapping]] = ..., keyword: _Optional[_Iterable[str]] = ..., allow_background_playback: bool = ..., availability: _Optional[_Iterable[_Union[Availability, _Mapping]]] = ..., external_url: _Optional[str] = ..., original_audio: _Optional[_Union[Audio, _Mapping]] = ..., type: _Optional[_Union[Episode.EpisodeType, str]] = ..., music_and_talk: bool = ..., content_rating: _Optional[_Iterable[_Union[ContentRating, _Mapping]]] = ..., is_audiobook_chapter: bool = ..., is_podcast_short: bool = ...) -> None: ...

class Licensor(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    def __init__(self, uuid: _Optional[bytes] = ...) -> None: ...

class Audio(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    def __init__(self, uuid: _Optional[bytes] = ...) -> None: ...

class TopTracks(_message.Message):
    __slots__ = ("country", "track")
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    TRACK_FIELD_NUMBER: _ClassVar[int]
    country: str
    track: _containers.RepeatedCompositeFieldContainer[Track]
    def __init__(self, country: _Optional[str] = ..., track: _Optional[_Iterable[_Union[Track, _Mapping]]] = ...) -> None: ...

class ActivityPeriod(_message.Message):
    __slots__ = ("start_year", "end_year", "decade")
    START_YEAR_FIELD_NUMBER: _ClassVar[int]
    END_YEAR_FIELD_NUMBER: _ClassVar[int]
    DECADE_FIELD_NUMBER: _ClassVar[int]
    start_year: int
    end_year: int
    decade: int
    def __init__(self, start_year: _Optional[int] = ..., end_year: _Optional[int] = ..., decade: _Optional[int] = ...) -> None: ...

class AlbumGroup(_message.Message):
    __slots__ = ("album",)
    ALBUM_FIELD_NUMBER: _ClassVar[int]
    album: _containers.RepeatedCompositeFieldContainer[Album]
    def __init__(self, album: _Optional[_Iterable[_Union[Album, _Mapping]]] = ...) -> None: ...

class Date(_message.Message):
    __slots__ = ("year", "month", "day", "hour", "minute")
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MINUTE_FIELD_NUMBER: _ClassVar[int]
    year: int
    month: int
    day: int
    hour: int
    minute: int
    def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., minute: _Optional[int] = ...) -> None: ...

class Image(_message.Message):
    __slots__ = ("file_id", "size", "width", "height")
    class Size(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT: _ClassVar[Image.Size]
        SMALL: _ClassVar[Image.Size]
        LARGE: _ClassVar[Image.Size]
        XLARGE: _ClassVar[Image.Size]
    DEFAULT: Image.Size
    SMALL: Image.Size
    LARGE: Image.Size
    XLARGE: Image.Size
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    file_id: bytes
    size: Image.Size
    width: int
    height: int
    def __init__(self, file_id: _Optional[bytes] = ..., size: _Optional[_Union[Image.Size, str]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class ImageGroup(_message.Message):
    __slots__ = ("image",)
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, image: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...

class Biography(_message.Message):
    __slots__ = ("text", "portrait", "portrait_group")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    PORTRAIT_FIELD_NUMBER: _ClassVar[int]
    PORTRAIT_GROUP_FIELD_NUMBER: _ClassVar[int]
    text: str
    portrait: _containers.RepeatedCompositeFieldContainer[Image]
    portrait_group: _containers.RepeatedCompositeFieldContainer[ImageGroup]
    def __init__(self, text: _Optional[str] = ..., portrait: _Optional[_Iterable[_Union[Image, _Mapping]]] = ..., portrait_group: _Optional[_Iterable[_Union[ImageGroup, _Mapping]]] = ...) -> None: ...

class Disc(_message.Message):
    __slots__ = ("number", "name", "track")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TRACK_FIELD_NUMBER: _ClassVar[int]
    number: int
    name: str
    track: _containers.RepeatedCompositeFieldContainer[Track]
    def __init__(self, number: _Optional[int] = ..., name: _Optional[str] = ..., track: _Optional[_Iterable[_Union[Track, _Mapping]]] = ...) -> None: ...

class Copyright(_message.Message):
    __slots__ = ("type", "text")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        P: _ClassVar[Copyright.Type]
        C: _ClassVar[Copyright.Type]
    P: Copyright.Type
    C: Copyright.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    type: Copyright.Type
    text: str
    def __init__(self, type: _Optional[_Union[Copyright.Type, str]] = ..., text: _Optional[str] = ...) -> None: ...

class Restriction(_message.Message):
    __slots__ = ("catalogue", "type", "catalogue_str", "countries_allowed", "countries_forbidden")
    class Catalogue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AD: _ClassVar[Restriction.Catalogue]
        SUBSCRIPTION: _ClassVar[Restriction.Catalogue]
        CATALOGUE_ALL: _ClassVar[Restriction.Catalogue]
        SHUFFLE: _ClassVar[Restriction.Catalogue]
        COMMERCIAL: _ClassVar[Restriction.Catalogue]
    AD: Restriction.Catalogue
    SUBSCRIPTION: Restriction.Catalogue
    CATALOGUE_ALL: Restriction.Catalogue
    SHUFFLE: Restriction.Catalogue
    COMMERCIAL: Restriction.Catalogue
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STREAMING: _ClassVar[Restriction.Type]
    STREAMING: Restriction.Type
    CATALOGUE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CATALOGUE_STR_FIELD_NUMBER: _ClassVar[int]
    COUNTRIES_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    COUNTRIES_FORBIDDEN_FIELD_NUMBER: _ClassVar[int]
    catalogue: _containers.RepeatedScalarFieldContainer[Restriction.Catalogue]
    type: Restriction.Type
    catalogue_str: _containers.RepeatedScalarFieldContainer[str]
    countries_allowed: str
    countries_forbidden: str
    def __init__(self, catalogue: _Optional[_Iterable[_Union[Restriction.Catalogue, str]]] = ..., type: _Optional[_Union[Restriction.Type, str]] = ..., catalogue_str: _Optional[_Iterable[str]] = ..., countries_allowed: _Optional[str] = ..., countries_forbidden: _Optional[str] = ...) -> None: ...

class Availability(_message.Message):
    __slots__ = ("catalogue_str", "start")
    CATALOGUE_STR_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    catalogue_str: _containers.RepeatedScalarFieldContainer[str]
    start: Date
    def __init__(self, catalogue_str: _Optional[_Iterable[str]] = ..., start: _Optional[_Union[Date, _Mapping]] = ...) -> None: ...

class SalePeriod(_message.Message):
    __slots__ = ("restriction", "start", "end")
    RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    restriction: _containers.RepeatedCompositeFieldContainer[Restriction]
    start: Date
    end: Date
    def __init__(self, restriction: _Optional[_Iterable[_Union[Restriction, _Mapping]]] = ..., start: _Optional[_Union[Date, _Mapping]] = ..., end: _Optional[_Union[Date, _Mapping]] = ...) -> None: ...

class ExternalId(_message.Message):
    __slots__ = ("type", "id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    type: str
    id: str
    def __init__(self, type: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class AudioFile(_message.Message):
    __slots__ = ("file_id", "format")
    class Format(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OGG_VORBIS_96: _ClassVar[AudioFile.Format]
        OGG_VORBIS_160: _ClassVar[AudioFile.Format]
        OGG_VORBIS_320: _ClassVar[AudioFile.Format]
        MP3_256: _ClassVar[AudioFile.Format]
        MP3_320: _ClassVar[AudioFile.Format]
        MP3_160: _ClassVar[AudioFile.Format]
        MP3_96: _ClassVar[AudioFile.Format]
        MP3_160_ENC: _ClassVar[AudioFile.Format]
        AAC_24: _ClassVar[AudioFile.Format]
        AAC_48: _ClassVar[AudioFile.Format]
        FLAC_FLAC: _ClassVar[AudioFile.Format]
        XHE_AAC_24: _ClassVar[AudioFile.Format]
        XHE_AAC_16: _ClassVar[AudioFile.Format]
        XHE_AAC_12: _ClassVar[AudioFile.Format]
        FLAC_FLAC_24BIT: _ClassVar[AudioFile.Format]
    OGG_VORBIS_96: AudioFile.Format
    OGG_VORBIS_160: AudioFile.Format
    OGG_VORBIS_320: AudioFile.Format
    MP3_256: AudioFile.Format
    MP3_320: AudioFile.Format
    MP3_160: AudioFile.Format
    MP3_96: AudioFile.Format
    MP3_160_ENC: AudioFile.Format
    AAC_24: AudioFile.Format
    AAC_48: AudioFile.Format
    FLAC_FLAC: AudioFile.Format
    XHE_AAC_24: AudioFile.Format
    XHE_AAC_16: AudioFile.Format
    XHE_AAC_12: AudioFile.Format
    FLAC_FLAC_24BIT: AudioFile.Format
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    file_id: bytes
    format: AudioFile.Format
    def __init__(self, file_id: _Optional[bytes] = ..., format: _Optional[_Union[AudioFile.Format, str]] = ...) -> None: ...

class Video(_message.Message):
    __slots__ = ("gid",)
    GID_FIELD_NUMBER: _ClassVar[int]
    gid: bytes
    def __init__(self, gid: _Optional[bytes] = ...) -> None: ...

class VideoFile(_message.Message):
    __slots__ = ("file_id",)
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    file_id: bytes
    def __init__(self, file_id: _Optional[bytes] = ...) -> None: ...

class ContentRating(_message.Message):
    __slots__ = ("country", "tag")
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    country: str
    tag: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, country: _Optional[str] = ..., tag: _Optional[_Iterable[str]] = ...) -> None: ...
