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

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

class ProtoEth(ethereum_pb2_grpc.ProtoEthServiceServicer):
    def GetAccounts(self, request, context):
        print("Running getAccounts....")
        accounts, balance = self.web3getAccounts()
        result = json.dumps({
            "accounts": accounts,
            "balance": balance
        })
        resp = ethereum_pb2.GetAccountsResponse(result=result)
        yield resp
    def web3getAccounts(self):
        accounts = w3.eth.accounts
        balance = w3.eth.getBalance(accounts[0])
        return accounts, balance
  
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