from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectivitySdkData(_message.Message):
    __slots__ = ()
    PLATFORM_SPECIFIC_DATA_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    platform_specific_data: PlatformSpecificData
    device_id: str
    def __init__(self, platform_specific_data: _Optional[_Union[PlatformSpecificData, _Mapping]] = ..., device_id: _Optional[str] = ...) -> None: ...

class PlatformSpecificData(_message.Message):
    __slots__ = ()
    ANDROID_FIELD_NUMBER: _ClassVar[int]
    IOS_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_MACOS_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_WINDOWS_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_LINUX_FIELD_NUMBER: _ClassVar[int]
    android: NativeAndroidData
    ios: NativeIOSData
    desktop_macos: NativeDesktopMacOSData
    desktop_windows: NativeDesktopWindowsData
    desktop_linux: NativeDesktopLinuxData
    def __init__(self, android: _Optional[_Union[NativeAndroidData, _Mapping]] = ..., ios: _Optional[_Union[NativeIOSData, _Mapping]] = ..., desktop_macos: _Optional[_Union[NativeDesktopMacOSData, _Mapping]] = ..., desktop_windows: _Optional[_Union[NativeDesktopWindowsData, _Mapping]] = ..., desktop_linux: _Optional[_Union[NativeDesktopLinuxData, _Mapping]] = ...) -> None: ...

class NativeAndroidData(_message.Message):
    __slots__ = ()
    SCREEN_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    ANDROID_VERSION_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_STR_FIELD_NUMBER: _ClassVar[int]
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    VENDOR_2_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_VALUE_8_FIELD_NUMBER: _ClassVar[int]
    screen_dimensions: Screen
    android_version: str
    api_version: int
    device_name: str
    model_str: str
    vendor: str
    vendor_2: str
    unknown_value_8: int
    def __init__(self, screen_dimensions: _Optional[_Union[Screen, _Mapping]] = ..., android_version: _Optional[str] = ..., api_version: _Optional[int] = ..., device_name: _Optional[str] = ..., model_str: _Optional[str] = ..., vendor: _Optional[str] = ..., vendor_2: _Optional[str] = ..., unknown_value_8: _Optional[int] = ...) -> None: ...

class NativeIOSData(_message.Message):
    __slots__ = ()
    USER_INTERFACE_IDIOM_FIELD_NUMBER: _ClassVar[int]
    TARGET_IPHONE_SIMULATOR_FIELD_NUMBER: _ClassVar[int]
    HW_MACHINE_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_VERSION_FIELD_NUMBER: _ClassVar[int]
    SIMULATOR_MODEL_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    user_interface_idiom: int
    target_iphone_simulator: bool
    hw_machine: str
    system_version: str
    simulator_model_identifier: str
    def __init__(self, user_interface_idiom: _Optional[int] = ..., target_iphone_simulator: _Optional[bool] = ..., hw_machine: _Optional[str] = ..., system_version: _Optional[str] = ..., simulator_model_identifier: _Optional[str] = ...) -> None: ...

class NativeDesktopWindowsData(_message.Message):
    __slots__ = ()
    OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    OS_BUILD_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_VALUE_5_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_VALUE_6_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FILE_MACHINE_FIELD_NUMBER: _ClassVar[int]
    PE_MACHINE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_VALUE_10_FIELD_NUMBER: _ClassVar[int]
    os_version: int
    os_build: int
    platform_id: int
    unknown_value_5: int
    unknown_value_6: int
    image_file_machine: int
    pe_machine: int
    unknown_value_10: bool
    def __init__(self, os_version: _Optional[int] = ..., os_build: _Optional[int] = ..., platform_id: _Optional[int] = ..., unknown_value_5: _Optional[int] = ..., unknown_value_6: _Optional[int] = ..., image_file_machine: _Optional[int] = ..., pe_machine: _Optional[int] = ..., unknown_value_10: _Optional[bool] = ...) -> None: ...

class NativeDesktopLinuxData(_message.Message):
    __slots__ = ()
    SYSTEM_NAME_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_RELEASE_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_VERSION_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_FIELD_NUMBER: _ClassVar[int]
    system_name: str
    system_release: str
    system_version: str
    hardware: str
    def __init__(self, system_name: _Optional[str] = ..., system_release: _Optional[str] = ..., system_version: _Optional[str] = ..., hardware: _Optional[str] = ...) -> None: ...

class NativeDesktopMacOSData(_message.Message):
    __slots__ = ()
    SYSTEM_VERSION_FIELD_NUMBER: _ClassVar[int]
    HW_MODEL_FIELD_NUMBER: _ClassVar[int]
    COMPILED_CPU_TYPE_FIELD_NUMBER: _ClassVar[int]
    system_version: str
    hw_model: str
    compiled_cpu_type: str
    def __init__(self, system_version: _Optional[str] = ..., hw_model: _Optional[str] = ..., compiled_cpu_type: _Optional[str] = ...) -> None: ...

class Screen(_message.Message):
    __slots__ = ()
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    DENSITY_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_VALUE_4_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_VALUE_5_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    density: int
    unknown_value_4: int
    unknown_value_5: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., density: _Optional[int] = ..., unknown_value_4: _Optional[int] = ..., unknown_value_5: _Optional[int] = ...) -> None: ...
