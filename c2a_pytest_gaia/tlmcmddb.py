from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


@dataclass
class TelemetryMetadata:
    packet_id: int

    @staticmethod
    def build(dict):
        return TelemetryMetadata(
            packet_id=dict["packet_id"],
        )


class VariableType(Enum):
    int8_t = auto()
    int16_t = auto()
    int32_t = auto()
    uint8_t = auto()
    uint16_t = auto()
    uint32_t = auto()
    float = auto()
    double = auto()


@dataclass
class TelemetryField:
    name: str
    variable_type: VariableType
    conversion_info: Any

    @staticmethod
    def build(variable_type_str, dict):
        return TelemetryField(
            name=dict["name"],
            variable_type=VariableType[variable_type_str],
            conversion_info=dict["conversion_info"],
        )


@dataclass
class Telemetry:
    name: str
    metadata: TelemetryMetadata
    fields: list[TelemetryField]

    @staticmethod
    def build(dict):
        return Telemetry(
            name=dict["name"],
            metadata=TelemetryMetadata.build(dict["metadata"]),
            fields=[
                TelemetryField.build(
                    entry["onboard_software_info"]["variable_type"], sub_entry
                )
                for entry in dict["entries"]
                if entry["type"] == "FIELD_GROUP"
                for sub_entry in entry["sub_entries"]
                if sub_entry["type"] == "FIELD"
            ],
        )


@dataclass
class TelemetryDatabase:
    telemetries: list[Telemetry]

    @staticmethod
    def build(dict):
        return TelemetryDatabase(
            [Telemetry.build(entry) for entry in dict["telemetries"]]
        )


class DataType(Enum):
    int8_t = auto()
    int16_t = auto()
    int32_t = auto()
    uint8_t = auto()
    uint16_t = auto()
    uint32_t = auto()
    float = auto()
    double = auto()
    raw = auto()


@dataclass
class Parameter:
    data_type: DataType

    @staticmethod
    def build(dict):
        return Parameter(data_type=DataType[dict["data_type"]])


@dataclass
class Command:
    name: str
    code: int
    parameters: list[Parameter]

    @staticmethod
    def build(dict):
        return Command(
            name=dict["name"],
            code=dict["code"],
            parameters=[Parameter.build(p) for p in dict["parameters"]],
        )


@dataclass
class CommandDatabase:
    commands: list[Command]

    @staticmethod
    def build(dict):
        return CommandDatabase(
            [
                Command.build(entry)
                for entry in dict["entries"]
                if entry["type"] == "COMMAND"
            ]
        )


@dataclass
class Component:
    name: str
    tlm: TelemetryDatabase
    cmd: CommandDatabase

    @staticmethod
    def build(dict):
        return Component(
            name=dict["name"],
            tlm=TelemetryDatabase.build(dict["tlm"]),
            cmd=CommandDatabase.build(dict["cmd"]),
        )


@dataclass
class Database:
    components: list[Component]

    @staticmethod
    def build(dict):
        return Database([Component.build(c) for c in dict["components"]])
