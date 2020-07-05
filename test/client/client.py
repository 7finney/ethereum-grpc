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
    with grpc.insecure_channel('localhost:50054') as channel:
        ethstub = ethereum_pb2_grpc.ProtoEthServiceStub(channel)
        # txHash is of goerli testnet will give error in other testnets
        request = ethereum_pb2.GetTxReq(networkid=5, txhash="0xd3c2743bad5cc74d13083da285a9a4c1f9c98aeba215fd661ca682800b3d846a")
        resp = ethstub.GetTransaction(request)
        tx = json.loads(resp.transaction)
        print("transacion: ", tx)

if __name__ == '__main__':
    logging.basicConfig()
    run()
