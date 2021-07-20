import multiprocessing
import json
import logging
from eth_utils import address
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
                txhash = web3.eth.sendRawTransaction(request.tx)
                return txhash
            except Exception as e:
                raise Exception(e)
        if(method == 'eth_buildRawTransaction'):
            try:
                bytecode = request.bytecode
                abi = json.loads(request.abi)
                if len(request.params) > 0:
                    params = json.loads(request.params)
                else:
                    params = None
                fromAddress = Web3.toChecksumAddress(request.fromaddress)
                gasSupply = request.gas or 0
                value = request.value or 0
                Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
                nonce = web3.eth.getTransactionCount(Web3.toChecksumAddress(fromAddress), "pending")
                transaction = Contract.constructor(*self.unpackParams(params)).buildTransaction({
                    'from': Web3.toChecksumAddress(fromAddress),
                    'nonce': nonce,
                    'gas': gasSupply
                })
                del transaction['to']
                return transaction
            except Exception as e:
                raise Exception(e)
        if(method == 'eth_Transact'):
            try:
                bytecode = request.bytecode
                abi = json.loads(request.abi)
                if len(request.params) > 0:
                    params = json.loads(request.params)
                else:
                    params = None
                fromAddress = Web3.toChecksumAddress(request.fromaddress)
                gasSupply = request.gas or 0
                value = request.value or 0
                Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
                transaction = Contract.constructor(*self.unpackParams(params)).transact({
                    'from': Web3.toChecksumAddress(fromAddress),
                    'gas': gasSupply
                })
                return transaction
            except Exception as e:
                raise Exception(e)
        if(method == 'eth_call'):
            try:
                methodName = request.fn
                abi = json.loads(request.abi)
                if len(request.params) > 0:
                    params = json.loads(request.params)
                else:
                    params = None
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
                            # assign transaction as call result
                            callResult = transaction
                            break
                        else:
                            callResult = method_to_call(*self.unpackParams(params)).call()
                            break
                print(Web3.toJSON(callResult))
                return Web3.toJSON(callResult)
            except Exception as e:
                raise Exception(e)
        if(method == 'estimate_gas'):
            print(request)
            try:
                bytecode = request.bytecode
                abi = json.loads(request.abi)
                if len(request.params) > 0:
                    params = json.loads(request.params)
                else:
                    params = None
                fromAddress = Web3.toChecksumAddress(request.fromaddress)
                Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
                estimatedGas = Contract.constructor(*self.unpackParams(params)).estimateGas({ 'from': fromAddress })
                return estimatedGas
            except Exception as e:
                raise Exception(e)
        if(method == 'eth_getBalance'):
            try:
                address = Web3.toChecksumAddress(request.address)
                balance = web3.eth.getBalance(address)
                return balance
            except Exception as e:
                raise Exception(e)
        if(method == 'ganache_accounts'):
            try:
                accounts = web3.eth.accounts
                balance = web3.eth.getBalance(Web3.toChecksumAddress(accounts[0]))
                return accounts, balance
            except Exception as e:
                raise Exception(e)
        else:
            raise Exception("Error: No method specified!")
    def GetBalance(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'eth_getBalance')
            try:
                balance = task.result(timeout=30)
                return ethereum_pb2.GetBalanceResp(balance=json.dumps(balance))
            except Exception as exc:
                print("Exception: ", exc)
                detail = any_pb2.Any()
                rich_status = rpc_status.status_pb2.Status(
                    code=code_pb2.NOT_FOUND,
                    message=str(exc),
                    details=[detail]
                )
                context.abort_with_status(rpc_status.to_status(rich_status))
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
    def BuildRawTransaction(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'eth_buildRawTransaction')
            try:
                tx = task.result(timeout=30)
                print(tx)
                return ethereum_pb2.RawTransaction(transaction=Web3.toJSON(tx))
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
                txhash = task.result(timeout=30)
                print(txhash)
                return ethereum_pb2.TxHash(txhash=Web3.toJSON(txhash))
            except Exception as exc:
                print("Exception: ", exc)
                detail = any_pb2.Any()
                rich_status = rpc_status.status_pb2.Status(
                    code=code_pb2.NOT_FOUND,
                    message=str(exc),
                    details=[detail]
                )
                context.abort_with_status(rpc_status.to_status(rich_status))
    def Transact(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'eth_Transact')
            try:
                tx = task.result(timeout=30)
                return ethereum_pb2.TxHash(txhash=Web3.toJSON(tx))
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
    def EstimateGas(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'estimate_gas')
            try:
                res = task.result(timeout=30)
                return ethereum_pb2.EstimateGasResp(result=Web3.toJSON(res))
            except Exception as exc:
                print("Exception: ", exc)
                detail = any_pb2.Any()
                rich_status = rpc_status.status_pb2.Status(
                    code=code_pb2.NOT_FOUND,
                    message=str(exc),
                    details=[detail]
                )
                context.abort_with_status(rpc_status.to_status(rich_status))
    def GetGanacheAccounts(self, request, context):
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            task = executor.submit(self.web3Task, request, 'ganache_accounts')
            try:
                accounts, balance = task.result(timeout=30)
                return ethereum_pb2.GanacheAccRsp(accounts=accounts, balance=Web3.toJSON(balance))
            except Exception as exc:
                print("Exception: ", exc)
                detail = any_pb2.Any()
                rich_status = rpc_status.status_pb2.Status(
                    code=code_pb2.NOT_FOUND,
                    message=str(exc),
                    details=[detail]
                )
                context.abort_with_status(rpc_status.to_status(rich_status))
    def unpackParams(self, args):
        params = []
        regExp = r'\w+(?=\[\d*\])'
        if args == None:
            return params
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
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        server = grpc.server(executor,)
        ethereum_pb2_grpc.add_ProtoEthServiceServicer_to_server(ProtoEth(), server)
        server.add_insecure_port('[::]:50054')
        server.start()
        print("gRPC server listening on port 50054")
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
