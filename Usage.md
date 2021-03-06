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

We provide a Ropsten test account with about 3 ether for ease of setup; its private key is in the "privatekey-ropsten" file, its keystore file is "UTC--2017-12-17T17-33-34.988067000Z--aa08901e5673593c51ee4439b8ff9639a09fe892", and its password is "testacc".

To run the client, put the client.py file in its own folder, along with instructions.txt and a small plaintext file you want to encrypt (do not put anything else, or it will be encrypted!). Then, run
```
python client.py
```
and follow the instructions.txt file.

Troubleshooting---
If, when running the server, you have an import error related to importing Text from a typing library, just delete all references to Text in that method. This seems to be a bug related to the beta 4 of web3py.