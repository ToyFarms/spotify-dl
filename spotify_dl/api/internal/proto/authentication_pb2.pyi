from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthenticationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUTHENTICATION_USER_PASS: _ClassVar[AuthenticationType]
    AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS: _ClassVar[AuthenticationType]
    AUTHENTICATION_STORED_FACEBOOK_CREDENTIALS: _ClassVar[AuthenticationType]
    AUTHENTICATION_SPOTIFY_TOKEN: _ClassVar[AuthenticationType]
    AUTHENTICATION_FACEBOOK_TOKEN: _ClassVar[AuthenticationType]

class AccountCreation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACCOUNT_CREATION_ALWAYS_PROMPT: _ClassVar[AccountCreation]
    ACCOUNT_CREATION_ALWAYS_CREATE: _ClassVar[AccountCreation]

class CpuFamily(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CPU_UNKNOWN: _ClassVar[CpuFamily]
    CPU_X86: _ClassVar[CpuFamily]
    CPU_X86_64: _ClassVar[CpuFamily]
    CPU_PPC: _ClassVar[CpuFamily]
    CPU_PPC_64: _ClassVar[CpuFamily]
    CPU_ARM: _ClassVar[CpuFamily]
    CPU_IA64: _ClassVar[CpuFamily]
    CPU_SH: _ClassVar[CpuFamily]
    CPU_MIPS: _ClassVar[CpuFamily]
    CPU_BLACKFIN: _ClassVar[CpuFamily]

class Brand(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BRAND_UNBRANDED: _ClassVar[Brand]
    BRAND_INQ: _ClassVar[Brand]
    BRAND_HTC: _ClassVar[Brand]
    BRAND_NOKIA: _ClassVar[Brand]

class Os(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OS_UNKNOWN: _ClassVar[Os]
    OS_WINDOWS: _ClassVar[Os]
    OS_OSX: _ClassVar[Os]
    OS_IPHONE: _ClassVar[Os]
    OS_S60: _ClassVar[Os]
    OS_LINUX: _ClassVar[Os]
    OS_WINDOWS_CE: _ClassVar[Os]
    OS_ANDROID: _ClassVar[Os]
    OS_PALM: _ClassVar[Os]
    OS_FREEBSD: _ClassVar[Os]
    OS_BLACKBERRY: _ClassVar[Os]
    OS_SONOS: _ClassVar[Os]
    OS_LOGITECH: _ClassVar[Os]
    OS_WP7: _ClassVar[Os]
    OS_ONKYO: _ClassVar[Os]
    OS_PHILIPS: _ClassVar[Os]
    OS_WD: _ClassVar[Os]
    OS_VOLVO: _ClassVar[Os]
    OS_TIVO: _ClassVar[Os]
    OS_AWOX: _ClassVar[Os]
    OS_MEEGO: _ClassVar[Os]
    OS_QNXNTO: _ClassVar[Os]
    OS_BCO: _ClassVar[Os]

class AccountType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Spotify: _ClassVar[AccountType]
    Facebook: _ClassVar[AccountType]
AUTHENTICATION_USER_PASS: AuthenticationType
AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS: AuthenticationType
AUTHENTICATION_STORED_FACEBOOK_CREDENTIALS: AuthenticationType
AUTHENTICATION_SPOTIFY_TOKEN: AuthenticationType
AUTHENTICATION_FACEBOOK_TOKEN: AuthenticationType
ACCOUNT_CREATION_ALWAYS_PROMPT: AccountCreation
ACCOUNT_CREATION_ALWAYS_CREATE: AccountCreation
CPU_UNKNOWN: CpuFamily
CPU_X86: CpuFamily
CPU_X86_64: CpuFamily
CPU_PPC: CpuFamily
CPU_PPC_64: CpuFamily
CPU_ARM: CpuFamily
CPU_IA64: CpuFamily
CPU_SH: CpuFamily
CPU_MIPS: CpuFamily
CPU_BLACKFIN: CpuFamily
BRAND_UNBRANDED: Brand
BRAND_INQ: Brand
BRAND_HTC: Brand
BRAND_NOKIA: Brand
OS_UNKNOWN: Os
OS_WINDOWS: Os
OS_OSX: Os
OS_IPHONE: Os
OS_S60: Os
OS_LINUX: Os
OS_WINDOWS_CE: Os
OS_ANDROID: Os
OS_PALM: Os
OS_FREEBSD: Os
OS_BLACKBERRY: Os
OS_SONOS: Os
OS_LOGITECH: Os
OS_WP7: Os
OS_ONKYO: Os
OS_PHILIPS: Os
OS_WD: Os
OS_VOLVO: Os
OS_TIVO: Os
OS_AWOX: Os
OS_MEEGO: Os
OS_QNXNTO: Os
OS_BCO: Os
Spotify: AccountType
Facebook: AccountType

class ClientResponseEncrypted(_message.Message):
    __slots__ = ()
    LOGIN_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_CREATION_FIELD_NUMBER: _ClassVar[int]
    FINGERPRINT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PEER_TICKET_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_INFO_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_MODEL_FIELD_NUMBER: _ClassVar[int]
    VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    APPKEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_INFO_FIELD_NUMBER: _ClassVar[int]
    login_credentials: LoginCredentials
    account_creation: AccountCreation
    fingerprint_response: FingerprintResponseUnion
    peer_ticket: PeerTicketUnion
    system_info: SystemInfo
    platform_model: str
    version_string: str
    appkey: LibspotifyAppKey
    client_info: ClientInfo
    def __init__(self, login_credentials: _Optional[_Union[LoginCredentials, _Mapping]] = ..., account_creation: _Optional[_Union[AccountCreation, str]] = ..., fingerprint_response: _Optional[_Union[FingerprintResponseUnion, _Mapping]] = ..., peer_ticket: _Optional[_Union[PeerTicketUnion, _Mapping]] = ..., system_info: _Optional[_Union[SystemInfo, _Mapping]] = ..., platform_model: _Optional[str] = ..., version_string: _Optional[str] = ..., appkey: _Optional[_Union[LibspotifyAppKey, _Mapping]] = ..., client_info: _Optional[_Union[ClientInfo, _Mapping]] = ...) -> None: ...

class LoginCredentials(_message.Message):
    __slots__ = ()
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    TYP_FIELD_NUMBER: _ClassVar[int]
    AUTH_DATA_FIELD_NUMBER: _ClassVar[int]
    username: str
    typ: AuthenticationType
    auth_data: bytes
    def __init__(self, username: _Optional[str] = ..., typ: _Optional[_Union[AuthenticationType, str]] = ..., auth_data: _Optional[bytes] = ...) -> None: ...

class FingerprintResponseUnion(_message.Message):
    __slots__ = ()
    GRAIN_FIELD_NUMBER: _ClassVar[int]
    HMAC_RIPEMD_FIELD_NUMBER: _ClassVar[int]
    grain: FingerprintGrainResponse
    hmac_ripemd: FingerprintHmacRipemdResponse
    def __init__(self, grain: _Optional[_Union[FingerprintGrainResponse, _Mapping]] = ..., hmac_ripemd: _Optional[_Union[FingerprintHmacRipemdResponse, _Mapping]] = ...) -> None: ...

class FingerprintGrainResponse(_message.Message):
    __slots__ = ()
    ENCRYPTED_KEY_FIELD_NUMBER: _ClassVar[int]
    encrypted_key: bytes
    def __init__(self, encrypted_key: _Optional[bytes] = ...) -> None: ...

class FingerprintHmacRipemdResponse(_message.Message):
    __slots__ = ()
    HMAC_FIELD_NUMBER: _ClassVar[int]
    hmac: bytes
    def __init__(self, hmac: _Optional[bytes] = ...) -> None: ...

class PeerTicketUnion(_message.Message):
    __slots__ = ()
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    OLD_TICKET_FIELD_NUMBER: _ClassVar[int]
    public_key: PeerTicketPublicKey
    old_ticket: PeerTicketOld
    def __init__(self, public_key: _Optional[_Union[PeerTicketPublicKey, _Mapping]] = ..., old_ticket: _Optional[_Union[PeerTicketOld, _Mapping]] = ...) -> None: ...

class PeerTicketPublicKey(_message.Message):
    __slots__ = ()
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    public_key: bytes
    def __init__(self, public_key: _Optional[bytes] = ...) -> None: ...

class PeerTicketOld(_message.Message):
    __slots__ = ()
    PEER_TICKET_FIELD_NUMBER: _ClassVar[int]
    PEER_TICKET_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    peer_ticket: bytes
    peer_ticket_signature: bytes
    def __init__(self, peer_ticket: _Optional[bytes] = ..., peer_ticket_signature: _Optional[bytes] = ...) -> None: ...

class SystemInfo(_message.Message):
    __slots__ = ()
    CPU_FAMILY_FIELD_NUMBER: _ClassVar[int]
    CPU_SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    CPU_EXT_FIELD_NUMBER: _ClassVar[int]
    BRAND_FIELD_NUMBER: _ClassVar[int]
    BRAND_FLAGS_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    OS_EXT_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_INFORMATION_STRING_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    cpu_family: CpuFamily
    cpu_subtype: int
    cpu_ext: int
    brand: Brand
    brand_flags: int
    os: Os
    os_version: int
    os_ext: int
    system_information_string: str
    device_id: str
    def __init__(self, cpu_family: _Optional[_Union[CpuFamily, str]] = ..., cpu_subtype: _Optional[int] = ..., cpu_ext: _Optional[int] = ..., brand: _Optional[_Union[Brand, str]] = ..., brand_flags: _Optional[int] = ..., os: _Optional[_Union[Os, str]] = ..., os_version: _Optional[int] = ..., os_ext: _Optional[int] = ..., system_information_string: _Optional[str] = ..., device_id: _Optional[str] = ...) -> None: ...

class LibspotifyAppKey(_message.Message):
    __slots__ = ()
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DEVKEY_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    USERAGENT_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_HASH_FIELD_NUMBER: _ClassVar[int]
    version: int
    devkey: bytes
    signature: bytes
    useragent: str
    callback_hash: bytes
    def __init__(self, version: _Optional[int] = ..., devkey: _Optional[bytes] = ..., signature: _Optional[bytes] = ..., useragent: _Optional[str] = ..., callback_hash: _Optional[bytes] = ...) -> None: ...

class ClientInfo(_message.Message):
    __slots__ = ()
    LIMITED_FIELD_NUMBER: _ClassVar[int]
    FB_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    limited: bool
    fb: ClientInfoFacebook
    language: str
    def __init__(self, limited: _Optional[bool] = ..., fb: _Optional[_Union[ClientInfoFacebook, _Mapping]] = ..., language: _Optional[str] = ...) -> None: ...

class ClientInfoFacebook(_message.Message):
    __slots__ = ()
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    machine_id: str
    def __init__(self, machine_id: _Optional[str] = ...) -> None: ...

class APWelcome(_message.Message):
    __slots__ = ()
    CANONICAL_USERNAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_TYPE_LOGGED_IN_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_TYPE_LOGGED_IN_FIELD_NUMBER: _ClassVar[int]
    REUSABLE_AUTH_CREDENTIALS_TYPE_FIELD_NUMBER: _ClassVar[int]
    REUSABLE_AUTH_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    LFS_SECRET_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_INFO_FIELD_NUMBER: _ClassVar[int]
    FB_FIELD_NUMBER: _ClassVar[int]
    canonical_username: str
    account_type_logged_in: AccountType
    credentials_type_logged_in: AccountType
    reusable_auth_credentials_type: AuthenticationType
    reusable_auth_credentials: bytes
    lfs_secret: bytes
    account_info: AccountInfo
    fb: AccountInfoFacebook
    def __init__(self, canonical_username: _Optional[str] = ..., account_type_logged_in: _Optional[_Union[AccountType, str]] = ..., credentials_type_logged_in: _Optional[_Union[AccountType, str]] = ..., reusable_auth_credentials_type: _Optional[_Union[AuthenticationType, str]] = ..., reusable_auth_credentials: _Optional[bytes] = ..., lfs_secret: _Optional[bytes] = ..., account_info: _Optional[_Union[AccountInfo, _Mapping]] = ..., fb: _Optional[_Union[AccountInfoFacebook, _Mapping]] = ...) -> None: ...

class AccountInfo(_message.Message):
    __slots__ = ()
    SPOTIFY_FIELD_NUMBER: _ClassVar[int]
    FACEBOOK_FIELD_NUMBER: _ClassVar[int]
    spotify: AccountInfoSpotify
    facebook: AccountInfoFacebook
    def __init__(self, spotify: _Optional[_Union[AccountInfoSpotify, _Mapping]] = ..., facebook: _Optional[_Union[AccountInfoFacebook, _Mapping]] = ...) -> None: ...

class AccountInfoSpotify(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AccountInfoFacebook(_message.Message):
    __slots__ = ()
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    machine_id: str
    def __init__(self, access_token: _Optional[str] = ..., machine_id: _Optional[str] = ...) -> None: ...
