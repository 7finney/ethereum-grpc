# Getting started
```
cd ethereum-grpc/src/
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt
python server.py
```

# Development
1. Generate protocol buffers
```
python3 -m grpc_tools.protoc -I./src/protoeth --python_out=./ --grpc_python_out=./ ./src/protoeth/ethereum.proto
```

# Deploy docker image to server
### Staging image
```
docker build . -t gcr.io/eth-devtools-api-dev/staging/remix-debug:0.5 --no-cache
docker push
```
### Production image
```
docker build . -t gcr.io/eth-devtools-api-dev/ethereum-grpc-api:production --no-cache
docker push gcr.io/eth-devtools-api-dev/ethereum-grpc-api:latest
```