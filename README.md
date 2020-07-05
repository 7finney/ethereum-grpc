# Getting started
```
cd ethereum-grpc/
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt
cd src/
python server.py
```

# Development
1. Generate protocol buffers
```
python -m grpc_tools.protoc -I./src/protoeth --python_out=./ --grpc_python_out=./ ./src/protoeth/ethereum.proto
```

# Build & push docker image
```
docker build -t ethential/ethereum-grpc:latest --no-cache .
docker push ethential/ethereum-grpc:latest
```