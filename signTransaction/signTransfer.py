from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import time

# w3 = Web3(HTTPProvider('http://localhost:8545'))
w3=Web3(Web3.IPCProvider("~/.ethereum/geth.ipc"))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)  #use ipc
w3.isConnected(),'connect fail 请打开geth'
ourAddress =w3.toChecksumAddress("0x4ffa4508e02cc585f5ea209967039ba345effc88")
to=w3.toChecksumAddress("0x6efb59decd7d384b79735987bffe0d84f8ae9274")
key = '0xda17f8c80a071f1fc8c84df601f4c9f0e1d864e7961d93c6b4245b9246874f17'



nonce = w3.eth.getTransactionCount(ourAddress) 
transaction = {
     'to': to,
     'value': 1000000000000000000,       #1ether
      'gas': 2000000,
     'gasPrice': 2100000,
     'nonce': nonce
}


#签名
signed = w3.eth.account.signTransaction(transaction, key)


#When you run sendRawTransaction, you get back the hash of the transaction:
transactionHash=w3.eth.sendRawTransaction(signed.rawTransaction)  
# watingMined(transactionHash)
print("waiting for mined")
transaction=w3.eth.waitForTransactionReceipt(transactionHash, timeout=120)
print("打包成功")
print(transaction)

