## API spec
| JSON RPC  | Web3  | protobuf  | implementation status  |
|:-:|:-:|:-:|:-:|
| `eth_protocolVersion`  | `web3.eth.getProtocolVersion([callback])`  | `GetProtocolVersion()`  | <ul><li>[ ] None</li></ul> |
| `eth_syncing`  | `web3.eth.isSyncing([callback])`  | `isSyncing()`  | <ul><li>[ ] None</li></ul> |
| `eth_coinbase`  | `web3.eth.getCoinbase([callback])`  | `GetCoinbase()`  | <ul><li>[ ] None</li></ul> |
| `eth_mining`  | `web3.eth.isMining([callback])`  | `isMining()`  | <ul><li>[ ] None</li></ul> |
| `eth_hashrate`  | `web3.eth.getHashrate([callback])`  | `GetHashrate()`  | <ul><li>[ ] None</li></ul> |
| `eth_gasPrice`  | `web3.eth.getGasPrice([callback])`  | `GetGasPrice()`  | <ul><li>[ ] None</li></ul> |
| `eth_accounts`  | `web3.eth.getAccounts()`  | `GetAccounts()`  | <ul><li>[x] None</li></ul> |
| `eth_blockNumber`  | `web3.eth.getBlockNumber([callback])`  | `GetBlockNumber()`  | <ul><li>[ ] None</li></ul> |
| `eth_getBalance`  | `web3.eth.getBalance(address [, defaultBlock] [, callback])`  | `GetBalance()`  | <ul><li>[x] None</li></ul> |
| `eth_getStorageAt`  | `web3.eth.getStorageAt(address, position [, defaultBlock] [, callback])`  | `GetStorageAt()`  | <ul><li>[ ] None</li></ul> |
| `eth_getTransactionCount`  | `web3.eth.getBlockTransactionCount(blockHashOrBlockNumber [, callback])`  | `GetBlockTransactionCount()`  | <ul><li>[ ] None</li></ul> |
| `eth_getBlockTransactionCountByHash`  | `web3.eth.getBlockTransactionCount(blockHashOrBlockNumber [, callback])`  | `GetBlockTransactionCount()`  | <ul><li>[ ] None</li></ul> |
| `eth_getBlockTransactionCountByNumber`  | `web3.eth.getBlockTransactionCount(blockHashOrBlockNumber [, callback])`  | `GetBlockTransactionCount()`  | <ul><li>[ ] None</li></ul> |
| `eth_getCode`  | `web3.eth.getCode(address [, defaultBlock] [, callback])`  | `GetCode()`  | <ul><li>[ ] None</li></ul> |
| `eth_sign`  | `web3.eth.sign(dataToSign, address [, callback])`  | `Sign()`  | <ul><li>[ ] None</li></ul> |
| `eth_sendTransaction`  | `web3.eth.signTransaction(transactionObject, address [, callback])`  | `SignTransaction()`  | <ul><li>[ ] None</li></ul> |
| `eth_call`  | `web3.eth.call(callObject [, defaultBlock] [, callback])`  | `Call()`  | <ul><li>[ ] None</li></ul> |
| `eth_estimateGas`  | `web3.eth.estimateGas(callObject [, callback])`  | `EstimateGas()`  | <ul><li>[ ] None</li></ul> |
| `eth_getBlockByHash`  | `web3.eth.getBlock(blockHashOrBlockNumber [, returnTransactionObjects] [, callback])`  | `GetBlock()`  | <ul><li>[ ] None</li></ul> |
| `eth_getBlockByNumber`  | `web3.eth.getBlock(blockHashOrBlockNumber [, returnTransactionObjects] [, callback])`  | `GetBlock()`  | <ul><li>[ ] None</li></ul> |
| `eth_getTransactionByHash`  | `web3.eth.getTransaction(transactionHash [, callback])`  | `GetTransaction()`  | <ul><li>[x] None</li></ul> |
| `eth_getTransactionByBlockHashAndIndex`  | `getTransactionFromBlock(hashStringOrNumber, indexNumber [, callback])`  | `GetTransactionFromBlock()`  | <ul><li>[ ] None</li></ul> |
| `eth_getTransactionByBlockNumberAndIndex`  | `web3.eth.getTransactionFromBlock(hashStringOrNumber, indexNumber [, callback])`  | `GetTransactionFromBlock()`  | <ul><li>[ ] None</li></ul> |
| [`eth_getTransactionReceipt`](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactionreceipt)  | [`web3.eth.getTransactionReceipt(hash [, callback])`](https://web3js.readthedocs.io/en/v1.2.0/web3-eth.html#gettransactionreceipt)  | `GetTransactionReceipt()`  | <ul><li>[ ] None</li></ul> |
| [`eth_sendRawTransaction`](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sendrawtransaction)  | [`web3.eth.sendSignedTransaction(signedTransactionData [, callback])`](https://web3js.readthedocs.io/en/v1.2.0/web3-eth.html#sendsignedtransaction)  | `SendSignedTransaction()`  | <ul><li>[ ] None</li></ul> |

# Generate protobuf
```
python3 -m grpc_tools.protoc -I./protoeth --python_out=./server/ --grpc_python_out=./server/ ./protoeth/ethereum.proto
```