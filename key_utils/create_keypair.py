import json,uuid
from eth_account import Account
def new_key_pair():
        password =str(uuid.uuid4())
        account = Account.create(password)
        private_key = account.privateKey.hex()
        address = account.address
        key_pair = {}
        key_pair['private_key'] = private_key
        key_pair['address'] = address
        key_pair_json = json.dumps(key_pair)
        return key_pair_json

if __name__ == "__main__":
    amount = 9
    for index in range(amount):
        key_pair=new_key_pair()
        key_pair_json = json.loads(key_pair)
        private_key = key_pair_json['private_key']
        address  = key_pair_json['address'] 
        print("私钥 {} 地址 {}".format(private_key,address))