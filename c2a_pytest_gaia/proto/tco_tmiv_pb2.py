# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tco_tmiv.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0etco_tmiv.proto\x12\x08tco_tmiv\x1a\x1fgoogle/protobuf/timestamp.proto"7\n\x03Tco\x12\x0c\n\x04name\x18\x01 \x01(\t\x12"\n\x06params\x18\x02 \x03(\x0b\x32\x12.tco_tmiv.TcoParam"W\n\x08TcoParam\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\x07integer\x18\x02 \x01(\x03H\x00\x12\x10\n\x06\x64ouble\x18\x03 \x01(\x01H\x00\x12\x0f\n\x05\x62ytes\x18\x04 \x01(\x0cH\x00\x42\x07\n\x05value"\x86\x01\n\x04Tmiv\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1c\n\x14plugin_received_time\x18\x02 \x01(\x04\x12#\n\x06\x66ields\x18\x03 \x03(\x0b\x32\x13.tco_tmiv.TmivField\x12-\n\ttimestamp\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp"z\n\tTmivField\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x06string\x18\x02 \x01(\tH\x00\x12\x10\n\x06\x64ouble\x18\x03 \x01(\x01H\x00\x12\x11\n\x07integer\x18\x04 \x01(\x03H\x00\x12\x0e\n\x04\x65num\x18\x05 \x01(\tH\x00\x12\x0f\n\x05\x62ytes\x18\x06 \x01(\x0cH\x00\x42\x07\n\x05valueb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "tco_tmiv_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _TCO._serialized_start = 61
    _TCO._serialized_end = 116
    _TCOPARAM._serialized_start = 118
    _TCOPARAM._serialized_end = 205
    _TMIV._serialized_start = 208
    _TMIV._serialized_end = 342
    _TMIVFIELD._serialized_start = 344
    _TMIVFIELD._serialized_end = 466
# @@protoc_insertion_point(module_scope)
