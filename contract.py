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
contract = w3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])
data = contract._encode_constructor_data(any_args, you_have, in_the_constructor)
transaction = dict(data=data, gas=...)

# Sign the transaction
acct = Account.privateKeyToAccount(your_private_key) # TODO get private key https://www.myetherwallet.com/
signed = acct.signTransaction(transaction)

w3.eth.sendRawTransaction(signed.rawTransaction)
