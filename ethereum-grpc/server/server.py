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


# w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

class ProtoEth(ethereum_pb2_grpc.ProtoEthServiceServicer):
    _w3: tuple
    _url: str
    _port: str
    def SetTestnet(self, request, context):
        id = request.id
        print("id: ", id, "\n")
        self._url = "http://115.187.58.4:"
        self._port = "754"
        if(id == 5):
            self._url += self._port + "5"
        elif(id == 4):
            self._url += self._port + "7"
        elif(id == 3):
            self._url += self._port + "6"
        elif(id == 10):
            self._url = "http://ganache:8545"
        else:
            self._url = "http://ganache:8545"
        self._w3 = Web3(Web3.HTTPProvider(self._url))
        # self._w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
        # self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return ethereum_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
    def GetAccounts(self, request, context):
        print("Running getAccounts....")
        accounts = self._w3.eth.accounts
        return ethereum_pb2.GetAccountsResp(accounts=accounts)
    def GetBalance(self, request, context):
        print("Running getBalance....")
        balance = self._w3.eth.getBalance(request.address)
        return ethereum_pb2.GetBalanceResp(balance=json.dumps(balance))
    def GetTransaction(self, request, context):
        print("Running getTransaction...")
        tx = self._w3.eth.getTransaction(request.txhash)
        return ethereum_pb2.TransactionInfo(transaction=Web3.toJSON(tx))
    def GetTransactionReceipt(self, request, context):
        print("Running getTransactionReceipt...")
        receipt = self._w3.eth.getTransactionReceipt(request.txhash)
        print(Web3.toJSON(receipt))
        return ethereum_pb2.TxReceipt(txReceipt=Web3.toJSON(receipt))
    def GetBlockNumber(self, request, context):
        print("Running getBlockNumber...")
        blockNumber = self._w3.eth.blockNumber
        return ethereum_pb2.BlockNumber(blocknum=blockNumber)
    def GetBlockTransactionCount(self, request, context):
        print("Running getBlockTransactionCount...")
        if(request.reqString) :
            count = self._w3.eth.getBlockTransactionCount(request.reqString)
        else:
            count = self._w3.eth.getBlockTransactionCount(request.reqNum)
        return ethereum_pb2.CountResp(count=count)
    def GetBlock(self, request, context):
        print("Running getBlock...")
        if(request.reqString) :
            resp = self._w3.eth.getBlock(request.reqString)
        else:
            resp = self._w3.eth.getBlock(request.reqNum)
        return ethereum_pb2.ObjResp(respObj=resp)
    def GetTransactionFromBlock(self, request, context):
        print("Running getTransactionFromBlock...")
        if(request.req.reqString):
            resp = self._w3.eth.getTransactionFromBlock(request.req.reqString, request.index)
        else:
            resp = self._w3.eth.getTransactionFromBlock(request.req.reqNum, request.index)
        return ethereum_pb2.ObjResp(respObj=resp)
    def GetHashrate(self, request, context):
        print("Running getHashRate...")
        resp = self._w3.eth.hashrate
        return ethereum_pb2.NumResult(resultNum=resp)
    def GetGasPrice(self, request, context):
        print("Running getGasPrice...")
        resp = self._w3.eth.gasPrice
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