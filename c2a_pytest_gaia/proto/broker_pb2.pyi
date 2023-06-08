import tco_tmiv_pb2 as _tco_tmiv_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CommandStreamRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CommandStreamResponse(_message.Message):
    __slots__ = ["tco", "tco_json"]
    TCO_FIELD_NUMBER: _ClassVar[int]
    TCO_JSON_FIELD_NUMBER: _ClassVar[int]
    tco: _tco_tmiv_pb2.Tco
    tco_json: str
    def __init__(
        self,
        tco_json: _Optional[str] = ...,
        tco: _Optional[_Union[_tco_tmiv_pb2.Tco, _Mapping]] = ...,
    ) -> None: ...

class GetLastReceivedTelemetryRequest(_message.Message):
    __slots__ = ["telemetry_name"]
    TELEMETRY_NAME_FIELD_NUMBER: _ClassVar[int]
    telemetry_name: str
    def __init__(self, telemetry_name: _Optional[str] = ...) -> None: ...

class GetLastReceivedTelemetryResponse(_message.Message):
    __slots__ = ["tmiv"]
    TMIV_FIELD_NUMBER: _ClassVar[int]
    tmiv: _tco_tmiv_pb2.Tmiv
    def __init__(
        self, tmiv: _Optional[_Union[_tco_tmiv_pb2.Tmiv, _Mapping]] = ...
    ) -> None: ...

class PostCommandRequest(_message.Message):
    __slots__ = ["tco"]
    TCO_FIELD_NUMBER: _ClassVar[int]
    tco: _tco_tmiv_pb2.Tco
    def __init__(
        self, tco: _Optional[_Union[_tco_tmiv_pb2.Tco, _Mapping]] = ...
    ) -> None: ...

class PostCommandResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PostTelemetryRequest(_message.Message):
    __slots__ = ["tmiv", "tmiv_json"]
    TMIV_FIELD_NUMBER: _ClassVar[int]
    TMIV_JSON_FIELD_NUMBER: _ClassVar[int]
    tmiv: _tco_tmiv_pb2.Tmiv
    tmiv_json: str
    def __init__(
        self,
        tmiv_json: _Optional[str] = ...,
        tmiv: _Optional[_Union[_tco_tmiv_pb2.Tmiv, _Mapping]] = ...,
    ) -> None: ...

class PostTelemetryResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TelemetryStreamRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TelemetryStreamResponse(_message.Message):
    __slots__ = ["tmiv"]
    TMIV_FIELD_NUMBER: _ClassVar[int]
    tmiv: _tco_tmiv_pb2.Tmiv
    def __init__(
        self, tmiv: _Optional[_Union[_tco_tmiv_pb2.Tmiv, _Mapping]] = ...
    ) -> None: ...
