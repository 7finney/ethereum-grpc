# ethcode-tools-api monorepo
Devtools API monorepo for ETHcode

#### Run from docker container
`RT_API_HOST=api.ethcode.dev docker-compose up`

## Protogen
```
npm i @grpc/proto-loader @improbable-eng/grpc-web ts-protoc-gen
PROTOC_GEN_TS_PATH="./node_modules/.bin/protoc-gen-ts"
OUT_DIR="./generated"
protoc --plugin="protoc-gen-ts=${PROTOC_GEN_TS_PATH}" --js_out="import_style=commonjs,binary:${OUT_DIR}" --ts_out="service=grpc-web:${OUT_DIR}" services/remix-debug.proto
```