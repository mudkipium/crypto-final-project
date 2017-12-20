from web3 import Web3, HTTPProvider, IPCProvider
import json
web3 = Web3(HTTPProvider('https://rinkeby.infura.io'))
web3.personal.unlockAccount("0xF5f065427d8e011963381824dcA5A4427f3A9C29", "returnsovertime")
with open('elf-abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)
    contract_address = '0x18dbe22c44fbb8024961edf33d286e9eb16062a8'
    contract = web3.eth.contract(abi, contract_address)
    print(contract.transact().hash(22))
print(web3.eth.blockNumber)