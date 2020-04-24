# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import ethereum_pb2 as ethereum__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class ProtoEthServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetBalance = channel.unary_unary(
        '/protoeth.ProtoEthService/GetBalance',
        request_serializer=ethereum__pb2.GetBalanceReq.SerializeToString,
        response_deserializer=ethereum__pb2.GetBalanceResp.FromString,
        )
    self.GetTransaction = channel.unary_unary(
        '/protoeth.ProtoEthService/GetTransaction',
        request_serializer=ethereum__pb2.GetTxReq.SerializeToString,
        response_deserializer=ethereum__pb2.TransactionInfo.FromString,
        )
    self.GetTransactionReceipt = channel.unary_unary(
        '/protoeth.ProtoEthService/GetTransactionReceipt',
        request_serializer=ethereum__pb2.TxHash.SerializeToString,
        response_deserializer=ethereum__pb2.TxReceipt.FromString,
        )
    self.ContractCall = channel.unary_unary(
        '/protoeth.ProtoEthService/ContractCall',
        request_serializer=ethereum__pb2.CallRequest.SerializeToString,
        response_deserializer=ethereum__pb2.CallResponse.FromString,
        )
    self.GetHashrate = channel.unary_unary(
        '/protoeth.ProtoEthService/GetHashrate',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=ethereum__pb2.NumResult.FromString,
        )
    self.GetGasPrice = channel.unary_unary(
        '/protoeth.ProtoEthService/GetGasPrice',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=ethereum__pb2.NumResult.FromString,
        )
    self.GetBlockNumber = channel.unary_unary(
        '/protoeth.ProtoEthService/GetBlockNumber',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=ethereum__pb2.BlockNumber.FromString,
        )
    self.GetBlockTransactionCount = channel.unary_unary(
        '/protoeth.ProtoEthService/GetBlockTransactionCount',
        request_serializer=ethereum__pb2.HashStringOrNumber.SerializeToString,
        response_deserializer=ethereum__pb2.CountResp.FromString,
        )
    self.GetBlock = channel.unary_unary(
        '/protoeth.ProtoEthService/GetBlock',
        request_serializer=ethereum__pb2.HashStringOrNumber.SerializeToString,
        response_deserializer=ethereum__pb2.ObjResp.FromString,
        )
    self.GetTransactionFromBlock = channel.unary_unary(
        '/protoeth.ProtoEthService/GetTransactionFromBlock',
        request_serializer=ethereum__pb2.InfoWithIndex.SerializeToString,
        response_deserializer=ethereum__pb2.ObjResp.FromString,
        )
    self.SendRawTransactions = channel.unary_unary(
        '/protoeth.ProtoEthService/SendRawTransactions',
        request_serializer=ethereum__pb2.RawTxRequest.SerializeToString,
        response_deserializer=ethereum__pb2.TxResponse.FromString,
        )


class ProtoEthServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetBalance(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTransaction(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTransactionReceipt(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ContractCall(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetHashrate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetGasPrice(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetBlockNumber(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetBlockTransactionCount(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetBlock(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTransactionFromBlock(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendRawTransactions(self, request, context):
    """eth_sendRawTransaction should have simple requests but stream of responses
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProtoEthServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetBalance': grpc.unary_unary_rpc_method_handler(
          servicer.GetBalance,
          request_deserializer=ethereum__pb2.GetBalanceReq.FromString,
          response_serializer=ethereum__pb2.GetBalanceResp.SerializeToString,
      ),
      'GetTransaction': grpc.unary_unary_rpc_method_handler(
          servicer.GetTransaction,
          request_deserializer=ethereum__pb2.GetTxReq.FromString,
          response_serializer=ethereum__pb2.TransactionInfo.SerializeToString,
      ),
      'GetTransactionReceipt': grpc.unary_unary_rpc_method_handler(
          servicer.GetTransactionReceipt,
          request_deserializer=ethereum__pb2.TxHash.FromString,
          response_serializer=ethereum__pb2.TxReceipt.SerializeToString,
      ),
      'ContractCall': grpc.unary_unary_rpc_method_handler(
          servicer.ContractCall,
          request_deserializer=ethereum__pb2.CallRequest.FromString,
          response_serializer=ethereum__pb2.CallResponse.SerializeToString,
      ),
      'GetHashrate': grpc.unary_unary_rpc_method_handler(
          servicer.GetHashrate,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=ethereum__pb2.NumResult.SerializeToString,
      ),
      'GetGasPrice': grpc.unary_unary_rpc_method_handler(
          servicer.GetGasPrice,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=ethereum__pb2.NumResult.SerializeToString,
      ),
      'GetBlockNumber': grpc.unary_unary_rpc_method_handler(
          servicer.GetBlockNumber,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=ethereum__pb2.BlockNumber.SerializeToString,
      ),
      'GetBlockTransactionCount': grpc.unary_unary_rpc_method_handler(
          servicer.GetBlockTransactionCount,
          request_deserializer=ethereum__pb2.HashStringOrNumber.FromString,
          response_serializer=ethereum__pb2.CountResp.SerializeToString,
      ),
      'GetBlock': grpc.unary_unary_rpc_method_handler(
          servicer.GetBlock,
          request_deserializer=ethereum__pb2.HashStringOrNumber.FromString,
          response_serializer=ethereum__pb2.ObjResp.SerializeToString,
      ),
      'GetTransactionFromBlock': grpc.unary_unary_rpc_method_handler(
          servicer.GetTransactionFromBlock,
          request_deserializer=ethereum__pb2.InfoWithIndex.FromString,
          response_serializer=ethereum__pb2.ObjResp.SerializeToString,
      ),
      'SendRawTransactions': grpc.unary_unary_rpc_method_handler(
          servicer.SendRawTransactions,
          request_deserializer=ethereum__pb2.RawTxRequest.FromString,
          response_serializer=ethereum__pb2.TxResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'protoeth.ProtoEthService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
