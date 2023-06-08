import time
from typing import Optional
import grpc
from .proto import tco_tmiv_pb2, broker_pb2, broker_pb2_grpc
from .tlmcmddb import DataType, Database, Telemetry, TelemetryField, VariableType, Command

default_obc_info = {
    "name": "MOBC",
    "hk_tlm_info": {
        "tlm_name": "HK",
        "cmd_counter": "OBC.GS_CMD.COUNTER",
        "cmd_last_exec_id": "OBC.GS_CMD.LAST_EXEC.ID",
        "cmd_last_exec_sts": "OBC.GS_CMD.LAST_EXEC.EXEC_STS",
    },
}


class Operation:
    tlmcmddb: Database
    stub: broker_pb2_grpc.BrokerStub
    def __init__(
        self, tlmcmddb, url="localhost:8900", obc_info: dict = default_obc_info
    ):
        self.tlmcmddb = Database.build(tlmcmddb)
        self.stub = broker_pb2_grpc.BrokerStub(grpc.insecure_channel(url))
        self.obc_info = obc_info

    def _get_tlm_def_by_tlm_id(self, tlm_id: int) -> tuple[str, Telemetry]:
        return next(
            (component_def.name, tlm_def)
            for component_def in self.tlmcmddb.components
            for tlm_def in component_def.tlm.telemetries
            if tlm_def.metadata.packet_id == tlm_id
        )

    def _get_tlm_field_def_by_tmiv_field_name(self, tlm_def: Telemetry, tmiv_field_name: str) -> TelemetryField:
        return next(
            tlm_field_def
            for tlm_field_def in tlm_def.fields
            if tlm_field_def.name == tmiv_field_name
        )

    def _build_tlm_field_pair(self, tlm_def: Telemetry, tmiv_field: tco_tmiv_pb2.TmivField):
        tmiv_field_name = tmiv_field.name
        which = tmiv_field.WhichOneof("value")
        if which == "integer":
            value = tmiv_field.integer
        elif which == "double":
            value = tmiv_field.double
        elif which == "enum":
            value = tmiv_field.enum
        tlm_field_def = self._get_tlm_field_def_by_tmiv_field_name(tlm_def, tmiv_field_name)
        variable_type = tlm_field_def.variable_type
        field_name = "%s.%s" % (tlm_def.name, tlm_field_def.name)
        if tlm_field_def.conversion_info == "HEX":
            if variable_type == VariableType.int8_t:
                return (field_name, "0x%0.2x" % value)
            elif variable_type == VariableType.uint8_t:
                return (field_name, "0x%0.2x" % value)
            elif variable_type == VariableType.int16_t:
                return (field_name, "0x%0.4x" % value)
            elif variable_type == VariableType.uint16_t:
                return (field_name, "0x%0.4x" % value)
            elif variable_type == VariableType.int32_t:
                return (field_name, "0x%0.8x" % value)
            elif variable_type == VariableType.uint32_t:
                return (field_name, "0x%0.8x" % value)
            else:
                return (field_name, value)
        else:
            return (field_name, value)

    def get_latest_tlm(self, tlm_code_id: int) -> tuple[dict, str]:
        (component_name, tlm_def) = self._get_tlm_def_by_tlm_id(tlm_code_id)
        telemetry_name = "RT.%s.%s" % (component_name, tlm_def.name)
        try:
            resp = self.stub.GetLastReceivedTelemetry(
                broker_pb2.GetLastReceivedTelemetryRequest(
                    telemetry_name=telemetry_name
                )
            )
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                return {}, None
            else:
                raise
        received_time = resp.tmiv.timestamp.ToJsonString()
        converted_fields = [
            field for field in resp.tmiv.fields if not field.name.endswith("@RAW")
        ]
        polymorphic_fields = [
            self._build_tlm_field_pair(tlm_def, field) for field in converted_fields
        ]
        telemetry_data = dict(polymorphic_fields)
        return telemetry_data, received_time

    def _get_cmd_def_by_cmd_code(self, component: str, cmd_code: int) -> Command:
        return next(
            cmd_def
            for component_def in self.tlmcmddb.components
            if component_def.name == component
            for cmd_def in component_def.cmd.commands
            if cmd_def.code == cmd_code
        )

    def _build_tco(
        self,
        component_name: str,
        cmd_def: Command,
        execution_type: str,
        time_indicator: Optional[int],
        cmd_params_value: tuple,
        is_via_mobc: bool,
    ):
        if is_via_mobc:
            cmd_prefix = "MOBC_%s" % (execution_type,)
        else:
            cmd_prefix = execution_type
        params = []
        if time_indicator is not None:
            params.append(
                tco_tmiv_pb2.TcoParam(name="time_indicator", integer=time_indicator)
            )
        for idx, param_def in enumerate(cmd_def.parameters):
            if param_def.data_type == DataType.float or param_def.data_type == DataType.double:
                params.append(
                    tco_tmiv_pb2.TcoParam(
                        name="param{}".format(idx + 1), double=cmd_params_value[idx]
                    )
                )
            elif param_def.data_type == DataType.raw:
                raw = bytes.fromhex(cmd_params_value[idx][2:])
                params.append(
                    tco_tmiv_pb2.TcoParam(name="param{}".format(idx + 1), bytes=raw)
                )
            else:
                if type(cmd_params_value[idx]) == str:
                    value = int(cmd_params_value[idx], 16)
                else:
                    value = cmd_params_value[idx]
                params.append(
                    tco_tmiv_pb2.TcoParam(name="param{}".format(idx + 1), integer=value)
                )
        tco_name = "%s.%s.%s" % (cmd_prefix, component_name, cmd_def.name)
        return tco_tmiv_pb2.Tco(name=tco_name, params=params)

    def _send_command(
        self,
        cmd_code: int,
        execution_type: str,
        time_indicator: Optional[int],
        cmd_params_value: tuple,
        component: str,
        is_via_mobc: bool = False,
    ):
        if component == "":
            component = self.obc_info["name"]
        cmd_def = self._get_cmd_def_by_cmd_code(component, cmd_code)
        tco = self._build_tco(
            component,
            cmd_def,
            execution_type,
            time_indicator,
            cmd_params_value,
            is_via_mobc,
        )
        print(tco)
        req = broker_pb2.PostCommandRequest(tco=tco)
        return self.stub.PostCommand(req)

    def send_rt_cmd(
        self,
        cmd_code: int,
        cmd_params_value: tuple,
        component: str = "",
        is_via_mobc: bool = False,
    ):
        self._send_command(
            cmd_code, "RT", None, cmd_params_value, component, is_via_mobc
        )
        time.sleep(0.1)

    def send_tl_cmd(
        self,
        ti: int,
        cmd_code: int,
        cmd_params_value: tuple,
        component: str = "",
        is_via_mobc: bool = False,
    ):
        self._send_command(cmd_code, "TL", ti, cmd_params_value, component, is_via_mobc)
        time.sleep(0.1)

    def send_bl_cmd(
        self,
        ti: int,
        cmd_code: int,
        cmd_params_value: tuple,
        component: str = "",
        is_via_mobc: bool = False,
    ):
        self._send_command(cmd_code, "BL", ti, cmd_params_value, component, is_via_mobc)
        time.sleep(0.1)

    def send_utl_cmd(
        self,
        unixtime: float,
        cmd_code: int,
        cmd_params_value: tuple,
        component: str = "",
        is_via_mobc: bool = False,
    ):
        epoch = 1577836800.0
        ti = round((unixtime - epoch) * 10.0)
        self._send_command(
            cmd_code, "UTL", ti, cmd_params_value, component, is_via_mobc
        )
        time.sleep(0.1)

    def send_tl_mis_cmd(
        self,
        ti: int,
        cmd_code: int,
        cmd_params_value: tuple,
        component: str = "",
        is_via_mobc: bool = False,
    ):
        self._send_command(
            cmd_code, "TL_MIS", ti, cmd_params_value, component, is_via_mobc
        )
        time.sleep(0.1)

    def send_utl_mis_cmd(
        self,
        unixtime: float,
        cmd_code: int,
        cmd_params_value: tuple,
        component: str = "",
        is_via_mobc: bool = False,
    ):
        epoch = 1577836800.0
        ti = round((unixtime - epoch) * 10.0)
        self._send_command(
            cmd_code, "UTL_MIS", ti, cmd_params_value, component, is_via_mobc
        )
        time.sleep(0.1)

    def get_obc_info(self) -> dict:
        return self.obc_info
