# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ethereum.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ethereum.proto',
  package='protoeth',
  syntax='proto3',
  serialized_options=_b('Z\010protoeth'),
  serialized_pb=_b('\n\x0e\x65thereum.proto\x12\x08protoeth\"\x14\n\x12GetAccountsRequest\"%\n\x13GetAccountsResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\"\x1a\n\x0cRawTxRequest\x12\n\n\x02tx\x18\x01 \x01(\t\"\x1c\n\nTxResponse\x12\x0e\n\x06txData\x18\x01 \x01(\t2\xaa\x01\n\x0fProtoEthService\x12N\n\x0bGetAccounts\x12\x1c.protoeth.GetAccountsRequest\x1a\x1d.protoeth.GetAccountsResponse\"\x00\x30\x01\x12G\n\x13SendRawTransactions\x12\x16.protoeth.RawTxRequest\x1a\x14.protoeth.TxResponse\"\x00\x30\x01\x42\nZ\x08protoethb\x06proto3')
)




_GETACCOUNTSREQUEST = _descriptor.Descriptor(
  name='GetAccountsRequest',
  full_name='protoeth.GetAccountsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=48,
)


_GETACCOUNTSRESPONSE = _descriptor.Descriptor(
  name='GetAccountsResponse',
  full_name='protoeth.GetAccountsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='protoeth.GetAccountsResponse.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=87,
)


_RAWTXREQUEST = _descriptor.Descriptor(
  name='RawTxRequest',
  full_name='protoeth.RawTxRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tx', full_name='protoeth.RawTxRequest.tx', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=89,
  serialized_end=115,
)


_TXRESPONSE = _descriptor.Descriptor(
  name='TxResponse',
  full_name='protoeth.TxResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='txData', full_name='protoeth.TxResponse.txData', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=145,
)

DESCRIPTOR.message_types_by_name['GetAccountsRequest'] = _GETACCOUNTSREQUEST
DESCRIPTOR.message_types_by_name['GetAccountsResponse'] = _GETACCOUNTSRESPONSE
DESCRIPTOR.message_types_by_name['RawTxRequest'] = _RAWTXREQUEST
DESCRIPTOR.message_types_by_name['TxResponse'] = _TXRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAccountsRequest = _reflection.GeneratedProtocolMessageType('GetAccountsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETACCOUNTSREQUEST,
  '__module__' : 'ethereum_pb2'
  # @@protoc_insertion_point(class_scope:protoeth.GetAccountsRequest)
  })
_sym_db.RegisterMessage(GetAccountsRequest)

GetAccountsResponse = _reflection.GeneratedProtocolMessageType('GetAccountsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETACCOUNTSRESPONSE,
  '__module__' : 'ethereum_pb2'
  # @@protoc_insertion_point(class_scope:protoeth.GetAccountsResponse)
  })
_sym_db.RegisterMessage(GetAccountsResponse)

RawTxRequest = _reflection.GeneratedProtocolMessageType('RawTxRequest', (_message.Message,), {
  'DESCRIPTOR' : _RAWTXREQUEST,
  '__module__' : 'ethereum_pb2'
  # @@protoc_insertion_point(class_scope:protoeth.RawTxRequest)
  })
_sym_db.RegisterMessage(RawTxRequest)

TxResponse = _reflection.GeneratedProtocolMessageType('TxResponse', (_message.Message,), {
  'DESCRIPTOR' : _TXRESPONSE,
  '__module__' : 'ethereum_pb2'
  # @@protoc_insertion_point(class_scope:protoeth.TxResponse)
  })
_sym_db.RegisterMessage(TxResponse)


DESCRIPTOR._options = None

_PROTOETHSERVICE = _descriptor.ServiceDescriptor(
  name='ProtoEthService',
  full_name='protoeth.ProtoEthService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=148,
  serialized_end=318,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAccounts',
    full_name='protoeth.ProtoEthService.GetAccounts',
    index=0,
    containing_service=None,
    input_type=_GETACCOUNTSREQUEST,
    output_type=_GETACCOUNTSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SendRawTransactions',
    full_name='protoeth.ProtoEthService.SendRawTransactions',
    index=1,
    containing_service=None,
    input_type=_RAWTXREQUEST,
    output_type=_TXRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PROTOETHSERVICE)

DESCRIPTOR.services_by_name['ProtoEthService'] = _PROTOETHSERVICE

# @@protoc_insertion_point(module_scope)
