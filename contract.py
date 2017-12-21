import json
import web3

from web3 import Web3, TestRPCProvider, Account
from solc import compile_source
from web3.contract import ConciseContract
from web3.auto import w3

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract Greeter {
    string public greeting;

    function Greeter() {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Greeter']

# Generate the data field for the transaction to deploy the contract:
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
print(contract.address)
exit()
data = contract._encode_constructor_data() #Add any relevant args
# chainId 3 for Ropsten
transaction = dict(data=data, gas=200000, gasPrice=w3.eth.gasPrice, chainId=3, nonce=0, to=contract.address)

# Sign the transaction
acct = Account.privateKeyToAccount("8af9224f14c93018f8f551e14becb4a26cf95c091f12b9b56dd7ddfc25557a60") # TODO make more secure or splittable or something
signed = acct.signTransaction(transaction)

w3.eth.sendRawTransaction(signed.rawTransaction)
print(signed)