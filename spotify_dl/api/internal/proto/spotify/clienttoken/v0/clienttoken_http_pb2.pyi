import connectivity_pb2 as _connectivity_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientTokenRequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REQUEST_UNKNOWN: _ClassVar[ClientTokenRequestType]
    REQUEST_CLIENT_DATA_REQUEST: _ClassVar[ClientTokenRequestType]
    REQUEST_CHALLENGE_ANSWERS_REQUEST: _ClassVar[ClientTokenRequestType]

class ClientTokenResponseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESPONSE_UNKNOWN: _ClassVar[ClientTokenResponseType]
    RESPONSE_GRANTED_TOKEN_RESPONSE: _ClassVar[ClientTokenResponseType]
    RESPONSE_CHALLENGES_RESPONSE: _ClassVar[ClientTokenResponseType]

class ChallengeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHALLENGE_UNKNOWN: _ClassVar[ChallengeType]
    CHALLENGE_CLIENT_SECRET_HMAC: _ClassVar[ChallengeType]
    CHALLENGE_EVALUATE_JS: _ClassVar[ChallengeType]
    CHALLENGE_HASH_CASH: _ClassVar[ChallengeType]
REQUEST_UNKNOWN: ClientTokenRequestType
REQUEST_CLIENT_DATA_REQUEST: ClientTokenRequestType
REQUEST_CHALLENGE_ANSWERS_REQUEST: ClientTokenRequestType
RESPONSE_UNKNOWN: ClientTokenResponseType
RESPONSE_GRANTED_TOKEN_RESPONSE: ClientTokenResponseType
RESPONSE_CHALLENGES_RESPONSE: ClientTokenResponseType
CHALLENGE_UNKNOWN: ChallengeType
CHALLENGE_CLIENT_SECRET_HMAC: ChallengeType
CHALLENGE_EVALUATE_JS: ChallengeType
CHALLENGE_HASH_CASH: ChallengeType

class ClientTokenRequest(_message.Message):
    __slots__ = ()
    REQUEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_DATA_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_ANSWERS_FIELD_NUMBER: _ClassVar[int]
    request_type: ClientTokenRequestType
    client_data: ClientDataRequest
    challenge_answers: ChallengeAnswersRequest
    def __init__(self, request_type: _Optional[_Union[ClientTokenRequestType, str]] = ..., client_data: _Optional[_Union[ClientDataRequest, _Mapping]] = ..., challenge_answers: _Optional[_Union[ChallengeAnswersRequest, _Mapping]] = ...) -> None: ...

class ClientDataRequest(_message.Message):
    __slots__ = ()
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_SDK_DATA_FIELD_NUMBER: _ClassVar[int]
    client_version: str
    client_id: str
    connectivity_sdk_data: _connectivity_pb2.ConnectivitySdkData
    def __init__(self, client_version: _Optional[str] = ..., client_id: _Optional[str] = ..., connectivity_sdk_data: _Optional[_Union[_connectivity_pb2.ConnectivitySdkData, _Mapping]] = ...) -> None: ...

class ChallengeAnswersRequest(_message.Message):
    __slots__ = ()
    STATE_FIELD_NUMBER: _ClassVar[int]
    ANSWERS_FIELD_NUMBER: _ClassVar[int]
    state: str
    answers: _containers.RepeatedCompositeFieldContainer[ChallengeAnswer]
    def __init__(self, state: _Optional[str] = ..., answers: _Optional[_Iterable[_Union[ChallengeAnswer, _Mapping]]] = ...) -> None: ...

class ClientTokenResponse(_message.Message):
    __slots__ = ()
    RESPONSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    GRANTED_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CHALLENGES_FIELD_NUMBER: _ClassVar[int]
    response_type: ClientTokenResponseType
    granted_token: GrantedTokenResponse
    challenges: ChallengesResponse
    def __init__(self, response_type: _Optional[_Union[ClientTokenResponseType, str]] = ..., granted_token: _Optional[_Union[GrantedTokenResponse, _Mapping]] = ..., challenges: _Optional[_Union[ChallengesResponse, _Mapping]] = ...) -> None: ...

