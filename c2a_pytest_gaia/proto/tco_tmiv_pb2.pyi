from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class Tco(_message.Message):
    __slots__ = ["name", "params"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    name: str
    params: _containers.RepeatedCompositeFieldContainer[TcoParam]
    def __init__(
        self,
        name: _Optional[str] = ...,
        params: _Optional[_Iterable[_Union[TcoParam, _Mapping]]] = ...,
    ) -> None: ...

class TcoParam(_message.Message):
    __slots__ = ["bytes", "double", "integer", "name"]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    INTEGER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    bytes: bytes
    double: float
    integer: int
    name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        integer: _Optional[int] = ...,
        double: _Optional[float] = ...,
        bytes: _Optional[bytes] = ...,
    ) -> None: ...

class Tmiv(_message.Message):
    __slots__ = ["fields", "name", "plugin_received_time", "timestamp"]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_RECEIVED_TIME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[TmivField]
    name: str
    plugin_received_time: int
    timestamp: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        plugin_received_time: _Optional[int] = ...,
        fields: _Optional[_Iterable[_Union[TmivField, _Mapping]]] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class TmivField(_message.Message):
    __slots__ = ["bytes", "double", "enum", "integer", "name", "string"]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    ENUM_FIELD_NUMBER: _ClassVar[int]
    INTEGER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    bytes: bytes
    double: float
    enum: str
    integer: int
    name: str
    string: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        string: _Optional[str] = ...,
        double: _Optional[float] = ...,
        integer: _Optional[int] = ...,
        enum: _Optional[str] = ...,
        bytes: _Optional[bytes] = ...,
    ) -> None: ...
