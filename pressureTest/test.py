from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import uuid
import time
import threading
import time

max_thread_number =30
transfer_test_time = 100
class Test(threading.Thread):
    def __init__(self):
        # self.w3 = Web3(HTTPProvider('http://localhost:8545'))   #use rpc
        threading.Thread.__init__(self)
        self.w3=Web3(Web3.IPCProvider("~/.ethereum/geth.ipc"))   #use ipc
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0) 
        self.w3.isConnected(),'connect fail 请打开geth'
        self.ourAddress =self.w3.toChecksumAddress("0x4ffa4508e02cc585f5ea209967039ba345effc88")
        self.key = '0xda17f8c80a071f1fc8c84df601f4c9f0e1d864e7961d93c6b4245b9246874f17'
    
    def run(self):
            self.new_account()
    def new_account(self):
        password = str(uuid.uuid4())
        start_time = time.time()
        account = self.w3.personal.newAccount(password)
        end_time = time.time()
        timeused = end_time-start_time
        print("新建账户{}成功 用时{}秒 ".format(account,timeused))
        return account
    def getAccount(self,account_index):
        return self.w3.eth.accounts[account_index]
    def transfer(self,to):
        start_time = time.time()
        nonce = self.w3.eth.getTransactionCount(self.ourAddress) 
        transaction = {
            'to': to,
            'value': 1000000000,       
            'gas': 2000000,
            'gasPrice': 2100000,
            'nonce': nonce
        }
        #签名
        signed = self.w3.eth.account.signTransaction(transaction, self.key)
        #When you run sendRawTransaction, you get back the hash of the transaction:
        transactionHash=self.w3.eth.sendRawTransaction(signed.rawTransaction)  
        transaction=self.w3.eth.waitForTransactionReceipt(transactionHash)
        finishTime = time.time()
        timeused = finishTime - start_time
        print("交易{} 打包成功 to的账户余额为{} 用时{}秒".format(transaction.transactionHash.hex(),self.getBalance(to),timeused))

    def getBalance(self,to):
        return int(self.w3.eth.getBalance(to))

if __name__ == "__main__":
    
    #test transfer 

    # test = Test()
    # for index in range(transfer_test_time):
    #     account = test.w3.toChecksumAddress(test.getAccount(index))
    #     test.transfer(account)
    
    #test newAccount
    test = Test()
    for index in range(max_thread_number):
        test.new_account()