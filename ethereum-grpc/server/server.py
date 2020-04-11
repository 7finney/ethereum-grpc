import multiprocessing
import json
import logging
import grpc
import ethereum_pb2
import ethereum_pb2_grpc
from concurrent import futures
from google.protobuf.json_format import MessageToJson
from grpc_status import rpc_status
from google.protobuf import any_pb2
from google.rpc import code_pb2, status_pb2, error_details_pb2
import re
import requests
from datetime import datetime
from web3 import Web3
import os

# w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

class ProtoEth(ethereum_pb2_grpc.ProtoEthServiceServicer):
    def getWeb3Url(self, ntwrkId):
        url = "http://115.187.58.4:"
        port = "754"
        if(ntwrkId == 5):
            url += port + "5"
        elif(ntwrkId == 4):
            url += port + "7"
        elif(ntwrkId == 3):
            url += port + "6"
        elif (ntwrkId == 1):
            url = "http://115.187.58.4:8546"
        else:
            url = "http://115.187.58.4:7545"
        return url

    def web3Task(self, request, method):
        print("web3 subprocess started at ", datetime.now().isoformat(timespec='milliseconds'))
        print('[pid:%s] performing calculation on network ID: %s' % (os.getpid(), request))
        url = self.getWeb3Url(request.networkid)
        # print(url)
        web3 = Web3(Web3.HTTPProvider(url))
        if(method == 'get_Transaction'):
            print("getting transaction data from blockchain....")
            try:
                tx = web3.eth.getTransaction(request.txhash)
                return tx
            except Exception as e:
                raise Exception(e)
        else:
            raise Exception("Error: No method specified!")
    # def GetAccounts(self, request, context):
    #     print("Running getAccounts....")
    #     accounts = self._w3.eth.accounts
    #     return ethereum_pb2.GetAccountsResp(accounts=accounts)
    # def GetBalance(self, request, context):
    #     print("Running getBalance....")
    #     balance = self._w3.eth.getBalance(request.address)
    #     return ethereum_pb2.GetBalanceResp(balance=json.dumps(balance))
    # def killTask(self, tasks):
    #     for 
    #     task.cancel
    def GetTransaction(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'get_Transaction')
            try:
                tx = task.result(timeout=30)
                print(tx)
                return ethereum_pb2.TransactionInfo(transaction=Web3.toJSON(tx))
            except Exception as exc:
                print("EXCEPTION: ", exc)
                detail = any_pb2.Any()
                rich_status = rpc_status.status_pb2.Status(
                    code=code_pb2.NOT_FOUND,
                    message=str(exc),
                    details=[detail]
                )
                context.abort_with_status(rpc_status.to_status(rich_status))

    # def GetTransactionReceipt(self, request, context):
    #     print("Running getTransactionReceipt...")
    #     receipt = self._w3.eth.getTransactionReceipt(request.txhash)
    #     print(Web3.toJSON(receipt))
    #     return ethereum_pb2.TxReceipt(txReceipt=Web3.toJSON(receipt))
    # def GetBlockNumber(self, request, context):
    #     print("Running getBlockNumber...")
    #     blockNumber = self._w3.eth.blockNumber
    #     return ethereum_pb2.BlockNumber(blocknum=blockNumber)
    # def GetBlockTransactionCount(self, request, context):
    #     print("Running getBlockTransactionCount...")
    #     if(request.reqString) :
    #         count = self._w3.eth.getBlockTransactionCount(request.reqString)
    #     else:
    #         count = self._w3.eth.getBlockTransactionCount(request.reqNum)
    #     return ethereum_pb2.CountResp(count=count)
    # def GetBlock(self, request, context):
    #     print("Running getBlock...")
    #     if(request.reqString) :
    #         resp = self._w3.eth.getBlock(request.reqString)
    #     else:
    #         resp = self._w3.eth.getBlock(request.reqNum)
    #     return ethereum_pb2.ObjResp(respObj=resp)
    # def GetTransactionFromBlock(self, request, context):
    #     print("Running getTransactionFromBlock...")
    #     if(request.req.reqString):
    #         resp = self._w3.eth.getTransactionFromBlock(request.req.reqString, request.index)
    #     else:
    #         resp = self._w3.eth.getTransactionFromBlock(request.req.reqNum, request.index)
    #     return ethereum_pb2.ObjResp(respObj=resp)
    # def GetHashrate(self, request, context):
    #     print("Running getHashRate...")
    #     resp = self._w3.eth.hashrate
    #     return ethereum_pb2.NumResult(resultNum=resp)
    # def GetGasPrice(self, request, context):
    #     print("Running getGasPrice...")
    #     resp = self._w3.eth.gasPrice
    #     return ethereum_pb2.NumResult(resultNum=resp)
        
  
def serve():
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        server = grpc.server(executor)
        ethereum_pb2_grpc.add_ProtoEthServiceServicer_to_server(ProtoEth(), server)
        server.add_insecure_port('[::]:50053')
        server.start()
        print("gRPC server listening on port 50053")
        server.wait_for_termination()
if __name__ == '__main__':
    logging.basicConfig()
    serve()