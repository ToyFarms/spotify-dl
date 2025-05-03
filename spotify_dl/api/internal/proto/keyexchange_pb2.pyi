from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Product(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRODUCT_CLIENT: _ClassVar[Product]
    PRODUCT_LIBSPOTIFY: _ClassVar[Product]
    PRODUCT_MOBILE: _ClassVar[Product]
    PRODUCT_PARTNER: _ClassVar[Product]
    PRODUCT_LIBSPOTIFY_EMBEDDED: _ClassVar[Product]

class ProductFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRODUCT_FLAG_NONE: _ClassVar[ProductFlags]
    PRODUCT_FLAG_DEV_BUILD: _ClassVar[ProductFlags]

class Platform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PLATFORM_WIN32_X86: _ClassVar[Platform]
    PLATFORM_OSX_X86: _ClassVar[Platform]
    PLATFORM_LINUX_X86: _ClassVar[Platform]
    PLATFORM_IPHONE_ARM: _ClassVar[Platform]
    PLATFORM_S60_ARM: _ClassVar[Platform]
    PLATFORM_OSX_PPC: _ClassVar[Platform]
    PLATFORM_ANDROID_ARM: _ClassVar[Platform]
    PLATFORM_WINDOWS_CE_ARM: _ClassVar[Platform]
    PLATFORM_LINUX_X86_64: _ClassVar[Platform]
    PLATFORM_OSX_X86_64: _ClassVar[Platform]
    PLATFORM_PALM_ARM: _ClassVar[Platform]
    PLATFORM_LINUX_SH: _ClassVar[Platform]
    PLATFORM_FREEBSD_X86: _ClassVar[Platform]
    PLATFORM_FREEBSD_X86_64: _ClassVar[Platform]
    PLATFORM_BLACKBERRY_ARM: _ClassVar[Platform]
    PLATFORM_SONOS: _ClassVar[Platform]
    PLATFORM_LINUX_MIPS: _ClassVar[Platform]
    PLATFORM_LINUX_ARM: _ClassVar[Platform]
    PLATFORM_LOGITECH_ARM: _ClassVar[Platform]
    PLATFORM_LINUX_BLACKFIN: _ClassVar[Platform]
    PLATFORM_WP7_ARM: _ClassVar[Platform]
    PLATFORM_ONKYO_ARM: _ClassVar[Platform]
    PLATFORM_QNXNTO_ARM: _ClassVar[Platform]
    PLATFORM_BCO_ARM: _ClassVar[Platform]
    PLATFORM_WEBPLAYER: _ClassVar[Platform]
    PLATFORM_WP8_ARM: _ClassVar[Platform]
    PLATFORM_WP8_X86: _ClassVar[Platform]
    PLATFORM_WINRT_ARM: _ClassVar[Platform]
    PLATFORM_WINRT_X86: _ClassVar[Platform]
    PLATFORM_WINRT_X86_64: _ClassVar[Platform]
    PLATFORM_FRONTIER: _ClassVar[Platform]
    PLATFORM_AMIGA_PPC: _ClassVar[Platform]
    PLATFORM_NANRADIO_NRX901: _ClassVar[Platform]
    PLATFORM_HARMAN_ARM: _ClassVar[Platform]
    PLATFORM_SONY_PS3: _ClassVar[Platform]
    PLATFORM_SONY_PS4: _ClassVar[Platform]
    PLATFORM_IPHONE_ARM64: _ClassVar[Platform]
    PLATFORM_RTEMS_PPC: _ClassVar[Platform]
    PLATFORM_GENERIC_PARTNER: _ClassVar[Platform]
    PLATFORM_WIN32_X86_64: _ClassVar[Platform]
    PLATFORM_WATCHOS: _ClassVar[Platform]

class Fingerprint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FINGERPRINT_GRAIN: _ClassVar[Fingerprint]
    FINGERPRINT_HMAC_RIPEMD: _ClassVar[Fingerprint]

class Cryptosuite(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRYPTO_SUITE_SHANNON: _ClassVar[Cryptosuite]
    CRYPTO_SUITE_RC4_SHA1_HMAC: _ClassVar[Cryptosuite]

class Powscheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POW_HASH_CASH: _ClassVar[Powscheme]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ProtocolError: _ClassVar[ErrorCode]
    TryAnotherAP: _ClassVar[ErrorCode]
    BadConnectionId: _ClassVar[ErrorCode]
    TravelRestriction: _ClassVar[ErrorCode]
    PremiumAccountRequired: _ClassVar[ErrorCode]
    BadCredentials: _ClassVar[ErrorCode]
    CouldNotValidateCredentials: _ClassVar[ErrorCode]
    AccountExists: _ClassVar[ErrorCode]
    ExtraVerificationRequired: _ClassVar[ErrorCode]
    InvalidAppKey: _ClassVar[ErrorCode]
    ApplicationBanned: _ClassVar[ErrorCode]
PRODUCT_CLIENT: Product
PRODUCT_LIBSPOTIFY: Product
PRODUCT_MOBILE: Product
PRODUCT_PARTNER: Product
PRODUCT_LIBSPOTIFY_EMBEDDED: Product
PRODUCT_FLAG_NONE: ProductFlags
PRODUCT_FLAG_DEV_BUILD: ProductFlags
PLATFORM_WIN32_X86: Platform
PLATFORM_OSX_X86: Platform
PLATFORM_LINUX_X86: Platform
PLATFORM_IPHONE_ARM: Platform
PLATFORM_S60_ARM: Platform
PLATFORM_OSX_PPC: Platform
PLATFORM_ANDROID_ARM: Platform
PLATFORM_WINDOWS_CE_ARM: Platform
PLATFORM_LINUX_X86_64: Platform
PLATFORM_OSX_X86_64: Platform
PLATFORM_PALM_ARM: Platform
PLATFORM_LINUX_SH: Platform
PLATFORM_FREEBSD_X86: Platform
PLATFORM_FREEBSD_X86_64: Platform
PLATFORM_BLACKBERRY_ARM: Platform
PLATFORM_SONOS: Platform
PLATFORM_LINUX_MIPS: Platform
PLATFORM_LINUX_ARM: Platform
PLATFORM_LOGITECH_ARM: Platform
PLATFORM_LINUX_BLACKFIN: Platform
PLATFORM_WP7_ARM: Platform
PLATFORM_ONKYO_ARM: Platform
PLATFORM_QNXNTO_ARM: Platform
PLATFORM_BCO_ARM: Platform
PLATFORM_WEBPLAYER: Platform
PLATFORM_WP8_ARM: Platform
PLATFORM_WP8_X86: Platform
PLATFORM_WINRT_ARM: Platform
PLATFORM_WINRT_X86: Platform
PLATFORM_WINRT_X86_64: Platform
PLATFORM_FRONTIER: Platform
PLATFORM_AMIGA_PPC: Platform
PLATFORM_NANRADIO_NRX901: Platform
PLATFORM_HARMAN_ARM: Platform
PLATFORM_SONY_PS3: Platform
PLATFORM_SONY_PS4: Platform
PLATFORM_IPHONE_ARM64: Platform
PLATFORM_RTEMS_PPC: Platform
PLATFORM_GENERIC_PARTNER: Platform
PLATFORM_WIN32_X86_64: Platform
PLATFORM_WATCHOS: Platform
FINGERPRINT_GRAIN: Fingerprint
FINGERPRINT_HMAC_RIPEMD: Fingerprint
CRYPTO_SUITE_SHANNON: Cryptosuite
CRYPTO_SUITE_RC4_SHA1_HMAC: Cryptosuite
POW_HASH_CASH: Powscheme
ProtocolError: ErrorCode
TryAnotherAP: ErrorCode
BadConnectionId: ErrorCode
TravelRestriction: ErrorCode
PremiumAccountRequired: ErrorCode
BadCredentials: ErrorCode
CouldNotValidateCredentials: ErrorCode
AccountExists: ErrorCode
ExtraVerificationRequired: ErrorCode
InvalidAppKey: ErrorCode
ApplicationBanned: ErrorCode

class ClientHello(_message.Message):
    __slots__ = ("build_info", "fingerprints_supported", "cryptosuites_supported", "powschemes_supported", "login_crypto_hello", "client_nonce", "padding", "feature_set")
    BUILD_INFO_FIELD_NUMBER: _ClassVar[int]
    FINGERPRINTS_SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    CRYPTOSUITES_SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    POWSCHEMES_SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    LOGIN_CRYPTO_HELLO_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NONCE_FIELD_NUMBER: _ClassVar[int]
    PADDING_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SET_FIELD_NUMBER: _ClassVar[int]
    build_info: BuildInfo
    fingerprints_supported: _containers.RepeatedScalarFieldContainer[Fingerprint]
    cryptosuites_supported: _containers.RepeatedScalarFieldContainer[Cryptosuite]
    powschemes_supported: _containers.RepeatedScalarFieldContainer[Powscheme]
    login_crypto_hello: LoginCryptoHelloUnion
    client_nonce: bytes
    padding: bytes
    feature_set: FeatureSet
    def __init__(self, build_info: _Optional[_Union[BuildInfo, _Mapping]] = ..., fingerprints_supported: _Optional[_Iterable[_Union[Fingerprint, str]]] = ..., cryptosuites_supported: _Optional[_Iterable[_Union[Cryptosuite, str]]] = ..., powschemes_supported: _Optional[_Iterable[_Union[Powscheme, str]]] = ..., login_crypto_hello: _Optional[_Union[LoginCryptoHelloUnion, _Mapping]] = ..., client_nonce: _Optional[bytes] = ..., padding: _Optional[bytes] = ..., feature_set: _Optional[_Union[FeatureSet, _Mapping]] = ...) -> None: ...

class BuildInfo(_message.Message):
    __slots__ = ("product", "product_flags", "platform", "version")
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    product: Product
    product_flags: _containers.RepeatedScalarFieldContainer[ProductFlags]
    platform: Platform
    version: int
    def __init__(self, product: _Optional[_Union[Product, str]] = ..., product_flags: _Optional[_Iterable[_Union[ProductFlags, str]]] = ..., platform: _Optional[_Union[Platform, str]] = ..., version: _Optional[int] = ...) -> None: ...

class LoginCryptoHelloUnion(_message.Message):
    __slots__ = ("diffie_hellman",)
    DIFFIE_HELLMAN_FIELD_NUMBER: _ClassVar[int]
    diffie_hellman: LoginCryptoDiffieHellmanHello
    def __init__(self, diffie_hellman: _Optional[_Union[LoginCryptoDiffieHellmanHello, _Mapping]] = ...) -> None: ...

class LoginCryptoDiffieHellmanHello(_message.Message):
    __slots__ = ("gc", "server_keys_known")
    GC_FIELD_NUMBER: _ClassVar[int]
    SERVER_KEYS_KNOWN_FIELD_NUMBER: _ClassVar[int]
    gc: bytes
    server_keys_known: int
    def __init__(self, gc: _Optional[bytes] = ..., server_keys_known: _Optional[int] = ...) -> None: ...

class FeatureSet(_message.Message):
    __slots__ = ("autoupdate2", "current_location")
    AUTOUPDATE2_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LOCATION_FIELD_NUMBER: _ClassVar[int]
    autoupdate2: bool
    current_location: bool
    def __init__(self, autoupdate2: bool = ..., current_location: bool = ...) -> None: ...

class APResponseMessage(_message.Message):
    __slots__ = ("challenge", "upgrade", "login_failed")
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_FIELD_NUMBER: _ClassVar[int]
    LOGIN_FAILED_FIELD_NUMBER: _ClassVar[int]
    challenge: APChallenge
    upgrade: UpgradeRequiredMessage
    login_failed: APLoginFailed
    def __init__(self, challenge: _Optional[_Union[APChallenge, _Mapping]] = ..., upgrade: _Optional[_Union[UpgradeRequiredMessage, _Mapping]] = ..., login_failed: _Optional[_Union[APLoginFailed, _Mapping]] = ...) -> None: ...

class APChallenge(_message.Message):
    __slots__ = ("login_crypto_challenge", "fingerprint_challenge", "pow_challenge", "crypto_challenge", "server_nonce", "padding")
    LOGIN_CRYPTO_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    FINGERPRINT_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    POW_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    CRYPTO_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    SERVER_NONCE_FIELD_NUMBER: _ClassVar[int]
    PADDING_FIELD_NUMBER: _ClassVar[int]
    login_crypto_challenge: LoginCryptoChallengeUnion
    fingerprint_challenge: FingerprintChallengeUnion
    pow_challenge: PoWChallengeUnion
    crypto_challenge: CryptoChallengeUnion
    server_nonce: bytes
    padding: bytes
    def __init__(self, login_crypto_challenge: _Optional[_Union[LoginCryptoChallengeUnion, _Mapping]] = ..., fingerprint_challenge: _Optional[_Union[FingerprintChallengeUnion, _Mapping]] = ..., pow_challenge: _Optional[_Union[PoWChallengeUnion, _Mapping]] = ..., crypto_challenge: _Optional[_Union[CryptoChallengeUnion, _Mapping]] = ..., server_nonce: _Optional[bytes] = ..., padding: _Optional[bytes] = ...) -> None: ...

class LoginCryptoChallengeUnion(_message.Message):
    __slots__ = ("diffie_hellman",)
    DIFFIE_HELLMAN_FIELD_NUMBER: _ClassVar[int]
    diffie_hellman: LoginCryptoDiffieHellmanChallenge
    def __init__(self, diffie_hellman: _Optional[_Union[LoginCryptoDiffieHellmanChallenge, _Mapping]] = ...) -> None: ...

class LoginCryptoDiffieHellmanChallenge(_message.Message):
    __slots__ = ("gs", "server_signature_key", "gs_signature")
    GS_FIELD_NUMBER: _ClassVar[int]
    SERVER_SIGNATURE_KEY_FIELD_NUMBER: _ClassVar[int]
    GS_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    gs: bytes
    server_signature_key: int
    gs_signature: bytes
    def __init__(self, gs: _Optional[bytes] = ..., server_signature_key: _Optional[int] = ..., gs_signature: _Optional[bytes] = ...) -> None: ...

class FingerprintChallengeUnion(_message.Message):
    __slots__ = ("grain", "hmac_ripemd")
    GRAIN_FIELD_NUMBER: _ClassVar[int]
    HMAC_RIPEMD_FIELD_NUMBER: _ClassVar[int]
    grain: FingerprintGrainChallenge
    hmac_ripemd: FingerprintHmacRipemdChallenge
    def __init__(self, grain: _Optional[_Union[FingerprintGrainChallenge, _Mapping]] = ..., hmac_ripemd: _Optional[_Union[FingerprintHmacRipemdChallenge, _Mapping]] = ...) -> None: ...

class FingerprintGrainChallenge(_message.Message):
    __slots__ = ("kek",)
    KEK_FIELD_NUMBER: _ClassVar[int]
    kek: bytes
    def __init__(self, kek: _Optional[bytes] = ...) -> None: ...

class FingerprintHmacRipemdChallenge(_message.Message):
    __slots__ = ("challenge",)
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    challenge: bytes
    def __init__(self, challenge: _Optional[bytes] = ...) -> None: ...

class PoWChallengeUnion(_message.Message):
    __slots__ = ("hash_cash",)
    HASH_CASH_FIELD_NUMBER: _ClassVar[int]
    hash_cash: PoWHashCashChallenge
    def __init__(self, hash_cash: _Optional[_Union[PoWHashCashChallenge, _Mapping]] = ...) -> None: ...

class PoWHashCashChallenge(_message.Message):
    __slots__ = ("prefix", "length", "target")
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    prefix: bytes
    length: int
    target: int
    def __init__(self, prefix: _Optional[bytes] = ..., length: _Optional[int] = ..., target: _Optional[int] = ...) -> None: ...

class CryptoChallengeUnion(_message.Message):
    __slots__ = ("shannon", "rc4_sha1_hmac")
    SHANNON_FIELD_NUMBER: _ClassVar[int]
    RC4_SHA1_HMAC_FIELD_NUMBER: _ClassVar[int]
    shannon: CryptoShannonChallenge
    rc4_sha1_hmac: CryptoRc4Sha1HmacChallenge
    def __init__(self, shannon: _Optional[_Union[CryptoShannonChallenge, _Mapping]] = ..., rc4_sha1_hmac: _Optional[_Union[CryptoRc4Sha1HmacChallenge, _Mapping]] = ...) -> None: ...

class CryptoShannonChallenge(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CryptoRc4Sha1HmacChallenge(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpgradeRequiredMessage(_message.Message):
    __slots__ = ("upgrade_signed_part", "signature", "http_suffix")
    UPGRADE_SIGNED_PART_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    HTTP_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    upgrade_signed_part: bytes
    signature: bytes
    http_suffix: str
    def __init__(self, upgrade_signed_part: _Optional[bytes] = ..., signature: _Optional[bytes] = ..., http_suffix: _Optional[str] = ...) -> None: ...

class APLoginFailed(_message.Message):
    __slots__ = ("error_code", "retry_delay", "expiry", "error_description")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    RETRY_DELAY_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    ERROR_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    error_code: ErrorCode
    retry_delay: int
    expiry: int
    error_description: str
    def __init__(self, error_code: _Optional[_Union[ErrorCode, str]] = ..., retry_delay: _Optional[int] = ..., expiry: _Optional[int] = ..., error_description: _Optional[str] = ...) -> None: ...

class ClientResponsePlaintext(_message.Message):
    __slots__ = ("login_crypto_response", "pow_response", "crypto_response")
    LOGIN_CRYPTO_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    POW_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CRYPTO_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    login_crypto_response: LoginCryptoResponseUnion
    pow_response: PoWResponseUnion
    crypto_response: CryptoResponseUnion
    def __init__(self, login_crypto_response: _Optional[_Union[LoginCryptoResponseUnion, _Mapping]] = ..., pow_response: _Optional[_Union[PoWResponseUnion, _Mapping]] = ..., crypto_response: _Optional[_Union[CryptoResponseUnion, _Mapping]] = ...) -> None: ...

class LoginCryptoResponseUnion(_message.Message):
    __slots__ = ("diffie_hellman",)
    DIFFIE_HELLMAN_FIELD_NUMBER: _ClassVar[int]
    diffie_hellman: LoginCryptoDiffieHellmanResponse
    def __init__(self, diffie_hellman: _Optional[_Union[LoginCryptoDiffieHellmanResponse, _Mapping]] = ...) -> None: ...

class LoginCryptoDiffieHellmanResponse(_message.Message):
    __slots__ = ("hmac",)
    HMAC_FIELD_NUMBER: _ClassVar[int]
    hmac: bytes
    def __init__(self, hmac: _Optional[bytes] = ...) -> None: ...

class PoWResponseUnion(_message.Message):
    __slots__ = ("hash_cash",)
    HASH_CASH_FIELD_NUMBER: _ClassVar[int]
    hash_cash: PoWHashCashResponse
    def __init__(self, hash_cash: _Optional[_Union[PoWHashCashResponse, _Mapping]] = ...) -> None: ...

class PoWHashCashResponse(_message.Message):
    __slots__ = ("hash_suffix",)
    HASH_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    hash_suffix: bytes
    def __init__(self, hash_suffix: _Optional[bytes] = ...) -> None: ...

class CryptoResponseUnion(_message.Message):
    __slots__ = ("shannon", "rc4_sha1_hmac")
    SHANNON_FIELD_NUMBER: _ClassVar[int]
    RC4_SHA1_HMAC_FIELD_NUMBER: _ClassVar[int]
    shannon: CryptoShannonResponse
    rc4_sha1_hmac: CryptoRc4Sha1HmacResponse
    def __init__(self, shannon: _Optional[_Union[CryptoShannonResponse, _Mapping]] = ..., rc4_sha1_hmac: _Optional[_Union[CryptoRc4Sha1HmacResponse, _Mapping]] = ...) -> None: ...

class CryptoShannonResponse(_message.Message):
    __slots__ = ("dummy",)
    DUMMY_FIELD_NUMBER: _ClassVar[int]
    dummy: int
    def __init__(self, dummy: _Optional[int] = ...) -> None: ...

class CryptoRc4Sha1HmacResponse(_message.Message):
    __slots__ = ("dummy",)
    DUMMY_FIELD_NUMBER: _ClassVar[int]
    dummy: int
    def __init__(self, dummy: _Optional[int] = ...) -> None: ...
