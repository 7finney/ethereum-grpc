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
from request_header_validator_interceptor import RequestHeaderValidatorInterceptor
import yaml
import numpy as np


class ProtoEth(ethereum_pb2_grpc.ProtoEthServiceServicer):
    def getWeb3Url(self, ntwrkId):
        with open("config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
        url = [cfg["networks"][n]["url"] for n in cfg["networks"] if np.uint8(cfg["networks"][n]["id"]) == ntwrkId]
        return url[0]
    def isTransaction(self, abi):
        if ('constant' in abi.keys() and abi['constant'] == False):
            return True
        elif ('payable' in abi.keys() and abi['payable'] == True):
            return True
        elif 'stateMutability' in abi.keys() and abi['stateMutability'] != 'view' and abi['stateMutability'] != 'pure':
            return True
        else:
            return False

    def web3Task(self, request, method):
        print("web3 subprocess started at ", datetime.now().isoformat(timespec='milliseconds'))
        print('[pid:%s] performing calculation on network ID: %s' % (os.getpid(), request.networkid))
        url = self.getWeb3Url(request.networkid)
        web3 = Web3(Web3.HTTPProvider(url))
        if(method == 'eth_getTransaction'):
            try:
                tx = web3.eth.getTransaction(request.txhash)
                return tx
            except Exception as e:
                raise Exception(e)
        if(method == 'eth_sendRawTransaction'):
            try:
                tx = web3.eth.sendRawTransaction(request.tx)
                return tx
            except Exception as e:
                raise Exception(e)
        if(method == 'eth_call'):
            try:
                methodName = request.fn
                abi = json.loads(request.abi)
                params = json.loads(request.params)
                contractAddress = Web3.toChecksumAddress(request.address)
                fromAddress = Web3.toChecksumAddress(request.fromAddress)
                gasSupply = request.gasSupply or 0
                value = request.value or 0
                # create contract instance
                Contract = web3.eth.contract(address=contractAddress, abi=abi)
                nonce = web3.eth.getTransactionCount(fromAddress, "pending")
                # find matching method with name
                method_to_call = getattr(Contract.functions, methodName)
                for i in abi:
                    if 'name' in i.keys() and i['name'] == methodName:
                        if(self.isTransaction(i)):
                            transaction = method_to_call(*self.unpackParams(params)).buildTransaction({ 'from': fromAddress, 'gas': 0, 'nonce': nonce, 'value': value })
                            try:
                                estimatedGas = web3.eth.estimateGas(transaction)
                                transaction['gas'] = estimatedGas
                            except Exception as e:
                                print(e)
                                transaction['gas'] = gasSupply
                            callResult = transaction
                            break
                        else:
                            callResult = method_to_call(*self.unpackParams(params)).call()
                            break
                print(Web3.toJSON(callResult))
                return Web3.toJSON(callResult)
            except Exception as e:
                raise Exception(e)
        else:
            raise Exception("Error: No method specified!")
    # def GetBalance(self, request, context):
    #     print("Running getBalance....")
    #     balance = self._w3.eth.getBalance(request.address)
    #     return ethereum_pb2.GetBalanceResp(balance=json.dumps(balance))
    # def killTask(self, tasks):
    #     for 
    #     task.cancel
    def GetTransaction(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'eth_getTransaction')
            try:
                tx = task.result(timeout=30)
                print(tx)
                return ethereum_pb2.TransactionInfo(transaction=Web3.toJSON(tx))
            except Exception as exc:
                print("Exception: ", exc)
                detail = any_pb2.Any()
                rich_status = rpc_status.status_pb2.Status(
                    code=code_pb2.NOT_FOUND,
                    message=str(exc),
                    details=[detail]
                )
                context.abort_with_status(rpc_status.to_status(rich_status))

    def SendRawTransactions(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'eth_sendRawTransaction')
            try:
                tx = task.result(timeout=30)
                print(tx)
                return ethereum_pb2.TransactionInfo(transaction=Web3.toJSON(tx))
            except Exception as exc:
                print("Exception: ", exc)
                detail = any_pb2.Any()
                rich_status = rpc_status.status_pb2.Status(
                    code=code_pb2.NOT_FOUND,
                    message=str(exc),
                    details=[detail]
                )
                context.abort_with_status(rpc_status.to_status(rich_status))
    def ContractCall(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'eth_call')
            try:
                res = task.result(timeout=30)
                return ethereum_pb2.CallResponse(result=Web3.toJSON(res))
            except Exception as exc:
                print("Exception: ", exc)
                detail = any_pb2.Any()
                rich_status = rpc_status.status_pb2.Status(
                    code=code_pb2.NOT_FOUND,
                    message=str(exc),
                    details=[detail]
                )
                context.abort_with_status(rpc_status.to_status(rich_status))
    def unpackParams(self, *args):
        params = []
        regExp = r'\w+(?=\[\d*\])'
        for i in range(0, len(args)):
            if(re.match(regExp, args[i]['type']) or str.__contains__(args[i]['type'], 'tuple')):
                params.append(json.loads(args[i]['value']))
            elif(str.__contains__(args[i]['type'], 'int')):
                params.append(int(args[i]['value']))
            elif(str.__contains__(args[i]['type'], 'address')):
                params.append(Web3.toChecksumAddress(args[i]['value']))
            else:
                params.append(args[i]['value'])
        return params


def serve():
    # header_validator = RequestHeaderValidatorInterceptor(grpc.StatusCode.UNAUTHENTICATED, 'Access denied!')
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        # server = grpc.server(executor, interceptors=(header_validator,))
        server = grpc.server(executor,)
        ethereum_pb2_grpc.add_ProtoEthServiceServicer_to_server(ProtoEth(), server)
        server.add_insecure_port('[::]:50054')
        server.start()
        print("gRPC server listening on port 50054")
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
