This project uses Python 3.5. First, install all of the requirements from requirements.txt

```
pip install -r requirements.txt
```
or, if necessary,
```
sudo -H pip install -r requirements.txt
```

To run the server, you first need to install [geth](https://github.com/ethereum/go-ethereum/releases), then run
```
geth --testnet --cache=512 --rpcapi="db,eth,net,web3,personal,web3" --rpc console
```
to start syncing the blockchain on testnet (Ropsten). Once the blockchain is synced to the latest block [here](ropsten.etherscan.io), you can run these commands
```
export FLASK_APP=server.py
flask run
```

We provide a Ropsten test account with about 3 ether; its credentials are already in the files.

To run the client, simply run
```
python client.py
```
and follow the instructions.

Troubleshooting---
If, when running the server, you have an import error related to importing Text from a typing library, just delete all references to Text in that method. This seems to be a bug related to the beta.