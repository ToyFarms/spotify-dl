from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PhoneNumber(_message.Message):
    __slots__ = ()
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    ISO_COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CALLING_CODE_FIELD_NUMBER: _ClassVar[int]
    number: str
    iso_country_code: str
    country_calling_code: str
    def __init__(self, number: _Optional[str] = ..., iso_country_code: _Optional[str] = ..., country_calling_code: _Optional[str] = ...) -> None: ...
