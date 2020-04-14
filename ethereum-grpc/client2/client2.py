# Copyright 2020 mathcody.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC ethereum client."""

from __future__ import print_function
import logging
import json

import grpc

import ethereum_pb2
import ethereum_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50053') as channel:
        ethstub = ethereum_pb2_grpc.ProtoEthServiceStub(channel)
        request = ethereum_pb2.TestnetReq(id=1)
        ethstub.SetTestnet(request)
        request = ethereum_pb2.GetAccountsReq()
        result = ethstub.GetAccounts(request)
        accounts = result.accounts
        print(accounts)
        request = ethereum_pb2.GetBalanceReq(address=accounts[0])
        resp = ethstub.GetBalance(request)
        balance = json.loads(resp.balance)
        print(balance)
        # txHash is of goerli testnet will give error in other testnets
        request = ethereum_pb2.TxHash(txhash="0x59670fc3e54c04006982c609f651266af0221c1d58cc343b1f8b5145a49efc20")
        resp = ethstub.GetTransaction(request)
        tx = json.loads(resp.transaction)
        print("transacion: ", tx)
        request = ethereum_pb2.TxHash(txhash="0x3434df9d7306402770270d3e2268ccfeefe133fcba76331f2cae6502e20d0599")
        resp = ethstub.GetTransactionReceipt(request)
        receipt = resp.txReceipt
        print("receipt: ", receipt)
        request = ethereum_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        resp = ethstub.GetBlockNumber(request)
        print("GetBlockNumber: ", resp)
        request1 = ethereum_pb2.HashStringOrNumber(reqString="0x035589cb682982eb269b7b5246e3a75b79d72cb65997dd118b28bf3b6ceda614")
        request2 = ethereum_pb2.HashStringOrNumber(reqNum=2671241)
        resp1 = ethstub.GetBlockTransactionCount(request1)
        resp2 = ethstub.GetBlockTransactionCount(request2)
        print("GetBlockTransactionCount: ")
        print(resp1)
        print(resp2)
        request1 = ethereum_pb2.HashStringOrNumber(reqString="0x035589cb682982eb269b7b5246e3a75b79d72cb65997dd118b28bf3b6ceda614")
        request2 = ethereum_pb2.HashStringOrNumber(reqNum=1990165)
        resp1 = ethstub.GetBlock(request1)
        resp2 = ethstub.GetBlock(request2)
        print("GetBlock: ")
        print(resp1)
        print(resp2)
        # print()
        # req1 = ethereum_pb2.HashStringOrNumber(reqString="0xa0d48fafcd9b58772d0e60701e481249c04a75f688017a83e13e65699f712686")
        # req2 = ethereum_pb2.HashStringOrNumber(reqNum=2064230)
        # request1 = ethereum_pb2.InfoWithIndex(req=req1, index=0)
        # request2 = ethereum_pb2.InfoWithIndex(req=req2, index=0)
        # resp1 = ethstub.GetTransactionFromBlock(request1)
        # resp2 = ethstub.GetTransactionFromBlock(request2)
        # print(resp1)
        # print(resp2)
        request = ethereum_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        resp = ethstub.GetHashrate(request)
        print("GetHashrate: ")
        print(resp.resultNum)
        resp = ethstub.GetGasPrice(request)
        print("GetGasPrice: ")
        print(resp.resultNum)

if __name__ == '__main__':
    logging.basicConfig()
    run()