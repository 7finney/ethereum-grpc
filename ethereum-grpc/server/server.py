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
  
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ethereum_pb2_grpc.add_ProtoEthServiceServicer_to_server(ProtoEth(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("gRPC server listening on port 50054")
    server.wait_for_termination()
if __name__ == '__main__':
    logging.basicConfig()
    serve()