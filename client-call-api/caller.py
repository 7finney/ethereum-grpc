import sys
sys.path.insert(1, './generated/')
import json
import logging
import grpc
import client_call_pb2
import client_call_pb2_grpc
from concurrent import futures
from google.protobuf.json_format import MessageToJson
import re
import requests
from web3 import Web3, middleware
from request_header_validator_interceptor import RequestHeaderValidatorInterceptor
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

class Deploy(client_call_pb2_grpc.ClientCallServiceServicer):
    _w3: any
    url: str
    port: str
    def unpackParams(self, *args):
        params = []
        regExp = r'\w+(?=\[\d*\])'
        for i in range(0, len(args)):
            print(args)
            if(re.match(regExp, args[i]['type']) or str.__contains__(args[i]['type'], 'tuple')):
                params.append(json.loads(args[i]['value']))
            elif(str.__contains__(args[i]['type'], 'int')):
                params.append(int(args[i]['value']))
            else:
                params.append(args[i]['value'])
        return params
    def RunDeploy(self, request, context):
        id = request.callInterface.testnetId
        self.url = "http://115.187.58.4:"
        self.port = "754"
        if(id == "5"):
            # Görli
            self.url += self.port + "5"
        elif(id == "4"):
            # Rinkeby
            self.url += self.port + "7"
        elif(id == "3"):
            # Ropsten
            self.url += self.port + "6"
        elif(id == "ganache"):
            self.url = "http://ganache:8545"
        else:
            self.url = "http://ganache:8545"
        self._w3 = Web3(Web3.HTTPProvider(self.url))
        if(id == "5" or id == "4"):
            self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        print("Running command " + request.callInterface.command + " with testnetId " + id)
        if request.callInterface.command == "deploy-contract":
            txRecipt = self.web3Deploy(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=txRecipt)
            yield resp
        if request.callInterface.command == "get-gas-estimate":
            gasEstimate = self.web3GasEstimate(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=gasEstimate)
            yield resp
        if request.callInterface.command == "get-accounts":
            accounts, balance = self.web3getAccounts()
            result = json.dumps({ "accounts": accounts, "balance": balance})
            resp = client_call_pb2.ClientCallResponse(result=result)
            yield resp
        if request.callInterface.command == "get-balance":
            # TODO: check for proper hash address before proceeding
            hashAddr = request.callInterface.payload
            balance = self.web3getAccBalance(hashAddr)
            resp = client_call_pb2.ClientCallResponse(result=balance)
            yield resp
        if request.callInterface.command == "send-ether":
            transaction = self.web3Transactions(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=transaction)
            yield resp
        if request.callInterface.command == "ganache-contract-method-call":
            callResponse = self.web3GanacheCallMethods(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=callResponse)
            yield resp
        if request.callInterface.command == "build-rawtx":
            rawTx = self.web3BuildTxn(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=rawTx)
            yield resp
        if request.callInterface.command == "build-raw-eth-tx":
            rawTx = self.web3BuildRawTxn(request.callInterface.payload, id)
            resp = client_call_pb2.ClientCallResponse(result=rawTx)
            yield resp
        if request.callInterface.command == "contract-method-call":
            rawTx = self.web3CallMethods(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=rawTx)
            yield resp
        if request.callInterface.command == "deploy-signed-tx":
            tx = self.web3DeploySignedTransaction(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=tx)
            yield resp
        else:
            return
    def web3Deploy(self, payload):
        input = json.loads(payload)
        bytecode = input['bytecode']
        abi = input['abi']
        params = input['params']
        gasSupply = input['gasSupply']
        Contract = self._w3.eth.contract(abi=abi, bytecode=bytecode)
        deploy_txn = Contract.constructor(*self.unpackParams(*params)).transact({ 'from': Web3.toChecksumAddress(self._w3.eth.accounts[0]), 'gas': gasSupply })
        txn_receipt = self._w3.eth.getTransactionReceipt(deploy_txn)
        return Web3.toJSON(txn_receipt)
    def web3GasEstimate(self, payload):
        input = json.loads(payload)
        bytecode = input['bytecode']
        abi = input['abi']
        params = input['params']
        Contract = self._w3.eth.contract(abi=abi, bytecode=bytecode)
        estimatedGas = Contract.constructor(*self.unpackParams(*params)).estimateGas()
        return Web3.toJSON(estimatedGas)
    # contract calls for ganache
    def web3GanacheCallMethods(self, payload):
        input = json.loads(payload)
        methodName = input['methodName']
        abi = input['abi']
        params = input['params']
        contractAddress = input['address']
        Contract = self._w3.eth.contract(address=Web3.toChecksumAddress(contractAddress), abi=abi)
        method_to_call = getattr(Contract.functions, methodName)
        for i in abi:
            if 'name' in i.keys() and i['name'] == methodName:
                if ('constant' in i.keys() and i['constant'] == False) or ('payable' in i.keys() and i['payable'] == True):
                    txHash = method_to_call(*self.unpackParams(*params)).transact({ 'from': Web3.toChecksumAddress(input['deployAccount']) })
                    callResult = self._w3.eth.waitForTransactionReceipt(txHash)
                    break
                else:
                    callResult = method_to_call(*self.unpackParams(*params)).call()
                    break
        print(Web3.toJSON(callResult))
        return Web3.toJSON(callResult)
    # contract calls for test networks
    def web3CallMethods(self, payload):
        input = json.loads(payload)
        methodName = input['methodName']
        abi = input['abi']
        fromAddress = Web3.toChecksumAddress(input['from'])
        params = input['params']
        contractAddress = input['address']
        gasSupply = input['gasSupply']
        Contract = self._w3.eth.contract(address=Web3.toChecksumAddress(contractAddress), abi=abi)
        method_to_call = getattr(Contract.functions, methodName)
        nonce = self._w3.eth.getTransactionCount(Web3.toChecksumAddress(input['deployAccount']), "pending")
        for i in abi:
            if 'name' in i.keys() and i['name'] == methodName:
                if ('constant' in i.keys() and i['constant'] == False) or ('payable' in i.keys() and i['payable'] == True):
                    txHash = method_to_call(*self.unpackParams(*params)).buildTransaction({ 'nonce': nonce, 'gas': gasSupply })
                    callResult = self._w3.eth.waitForTransactionReceipt(txHash)
                    break
                elif 'stateMutability' in i.keys() and i['stateMutability'] != 'view' and i['stateMutability'] != 'pure':
                    transaction = method_to_call(*self.unpackParams(*params)).buildTransaction({ 'from': fromAddress, 'nonce': nonce })
                    estimatedGas = self._w3.eth.estimateGas(transaction)
                    transaction['gas'] = estimatedGas
                    callResult = transaction
                    break
                else:
                    callResult = method_to_call(*self.unpackParams(*params)).call()
                    break
        print(Web3.toJSON(callResult))
        return Web3.toJSON(callResult)
    def web3getAccounts(self):
        accounts = self._w3.eth.accounts
        balance = self._w3.eth.getBalance(Web3.toChecksumAddress(accounts[0]))
        return accounts, balance
    def web3getAccBalance(self, hashAddr):
        balance = self._w3.eth.getBalance(Web3.toChecksumAddress(hashAddr))
        return Web3.toJSON(balance)
    def web3Transactions(self, transactionInfo):
        # This transaction will only work for ganache
        transaction_Info = json.loads(transactionInfo)
        toAddress = Web3.toChecksumAddress(transaction_Info['toAddress'])
        fromAddress = Web3.toChecksumAddress(transaction_Info['fromAddress'])
        amount = transaction_Info['amount']
        transaction = self._w3.eth.sendTransaction({ 'to': toAddress, 'from': fromAddress, 'value': amount })
        return Web3.toJSON(transaction)
    def web3BuildRawTxn(self, payload, networkId):
        input = json.loads(payload)
        transaction = dict(
            to=Web3.toChecksumAddress(input['to']),
            value=int(input['value']),
            nonce=self._w3.eth.getTransactionCount(Web3.toChecksumAddress(input['from']), "pending"),
            gasPrice=self._w3.eth.gasPrice
        )
        transaction['from'] = Web3.toChecksumAddress(input['from'])
        estimatedGas = self._w3.eth.estimateGas(transaction)
        transaction['gas'] = int(estimatedGas)
        return Web3.toJSON(transaction)
    def web3BuildTxn(self, payload):
        input = json.loads(payload)
        bytecode = input['bytecode']
        abi = input['abi']
        params = input['params']
        gasSupply = input['gasSupply']
        Contract = self._w3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = self._w3.eth.getTransactionCount(Web3.toChecksumAddress(input['from']), "pending")
        transaction = Contract.constructor(*self.unpackParams(*params)).buildTransaction({
            'from': Web3.toChecksumAddress(input['from']),
            'nonce': nonce,
            'gas': gasSupply
        })
        del transaction['to']
        return Web3.toJSON(transaction)
    def web3DeploySignedTransaction(self, rawTransaction):
        resp = self._w3.eth.sendRawTransaction(rawTransaction)
        return resp.hex()
def serve():
    header_validator = RequestHeaderValidatorInterceptor(grpc.StatusCode.UNAUTHENTICATED, 'Access denied!')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(header_validator,))
    client_call_pb2_grpc.add_ClientCallServiceServicer_to_server(Deploy(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("gRPC server listening on port 50053")
    server.wait_for_termination()
if __name__ == '__main__':
    logging.basicConfig()
    serve()