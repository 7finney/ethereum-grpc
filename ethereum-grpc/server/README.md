# Getting started
```
python3 -m virtualenv venv
source venv/bin/activate
cd server/
pip install -r requirements.txt
pip freeze > requirements.txt
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