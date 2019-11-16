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
git submodule update --init --recursive # initialize remix submodule after first clone
git submodule update --recursive --remote # update
```