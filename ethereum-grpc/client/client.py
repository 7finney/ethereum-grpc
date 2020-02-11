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
        request = ethereum_pb2.GetAccountsReq()
        result = ethstub.GetAccounts(request)
        accounts = result.accounts
        print(accounts)
        request = ethereum_pb2.GetBalanceReq(address=accounts[0])
        resp = ethstub.GetBalance(request)
        balance = json.loads(resp.balance)
        print(balance)
        # txHash is of goerli testnet will give error in other testnets
        request = ethereum_pb2.TxHash(txhash="0xc739e9d5d3e55537e703012c6d162c37e3b06bc4ce2456570c097b7421290ef6")
        resp = ethstub.GetTransaction(request)
        tx = json.loads(resp.transaction)
        print(tx)


if __name__ == '__main__':
    logging.basicConfig()
    run()