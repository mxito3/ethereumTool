from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import time

import json
import web3
from solc import compile_source
from web3.contract import ConciseContract
# w3 = Web3(HTTPProvider('http://localhost:8545'))
w3=Web3(Web3.IPCProvider("~/.ethereum/geth.ipc"))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)  #use ipc
w3.isConnected(),'connect fail 请打开geth'
ourAddress =w3.toChecksumAddress("0x4ffa4508e02cc585f5ea209967039ba345effc88")
to=w3.toChecksumAddress("0x6efb59decd7d384b79735987bffe0d84f8ae9274")
key = '0xda17f8c80a071f1fc8c84df601f4c9f0e1d864e7961d93c6b4245b9246874f17'
nonce = w3.eth.getTransactionCount(ourAddress) 

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.21;

contract Greeter {
    string public greeting;

    function Greeter() public {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() view public returns (string) {
        return greeting;
    }
}
'''
abi='[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]'
# set pre-funded account as sender
# w3.eth.defaultAccount = ourAddress

contract_address = w3.toChecksumAddress('0x789787557f2DcBF771a38f9a21e12Af4bc12be04')

# Greeter.
# # Submit the transaction that deploys the contract
# tx_hash = Greeter.constructor().transact().

# # Wait for the transaction to be mined, and get the transaction receipt
# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

greeter = w3.eth.contract(
    address=contract_address,
    abi=abi,
)
print('Default contract greeting: {}'.format(
    greeter.functions.greet().call()
))

greetWords = "i am yapie hei hei hei"
transaction = greeter.functions.setGreeting(greetWords).buildTransaction({
    'gas': 2000000,
    'gasPrice': 2100000,
    'nonce': nonce
})


#签名
signed = w3.eth.account.signTransaction(transaction, key)


#When you run sendRawTransaction, you get back the hash of the transaction:
transactionHash=w3.eth.sendRawTransaction(signed.rawTransaction)  
print("waiting for mined")
tx_receipt=w3.eth.waitForTransactionReceipt(transactionHash, timeout=120)


print("打包成功{}".format(tx_receipt))


time.sleep(10)

# Display the default greeting from the contract

