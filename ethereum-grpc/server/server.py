import json
import logging
import grpc
import ethereum_pb2
import ethereum_pb2_grpc
from concurrent import futures
from google.protobuf.json_format import MessageToJson
import re
import requests
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://172.26.84.11:7545"))
# w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

class ProtoEth(ethereum_pb2_grpc.ProtoEthServiceServicer):
    def GetAccounts(self, request, context):
        print("Running getAccounts....")
        accounts = w3.eth.accounts
        return ethereum_pb2.GetAccountsResp(accounts=accounts)
    def GetBalance(self, request, context):
        print("Running getBalance....")
        balance = w3.eth.getBalance(request.address)
        return ethereum_pb2.GetBalanceResp(balance=json.dumps(balance))
    def GetTransaction(self, request, context):
        print("Running getTransaction...")
        tx = w3.eth.getTransaction(request.txhash)
        return ethereum_pb2.TransactionInfo(transaction=Web3.toJSON(tx))
    def GetTransactionReceipt(self, request, context):
        print("Running getTransactionReceipt...")
        receipt = w3.eth.getTransactionReceipt(request.txhash)
        return ethereum_pb2.TxReceipt(txReceipt=Web3.toJSON(receipt))
    def GetBlockNumber(self, request, context):
        print("Running getBlockNumber...")
        blockNumber = w3.eth.blockNumber
        return ethereum_pb2.BlockNumber(blocknum=blockNumber)
    def GetBlockTransactionCount(self, request, context):
        print("Running getBlockTransactionCount...")
        if(request.reqString) :
            count = w3.eth.getBlockTransactionCount(request.reqString)
        else:
            count = w3.eth.getBlockTransactionCount(request.reqNum)
        return ethereum_pb2.CountResp(count=count)
    def GetBlock(self, request, context):
        print("Running getBlock...")
        resp = w3.eth.getBlock(request.reqString)
        return ethereum_pb2.ObjResp(respObj=resp)
    def GetTransactionFromBlock(self, request, context):
        print("Running getTransactionFromBlock...")
        if(request.req.reqString):
            resp = w3.eth.getTransactionFromBlock(request.req.reqString, request.index)
        else:
            resp = w3.eth.getTransactionFromBlock(request.req.reqNum, request.index)
        return ethereum_pb2.ObjResp(respObj=resp)
    def GetHashrate(self, request, context):
        print("Running getHashRate...")
        resp = w3.eth.hashrate
        return ethereum_pb2.NumResult(resultNum=resp)
    def GetGasPrice(self, request, context):
        print("Running getGasPrice...")
        resp = w3.eth.gasPrice
        return ethereum_pb2.NumResult(resultNum=resp)
        
  
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ethereum_pb2_grpc.add_ProtoEthServiceServicer_to_server(ProtoEth(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("gRPC server listening on port 50053")
    server.wait_for_termination()
if __name__ == '__main__':
    logging.basicConfig()
    serve()