# Ethereum gRPC cloud network configuration info

All variations of ethereum networks (including testnetworks) running in Math & Cody cloud can be found in `networks.json`.

```
{
    "networks": [
        {
            "network": "ethereum",
            "port": 8545
        },
        {
            "network": "ethereum-light",
            "port": 8546
        }
    ]
}
```

### Run networks
```
sudo docker-compose -f networks/docker-compose-testnets.yml up -d
```