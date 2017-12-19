from web3 import Web3, HTTPProvider, IPCProvider
import json
web3 = Web3(HTTPProvider('https://rinkeby.infura.io'))
with open('abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)
    contract_address = '0x9681Cb9709714C2890d8C888656eD811E79f5852'
    contract = web3.eth.contract(abi, contract_address)
    print(contract.call().mul(10))
print(web3.eth.blockNumber)