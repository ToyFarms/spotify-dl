from ....spotify.login5.v3 import client_info_pb2 as _client_info_pb2
from ....spotify.login5.v3 import user_info_pb2 as _user_info_pb2
from ....spotify.login5.v3.challenges import code_pb2 as _code_pb2
from ....spotify.login5.v3.challenges import hashcash_pb2 as _hashcash_pb2
from ....spotify.login5.v3.credentials import credentials_pb2 as _credentials_pb2
from ....spotify.login5.v3.identifiers import identifiers_pb2 as _identifiers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoginError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_ERROR: _ClassVar[LoginError]
    INVALID_CREDENTIALS: _ClassVar[LoginError]
    BAD_REQUEST: _ClassVar[LoginError]
    UNSUPPORTED_LOGIN_PROTOCOL: _ClassVar[LoginError]
    TIMEOUT: _ClassVar[LoginError]
    UNKNOWN_IDENTIFIER: _ClassVar[LoginError]
    TOO_MANY_ATTEMPTS: _ClassVar[LoginError]
    INVALID_PHONENUMBER: _ClassVar[LoginError]
    TRY_AGAIN_LATER: _ClassVar[LoginError]
UNKNOWN_ERROR: LoginError
INVALID_CREDENTIALS: LoginError
BAD_REQUEST: LoginError
UNSUPPORTED_LOGIN_PROTOCOL: LoginError
TIMEOUT: LoginError
UNKNOWN_IDENTIFIER: LoginError
TOO_MANY_ATTEMPTS: LoginError
INVALID_PHONENUMBER: LoginError
TRY_AGAIN_LATER: LoginError

class Challenges(_message.Message):
    __slots__ = ()
    CHALLENGES_FIELD_NUMBER: _ClassVar[int]
    challenges: _containers.RepeatedCompositeFieldContainer[Challenge]
    def __init__(self, challenges: _Optional[_Iterable[_Union[Challenge, _Mapping]]] = ...) -> None: ...

class Challenge(_message.Message):
    __slots__ = ()
    HASHCASH_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    hashcash: _hashcash_pb2.HashcashChallenge
    code: _code_pb2.CodeChallenge
    def __init__(self, hashcash: _Optional[_Union[_hashcash_pb2.HashcashChallenge, _Mapping]] = ..., code: _Optional[_Union[_code_pb2.CodeChallenge, _Mapping]] = ...) -> None: ...

class ChallengeSolutions(_message.Message):
    __slots__ = ()
    SOLUTIONS_FIELD_NUMBER: _ClassVar[int]
    solutions: _containers.RepeatedCompositeFieldContainer[ChallengeSolution]
    def __init__(self, solutions: _Optional[_Iterable[_Union[ChallengeSolution, _Mapping]]] = ...) -> None: ...

class ChallengeSolution(_message.Message):
    __slots__ = ()
    HASHCASH_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    hashcash: _hashcash_pb2.HashcashSolution
    code: _code_pb2.CodeSolution
    def __init__(self, hashcash: _Optional[_Union[_hashcash_pb2.HashcashSolution, _Mapping]] = ..., code: _Optional[_Union[_code_pb2.CodeSolution, _Mapping]] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ()
    CLIENT_INFO_FIELD_NUMBER: _ClassVar[int]
    LOGIN_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_SOLUTIONS_FIELD_NUMBER: _ClassVar[int]
    STORED_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FACEBOOK_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ONE_TIME_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PARENT_CHILD_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    APPLE_SIGN_IN_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    SAMSUNG_SIGN_IN_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_SIGN_IN_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    client_info: _client_info_pb2.ClientInfo
    login_context: bytes
    challenge_solutions: ChallengeSolutions
    stored_credential: _credentials_pb2.StoredCredential
    password: _credentials_pb2.Password
    facebook_access_token: _credentials_pb2.FacebookAccessToken
    phone_number: _identifiers_pb2.PhoneNumber
    one_time_token: _credentials_pb2.OneTimeToken
    parent_child_credential: _credentials_pb2.ParentChildCredential
    apple_sign_in_credential: _credentials_pb2.AppleSignInCredential
    samsung_sign_in_credential: _credentials_pb2.SamsungSignInCredential
    google_sign_in_credential: _credentials_pb2.GoogleSignInCredential
    def __init__(self, client_info: _Optional[_Union[_client_info_pb2.ClientInfo, _Mapping]] = ..., login_context: _Optional[bytes] = ..., challenge_solutions: _Optional[_Union[ChallengeSolutions, _Mapping]] = ..., stored_credential: _Optional[_Union[_credentials_pb2.StoredCredential, _Mapping]] = ..., password: _Optional[_Union[_credentials_pb2.Password, _Mapping]] = ..., facebook_access_token: _Optional[_Union[_credentials_pb2.FacebookAccessToken, _Mapping]] = ..., phone_number: _Optional[_Union[_identifiers_pb2.PhoneNumber, _Mapping]] = ..., one_time_token: _Optional[_Union[_credentials_pb2.OneTimeToken, _Mapping]] = ..., parent_child_credential: _Optional[_Union[_credentials_pb2.ParentChildCredential, _Mapping]] = ..., apple_sign_in_credential: _Optional[_Union[_credentials_pb2.AppleSignInCredential, _Mapping]] = ..., samsung_sign_in_credential: _Optional[_Union[_credentials_pb2.SamsungSignInCredential, _Mapping]] = ..., google_sign_in_credential: _Optional[_Union[_credentials_pb2.GoogleSignInCredential, _Mapping]] = ...) -> None: ...

class LoginOk(_message.Message):
    __slots__ = ()
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    STORED_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    username: str
    access_token: str
    stored_credential: bytes
    access_token_expires_in: int
    def __init__(self, username: _Optional[str] = ..., access_token: _Optional[str] = ..., stored_credential: _Optional[bytes] = ..., access_token_expires_in: _Optional[int] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ()
    class Warnings(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_WARNING: _ClassVar[LoginResponse.Warnings]
        DEPRECATED_PROTOCOL_VERSION: _ClassVar[LoginResponse.Warnings]
    UNKNOWN_WARNING: LoginResponse.Warnings
    DEPRECATED_PROTOCOL_VERSION: LoginResponse.Warnings
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    LOGIN_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    USER_INFO_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHALLENGES_FIELD_NUMBER: _ClassVar[int]
    warnings: _containers.RepeatedScalarFieldContainer[LoginResponse.Warnings]
    login_context: bytes
    identifier_token: str
    user_info: _user_info_pb2.UserInfo
    ok: LoginOk
    error: LoginError
    challenges: Challenges
    def __init__(self, warnings: _Optional[_Iterable[_Union[LoginResponse.Warnings, str]]] = ..., login_context: _Optional[bytes] = ..., identifier_token: _Optional[str] = ..., user_info: _Optional[_Union[_user_info_pb2.UserInfo, _Mapping]] = ..., ok: _Optional[_Union[LoginOk, _Mapping]] = ..., error: _Optional[_Union[LoginError, str]] = ..., challenges: _Optional[_Union[Challenges, _Mapping]] = ...) -> None: ...
