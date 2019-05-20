import sys
from web3.auto import w3
if len(sys.argv) != 3:
    print("请输入keystore路径和密码\n例如：python getPrivateKey.py" + ' /home/yapie/.web3/keys/a32140e2-7bf0-78f2-f123-5f7f061570a0.json'+' 123456')
    sys.exit(0)
keyStorePath = sys.argv[1]
password = sys.argv[2]
keyJson=None
try:
    keyFile=open(keyStorePath)
    keyJson=keyFile.read()
except IOError:
     print("Error: 没有找到文件或读取文件失败")

else:
    keyFile.close()
if keyJson:
    try:
        private_key = w3.eth.account.decrypt(keyJson, password)
        #bytes to hex string
        print("私钥是%s" %private_key.hex())
    except IOError:
        print("解锁失败")




