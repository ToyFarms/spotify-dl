from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserInfo(_message.Message):
    __slots__ = ()
    class Gender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[UserInfo.Gender]
        MALE: _ClassVar[UserInfo.Gender]
        FEMALE: _ClassVar[UserInfo.Gender]
        NEUTRAL: _ClassVar[UserInfo.Gender]
    UNKNOWN: UserInfo.Gender
    MALE: UserInfo.Gender
    FEMALE: UserInfo.Gender
    NEUTRAL: UserInfo.Gender
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    BIRTHDATE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    EMAIL_ALREADY_REGISTERED_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    email_verified: bool
    birthdate: str
    gender: UserInfo.Gender
    phone_number: str
    phone_number_verified: bool
    email_already_registered: bool
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., email_verified: _Optional[bool] = ..., birthdate: _Optional[str] = ..., gender: _Optional[_Union[UserInfo.Gender, str]] = ..., phone_number: _Optional[str] = ..., phone_number_verified: _Optional[bool] = ..., email_already_registered: _Optional[bool] = ...) -> None: ...
