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
from web3 import Web3
from request_header_validator_interceptor import RequestHeaderValidatorInterceptor

class Deploy(client_call_pb2_grpc.ClientCallServiceServicer):
    _w3: any
    url: str
    port: str
    def unpackParams(self, *args):
        params = []
        regExp = r'\w+(?=\[\d*\])'
        for i in range(0, len(args)):
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
            self.url += self.port + "5"
        elif(id == "4"):
            self.url += self.port + "7"
        elif(id == "3"):
            self.url += self.port + "6"
        elif(id == "ganache"):
            self.url = "http://localhost:8545"
        else:
            self.url = "http://localhost:8545"
        self._w3 = Web3(Web3.HTTPProvider(self.url))
        print("Running command: ", request.callInterface.command)
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
            print(request.callInterface)
            balance = self.web3getAccBalance(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=balance)
            yield resp
        if request.callInterface.command == "send-ether":
            transaction = self.web3Transactions(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=transaction)
            yield resp
        if request.callInterface.command == "contract-method-call":
            callResponse = self.web3CallMethods(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=callResponse)
            yield resp
        if request.callInterface.command == "build-rawtx":
            print("Build raw tx")
            rawTx = self.web3BuildTxn(request.callInterface.payload)
            resp = client_call_pb2.ClientCallResponse(result=rawTx)
            yield resp
        else:
            return
    def web3Deploy(self, payload):
        input = json.loads(payload)
        # bytecode = "608060405234801561001057600080fd5b506040516103c03803806103c08339818101604052602081101561003357600080fd5b810190808051604051939291908464010000000082111561005357600080fd5b90830190602082018581111561006857600080fd5b825164010000000081118282018810171561008257600080fd5b82525081516020918201929091019080838360005b838110156100af578181015183820152602001610097565b50505050905090810190601f1680156100dc5780820380516001836020036101000a031916815260200191505b50604052505081516100f6915060019060208401906100fd565b5050610198565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061013e57805160ff191683800117855561016b565b8280016001018555821561016b579182015b8281111561016b578251825591602001919060010190610150565b5061017792915061017b565b5090565b61019591905b808211156101775760008155600101610181565b90565b610219806101a76000396000f3fe608060405234801561001057600080fd5b506004361061005d577c0100000000000000000000000000000000000000000000000000000000600035046341c0e1b58114610062578063cfae32171461006c578063f1eae25c146100e9575b600080fd5b61006a6100f1565b005b61007461012e565b6040805160208082528351818301528351919283929083019185019080838360005b838110156100ae578181015183820152602001610096565b50505050905090810190601f1680156100db5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b61006a6101c3565b60005473ffffffffffffffffffffffffffffffffffffffff1633141561012c5760005473ffffffffffffffffffffffffffffffffffffffff16ff5b565b60018054604080516020601f600260001961010087891615020190951694909404938401819004810282018101909252828152606093909290918301828280156101b95780601f1061018e576101008083540402835291602001916101b9565b820191906000526020600020905b81548152906001019060200180831161019c57829003601f168201915b5050505050905090565b6000805473ffffffffffffffffffffffffffffffffffffffff19163317905556fea265627a7a723158205667d7defdcb9d2af78ea9111648fff00e87480f5152da9170bc07a8817701c464736f6c634300050b0032"
        # abi = json.loads('[{"constant":false,"inputs":[],"name":"kill","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0x41c0e1b5"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function","signature":"0xcfae3217"},{"constant":false,"inputs":[],"name":"mortal","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0xf1eae25c"},{"inputs":[{"internalType":"string","name":"_greeting","type":"string","value":"Hello"}],"payable":false,"stateMutability":"nonpayable","type":"constructor","signature":"constructor"}]')
        bytecode = input['bytecode']
        abi = input['abi']
        params = input['params']
        gasSupply = input['gasSupply']
        Contract = self._w3.eth.contract(abi=abi, bytecode=bytecode)
        deploy_txn = Contract.constructor(*self.unpackParams(*params)).transact({ 'from': self._w3.eth.accounts[0], 'gas': gasSupply })
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
    def web3CallMethods(self, payload):
        input = json.loads(payload)
        methodName = input['methodName']
        abi = input['abi']
        params = input['params']
        contractAddress = input['address']
        Contract = self._w3.eth.contract(address=Web3.toChecksumAddress(contractAddress), abi=abi)
        method_to_call = getattr(Contract.functions, methodName)
        for i in abi:
            if i['name'] == methodName:
                if i['constant'] == False or i['payable'] == True:
                    txHash = method_to_call(*self.unpackParams(*params)).transact({ 'from': input['deployAccount'] })
                    callResult = self._w3.eth.waitForTransactionReceipt(txHash)
                    break
                else:
                    callResult = method_to_call(*self.unpackParams(*params)).call()
                    break
        return Web3.toJSON(callResult)
    def web3getAccounts(self):
        accounts = self._w3.eth.accounts
        balance = self._w3.eth.getBalance(accounts[0])
        return accounts, balance
    def web3getAccBalance(self, account):
        balance = self._w3.eth.getBalance(account)
        return Web3.toJSON(balance)
    def web3Transactions(self, transactionInfo):
        transaction_Info = json.loads(transactionInfo)
        toAddress = transaction_Info['toAddress']
        fromAddress = transaction_Info['fromAddress']
        amount = transaction_Info['amount']
        transaction = self._w3.eth.sendTransaction({ 'to': toAddress, 'from': fromAddress, 'value': amount })
        return Web3.toJSON(transaction)
    def web3BuildTxn(self, payload):
        input = json.loads(payload)
        bytecode = input['bytecode']
        abi = input['abi']
        params = input['params']
        gasSupply = input['gasSupply']
        Contract = self._w3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = self._w3.eth.getTransactionCount(self._w3.toChecksumAddress(input['from']), "pending")
        transaction = Contract.constructor(*self.unpackParams(*params)).buildTransaction({ 'nonce': nonce, 'gas': gasSupply })
        del transaction['to']
        # print("del txn: \n", txn)
        return Web3.toJSON(transaction)
  
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