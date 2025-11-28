from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityExtensionDataHeader(_message.Message):
    __slots__ = ()
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    CACHE_TTL_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_TTL_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    etag: str
    locale: str
    cache_ttl_in_seconds: int
    offline_ttl_in_seconds: int
    def __init__(self, status_code: _Optional[int] = ..., etag: _Optional[str] = ..., locale: _Optional[str] = ..., cache_ttl_in_seconds: _Optional[int] = ..., offline_ttl_in_seconds: _Optional[int] = ...) -> None: ...

class EntityExtensionData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTITY_URI_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_DATA_FIELD_NUMBER: _ClassVar[int]
    header: EntityExtensionDataHeader
    entity_uri: str
    extension_data: _any_pb2.Any
    def __init__(self, header: _Optional[_Union[EntityExtensionDataHeader, _Mapping]] = ..., entity_uri: _Optional[str] = ..., extension_data: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class PlainListAssoc(_message.Message):
    __slots__ = ()
    ENTITY_URI_FIELD_NUMBER: _ClassVar[int]
    entity_uri: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entity_uri: _Optional[_Iterable[str]] = ...) -> None: ...

class AssocHeader(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Assoc(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PLAIN_LIST_FIELD_NUMBER: _ClassVar[int]
    header: AssocHeader
    plain_list: PlainListAssoc
    def __init__(self, header: _Optional[_Union[AssocHeader, _Mapping]] = ..., plain_list: _Optional[_Union[PlainListAssoc, _Mapping]] = ...) -> None: ...