class TokenDomain(_message.Message):
    __slots__ = ()
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: str
    def __init__(self, domain: _Optional[str] = ...) -> None: ...

class GrantedTokenResponse(_message.Message):
    __slots__ = ()
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AFTER_SECONDS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_AFTER_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    token: str
    expires_after_seconds: int
    refresh_after_seconds: int
    domains: _containers.RepeatedCompositeFieldContainer[TokenDomain]
    def __init__(self, token: _Optional[str] = ..., expires_after_seconds: _Optional[int] = ..., refresh_after_seconds: _Optional[int] = ..., domains: _Optional[_Iterable[_Union[TokenDomain, _Mapping]]] = ...) -> None: ...

class ChallengesResponse(_message.Message):
    __slots__ = ()
    STATE_FIELD_NUMBER: _ClassVar[int]
    CHALLENGES_FIELD_NUMBER: _ClassVar[int]
    state: str
    challenges: _containers.RepeatedCompositeFieldContainer[Challenge]
    def __init__(self, state: _Optional[str] = ..., challenges: _Optional[_Iterable[_Union[Challenge, _Mapping]]] = ...) -> None: ...

class ClientSecretParameters(_message.Message):
    __slots__ = ()
    SALT_FIELD_NUMBER: _ClassVar[int]
    salt: str
    def __init__(self, salt: _Optional[str] = ...) -> None: ...

class EvaluateJSParameters(_message.Message):
    __slots__ = ()
    CODE_FIELD_NUMBER: _ClassVar[int]
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    code: str
    libraries: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, code: _Optional[str] = ..., libraries: _Optional[_Iterable[str]] = ...) -> None: ...

class HashCashParameters(_message.Message):
    __slots__ = ()
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    length: int
    prefix: str
    def __init__(self, length: _Optional[int] = ..., prefix: _Optional[str] = ...) -> None: ...

class Challenge(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EVALUATE_JS_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EVALUATE_HASHCASH_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    type: ChallengeType
    client_secret_parameters: ClientSecretParameters
    evaluate_js_parameters: EvaluateJSParameters
    evaluate_hashcash_parameters: HashCashParameters
    def __init__(self, type: _Optional[_Union[ChallengeType, str]] = ..., client_secret_parameters: _Optional[_Union[ClientSecretParameters, _Mapping]] = ..., evaluate_js_parameters: _Optional[_Union[EvaluateJSParameters, _Mapping]] = ..., evaluate_hashcash_parameters: _Optional[_Union[HashCashParameters, _Mapping]] = ...) -> None: ...

class ClientSecretHMACAnswer(_message.Message):
    __slots__ = ()
    HMAC_FIELD_NUMBER: _ClassVar[int]
    hmac: str
    def __init__(self, hmac: _Optional[str] = ...) -> None: ...

class EvaluateJSAnswer(_message.Message):
    __slots__ = ()
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class HashCashAnswer(_message.Message):
    __slots__ = ()
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    suffix: str
    def __init__(self, suffix: _Optional[str] = ...) -> None: ...

class ChallengeAnswer(_message.Message):
    __slots__ = ()
    CHALLENGETYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    EVALUATE_JS_FIELD_NUMBER: _ClassVar[int]
    HASH_CASH_FIELD_NUMBER: _ClassVar[int]
    ChallengeType: ChallengeType
    client_secret: ClientSecretHMACAnswer
    evaluate_js: EvaluateJSAnswer
    hash_cash: HashCashAnswer
    def __init__(self, ChallengeType: _Optional[_Union[ChallengeType, str]] = ..., client_secret: _Optional[_Union[ClientSecretHMACAnswer, _Mapping]] = ..., evaluate_js: _Optional[_Union[EvaluateJSAnswer, _Mapping]] = ..., hash_cash: _Optional[_Union[HashCashAnswer, _Mapping]] = ...) -> None: ...

class ClientTokenBadRequest(_message.Message):
    __slots__ = ()
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
