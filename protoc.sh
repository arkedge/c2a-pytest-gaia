#!/bin/bash

set -Cue -o pipefail

rye run python -m grpc_tools.protoc \
  -I"${GAIA_PROTO_PATH}" \
  --python_out=c2a_pytest_gaia/proto \
  --pyi_out=c2a_pytest_gaia/proto \
  --grpc_python_out=c2a_pytest_gaia/proto \
  "${GAIA_PROTO_PATH}/broker.proto" \
  "${GAIA_PROTO_PATH}/tco_tmiv.proto"

# HACK: https://github.com/protocolbuffers/protobuf/issues/1491
sed -i -e 's|import broker_pb2 as broker__pb2|from . import broker_pb2 as broker__pb2|g' c2a_pytest_gaia/proto/*_grpc.py
sed -i -e 's|import tco_tmiv_pb2|from . import tco_tmiv_pb2|g' c2a_pytest_gaia/proto/*.py

