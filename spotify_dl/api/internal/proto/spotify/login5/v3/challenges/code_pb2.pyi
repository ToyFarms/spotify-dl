from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CodeChallenge(_message.Message):
    __slots__ = ()
    class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[CodeChallenge.Method]
        SMS: _ClassVar[CodeChallenge.Method]
    UNKNOWN: CodeChallenge.Method
    SMS: CodeChallenge.Method
    METHOD_FIELD_NUMBER: _ClassVar[int]
    CODE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    method: CodeChallenge.Method
    code_length: int
    expires_in: int
    canonical_phone_number: str
    def __init__(self, method: _Optional[_Union[CodeChallenge.Method, str]] = ..., code_length: _Optional[int] = ..., expires_in: _Optional[int] = ..., canonical_phone_number: _Optional[str] = ...) -> None: ...

class CodeSolution(_message.Message):
    __slots__ = ()
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: str
    def __init__(self, code: _Optional[str] = ...) -> None: ...
