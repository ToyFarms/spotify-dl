import extension_kind_pb2 as _extension_kind_pb2
import entity_extension_data_pb2 as _entity_extension_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExtensionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[ExtensionType]
    GENERIC: _ClassVar[ExtensionType]
    ASSOC: _ClassVar[ExtensionType]
UNKNOWN: ExtensionType
GENERIC: ExtensionType
ASSOC: ExtensionType

class ExtensionQuery(_message.Message):
    __slots__ = ()
    EXTENSION_KIND_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    extension_kind: _extension_kind_pb2.ExtensionKind
    etag: str
    def __init__(self, extension_kind: _Optional[_Union[_extension_kind_pb2.ExtensionKind, str]] = ..., etag: _Optional[str] = ...) -> None: ...

class EntityRequest(_message.Message):
    __slots__ = ()
    ENTITY_URI_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    entity_uri: str
    query: _containers.RepeatedCompositeFieldContainer[ExtensionQuery]
    def __init__(self, entity_uri: _Optional[str] = ..., query: _Optional[_Iterable[_Union[ExtensionQuery, _Mapping]]] = ...) -> None: ...

class BatchedEntityRequestHeader(_message.Message):
    __slots__ = ()
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    CATALOGUE_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    country: str
    catalogue: str
    task_id: bytes
    def __init__(self, country: _Optional[str] = ..., catalogue: _Optional[str] = ..., task_id: _Optional[bytes] = ...) -> None: ...

class BatchedEntityRequest(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTITY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    header: BatchedEntityRequestHeader
    entity_request: _containers.RepeatedCompositeFieldContainer[EntityRequest]
    def __init__(self, header: _Optional[_Union[BatchedEntityRequestHeader, _Mapping]] = ..., entity_request: _Optional[_Iterable[_Union[EntityRequest, _Mapping]]] = ...) -> None: ...

class EntityExtensionDataArrayHeader(_message.Message):
    __slots__ = ()
    PROVIDER_ERROR_STATUS_FIELD_NUMBER: _ClassVar[int]
    CACHE_TTL_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_TTL_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    provider_error_status: int
    cache_ttl_in_seconds: int
    offline_ttl_in_seconds: int
    extension_type: ExtensionType
    def __init__(self, provider_error_status: _Optional[int] = ..., cache_ttl_in_seconds: _Optional[int] = ..., offline_ttl_in_seconds: _Optional[int] = ..., extension_type: _Optional[_Union[ExtensionType, str]] = ...) -> None: ...

class EntityExtensionDataArray(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_KIND_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_DATA_FIELD_NUMBER: _ClassVar[int]
    header: EntityExtensionDataArrayHeader
    extension_kind: _extension_kind_pb2.ExtensionKind
    extension_data: _containers.RepeatedCompositeFieldContainer[_entity_extension_data_pb2.EntityExtensionData]
    def __init__(self, header: _Optional[_Union[EntityExtensionDataArrayHeader, _Mapping]] = ..., extension_kind: _Optional[_Union[_extension_kind_pb2.ExtensionKind, str]] = ..., extension_data: _Optional[_Iterable[_Union[_entity_extension_data_pb2.EntityExtensionData, _Mapping]]] = ...) -> None: ...

class BatchedExtensionResponseHeader(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BatchedExtensionResponse(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_METADATA_FIELD_NUMBER: _ClassVar[int]
    header: BatchedExtensionResponseHeader
    extended_metadata: _containers.RepeatedCompositeFieldContainer[EntityExtensionDataArray]
    def __init__(self, header: _Optional[_Union[BatchedExtensionResponseHeader, _Mapping]] = ..., extended_metadata: _Optional[_Iterable[_Union[EntityExtensionDataArray, _Mapping]]] = ...) -> None: ...
