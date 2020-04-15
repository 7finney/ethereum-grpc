# ethcode-tools-api monorepo

Devtools API monorepo for ETHcode

#### Run from docker container

`RD_API_HOST=remixdebug.localhost RT_API_HOST=remixtests.localhost docker-compose up`

## Protogen

```
npm i @grpc/proto-loader @improbable-eng/grpc-web ts-protoc-gen
PROTOC_GEN_TS_PATH="./node_modules/.bin/protoc-gen-ts"
OUT_DIR="./generated"
protoc --plugin="protoc-gen-ts=${PROTOC_GEN_TS_PATH}" --js_out="import_style=commonjs,binary:${OUT_DIR}" --ts_out="service=grpc-web:${OUT_DIR}" services/remix-debug.proto
```

# Development

```shell
cd remix-debug-api
git submodule update --init --recursive # initialize remix submodule after first clone
git submodule update --recursive --remote # update
cd ..
RD_API_HOST=remixdebug.localhost RT_API_HOST=remixtests.localhost docker-compose up # bring up all the services
docker-compose down
docker rmi ethcode-tools-api_remix-debug-api ethcode-tools-api_remix-tests-api # take down all the images
```

# Deployment with TLS

```shell
$ chmod 600 acme.json
$ sudo PROM_HOST=prometheus.ethcode.dev TRAEFIK_HOST=traefik.ethcode.dev GRAFANA_HOST=grafana.ethcode.dev CC_API_HOST=clientcallapi.ethcode.dev RD_API_HOST=remixdebug.ethcode.dev RT_API_HOST=rtapi.ethcode.dev docker-compose up -d
```

# Etheruem GRPC API Specification

### GetTransactionReceipt

Request

```go
// Golang
// searchproto -> proto file package
c := &searchproto.GetTxReq{
		Networkid:  netID,
		Txhash:     txHash,
}
client.GetTransactionReceipt(ctx, c)

```

Returns

_Returns the receipt of a transaction by transaction hash._

```js
 {
     transactionHash: '0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238',
     transactionIndex:  '0x1', // 1
     blockNumber: '0xb', // 11
     blockHash: '0xc6ef2fc5426d6ad6fd9e2a26abeab0aa2411b7ab17f30a99d3cb96aed1d1055b',
     cumulativeGasUsed: '0x33bc', // 13244
     gasUsed: '0x4dc', // 1244
     contractAddress: '0xb60e8dd61c5d32be8058bb8eb970870f07233155', // or null, if none was created
     logs: [{
         // logs as returned by getFilterLogs, etc.
     }, ...],
     logsBloom: "0x00...0", // 256 byte bloom filter
     status: '0x1'
  }
```

### GetAccounts

Request

```go
// Golang
c := &searchproto.GetAcReq{
		Networkid:      netID,
}
client.GetAccounts(ctx, c)
```

Returns

_Returns a list of addresses owned by client._

```js
["0xc94770007dda54cF92009BFF0dE90c06F603a09f"];
```

### GetBlockNumber

Request

```go
// Golang
c := &searchproto.GetBlockReq{
		Networkid:      netID,
		BlockNumber:    blocknum,
}
client.GetBlockNumber(ctx, c)
```

Returns

_Returns information about a block by block number._

```js
{
    "number": "0x1b4", // 436
    "hash": "0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331",
    "parentHash": "0x9646252be9520f6e71339a8df9c55e4d7619deeb018d2a3f2d21fc165dde5eb5",
    "nonce": "0xe04d296d2460cfb8472af2c5fd05b5a214109c25688d3704aed5484f9a7792f2",
    "sha3Uncles": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
    "logsBloom": "0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331",
    "transactionsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
    "stateRoot": "0xd5855eb08b3387c0af375e9cdb6acfc05eb8f519e419b874b6ff2ffda7ed1dff",
    "miner": "0x4e65fda2159562a496f9f3522f89122a3088497a",
    "difficulty": "0x027f07", // 163591
    "totalDifficulty":  "0x027f07", // 163591
    "extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "size":  "0x027f07", // 163591
    "gasLimit": "0x9f759", // 653145
    "gasUsed": "0x9f759", // 653145
    "timestamp": "0x54e34e8e" // 1424182926
    "transactions": [{...},{ ... }]
    "uncles": ["0x1606e5...", "0xd5145a9..."]
  }
```

### GetBalance

Request

```go
// Golang
c := &searchproto.GetBalanceReq{
		Networkid:      netID,
		Address:        address,
}
client.GetBlockNumber(ctx, c)
```

Response

_Returns the balance of the account of given address._

```js
"0x0234c8a3397aab58"; // 158972490234375000
```

### GetBlockTransactionCount

Request

```go
// Golang
c := &searchproto.GetBlockReq{
		Networkid:      netID,
		Address:        address,
}
client.GetBlockNumber(ctx, c)
```

Response

_Returns the number of transactions in a block from a block matching the given block hash._

```js
"0xc"; // 11
```

### GetBlock

Request

```go
// Golang
c := &searchproto.GetBlockReq{
		Networkid:      netID,
		Number:         number,
}
client.GetBlock(ctx, c)
```

Response

_Returns information about a block by block number._

```js
"0xa"; // 10
```

### GetHashrate

```go
// Golang
c := &searchproto.GetHashReq{
		Networkid:      netID,
}
client.GetBlock(ctx, c)
```

Response

_Returns the number of hashes per second that the node is mining with._

```js
"0x38a";
```

### GetGasPrice

```go
// Golang
c := &searchproto.GetGasReq{
		Networkid:      netID,
}
client.GetBlock(ctx, c)
```

Response

_Returns the current price per gas in wei._

```js
"0x09184e72a000"; // 10000000000000
```
