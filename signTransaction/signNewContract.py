
from add_root_path import *
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import time
import json
import web3
from solc import compile_source
from web3.contract import ConciseContract
from contract import erc20_info
w3 = Web3(HTTPProvider('https://rinkeby.infura.io/v3/a37a634302af4836b0a1b26fdf39c6f5'))
# w3=Web3(Web3.IPCProvider("~/.ethereum/geth.ipc"))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)  #use ipc
w3.isConnected(),'connect fail 请打开geth'

# rinkeby
key = '7B026DCA40D8B63659C6433030326655901FE3E74A6B22682ED7BC4259F22AF3'
ourAddress = '0xBcb8e3ad83c61660EB46d32DdD5E27dc4C59507b'
def deploy():
    abi=erc20_info.abi
    bytecode=erc20_info.byte_code['object']
    Erc20 = w3.eth.contract(abi=abi, bytecode=bytecode)
    name='yapie'
    symbol='yp'
    totalAmount=10000
    # Submit the transaction that deploys the contract
    # nonce = w3.eth.getTransactionCount(ourAddress) 
    nonce=223
    transaction = Erc20.constructor(name,symbol,totalAmount).buildTransaction({
                'nonce': nonce,
                'gas':1400000,#火币使用的，56000一般就够了
                'gasPrice':50000000000,
        })

    signed = w3.eth.account.signTransaction(transaction,key)


    #When you run sendRawTransaction, you get back the hash of the transaction:
    transactionHash=w3.eth.sendRawTransaction(signed.rawTransaction).hex()  
    # watingMined(transactionHash)
    print(transactionHash)
    print("waiting for mined")
    transaction=w3.eth.waitForTransactionReceipt(transactionHash, timeout=120)
    print("打包成功")
    print(transaction)

if __name__ == "__main__":
    deploy()