from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MercuryMultiGetRequest(_message.Message):
    __slots__ = ()
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _containers.RepeatedCompositeFieldContainer[MercuryRequest]
    def __init__(self, request: _Optional[_Iterable[_Union[MercuryRequest, _Mapping]]] = ...) -> None: ...

class MercuryMultiGetReply(_message.Message):
    __slots__ = ()
    REPLY_FIELD_NUMBER: _ClassVar[int]
    reply: _containers.RepeatedCompositeFieldContainer[MercuryReply]
    def __init__(self, reply: _Optional[_Iterable[_Union[MercuryReply, _Mapping]]] = ...) -> None: ...

class MercuryRequest(_message.Message):
    __slots__ = ()
    URI_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    uri: str
    content_type: str
    body: bytes
    etag: bytes
    def __init__(self, uri: _Optional[str] = ..., content_type: _Optional[str] = ..., body: _Optional[bytes] = ..., etag: _Optional[bytes] = ...) -> None: ...

class MercuryReply(_message.Message):
    __slots__ = ()
    class CachePolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CACHE_NO: _ClassVar[MercuryReply.CachePolicy]
        CACHE_PRIVATE: _ClassVar[MercuryReply.CachePolicy]
        CACHE_PUBLIC: _ClassVar[MercuryReply.CachePolicy]
    CACHE_NO: MercuryReply.CachePolicy
    CACHE_PRIVATE: MercuryReply.CachePolicy
    CACHE_PUBLIC: MercuryReply.CachePolicy
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CACHE_POLICY_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    status_message: str
    cache_policy: MercuryReply.CachePolicy
    ttl: int
    etag: bytes
    content_type: str
    body: bytes
    def __init__(self, status_code: _Optional[int] = ..., status_message: _Optional[str] = ..., cache_policy: _Optional[_Union[MercuryReply.CachePolicy, str]] = ..., ttl: _Optional[int] = ..., etag: _Optional[bytes] = ..., content_type: _Optional[str] = ..., body: _Optional[bytes] = ...) -> None: ...

class Header(_message.Message):
    __slots__ = ()
    URI_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELDS_FIELD_NUMBER: _ClassVar[int]
    uri: str
    content_type: str
    method: str
    status_code: int
    user_fields: _containers.RepeatedCompositeFieldContainer[UserField]
    def __init__(self, uri: _Optional[str] = ..., content_type: _Optional[str] = ..., method: _Optional[str] = ..., status_code: _Optional[int] = ..., user_fields: _Optional[_Iterable[_Union[UserField, _Mapping]]] = ...) -> None: ...

class UserField(_message.Message):
    __slots__ = ()
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: bytes
    def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
