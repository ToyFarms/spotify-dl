from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StoredCredential(_message.Message):
    __slots__ = ()
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    username: str
    data: bytes
    def __init__(self, username: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class Password(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PADDING_FIELD_NUMBER: _ClassVar[int]
    id: str
    password: str
    padding: bytes
    def __init__(self, id: _Optional[str] = ..., password: _Optional[str] = ..., padding: _Optional[bytes] = ...) -> None: ...

class FacebookAccessToken(_message.Message):
    __slots__ = ()
    FB_UID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    fb_uid: str
    access_token: str
    def __init__(self, fb_uid: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class OneTimeToken(_message.Message):
    __slots__ = ()
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ParentChildCredential(_message.Message):
    __slots__ = ()
    CHILD_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_STORED_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    child_id: str
    parent_stored_credential: StoredCredential
    def __init__(self, child_id: _Optional[str] = ..., parent_stored_credential: _Optional[_Union[StoredCredential, _Mapping]] = ...) -> None: ...

class AppleSignInCredential(_message.Message):
    __slots__ = ()
    AUTH_CODE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_ID_FIELD_NUMBER: _ClassVar[int]
    auth_code: str
    redirect_uri: str
    bundle_id: str
    def __init__(self, auth_code: _Optional[str] = ..., redirect_uri: _Optional[str] = ..., bundle_id: _Optional[str] = ...) -> None: ...

class SamsungSignInCredential(_message.Message):
    __slots__ = ()
    AUTH_CODE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    ID_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    auth_code: str
    redirect_uri: str
    id_token: str
    token_endpoint_url: str
    def __init__(self, auth_code: _Optional[str] = ..., redirect_uri: _Optional[str] = ..., id_token: _Optional[str] = ..., token_endpoint_url: _Optional[str] = ...) -> None: ...

class GoogleSignInCredential(_message.Message):
    __slots__ = ()
    AUTH_CODE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    auth_code: str
    redirect_uri: str
    def __init__(self, auth_code: _Optional[str] = ..., redirect_uri: _Optional[str] = ...) -> None: ...
