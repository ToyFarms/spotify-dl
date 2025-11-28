import datetime

from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HashcashChallenge(_message.Message):
    __slots__ = ()
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    prefix: bytes
    length: int
    def __init__(self, prefix: _Optional[bytes] = ..., length: _Optional[int] = ...) -> None: ...

class HashcashSolution(_message.Message):
    __slots__ = ()
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    suffix: bytes
    duration: _duration_pb2.Duration
    def __init__(self, suffix: _Optional[bytes] = ..., duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ...) -> None: ...
