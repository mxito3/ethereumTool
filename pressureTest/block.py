# 计算出块时间
from __future__ import division
from add_root_path import *
from config.utils.eth import EthUtil
from web3 import Web3, HTTPProvider,IPCProvider

import datetime,time
w3  = Web3(IPCProvider("/home/yapie/.ethereum/geth.ipc"))
# w3.middleware_stack.inject(geth_poa_middleware, layer=0)  #use ipc
w3.isConnected(),"连接失败"
eth_util = EthUtil(w3)

calculate_need_block = 1000 # 1000个块计算一次
def block_generate_speed():
    start_time = datetime.datetime.now()
    start_block = eth_util.get_block_height()
    now_block = start_block
    blocks_has_mined = 0
    print("开始计算，区块高度是{}".format(start_block))
    while blocks_has_mined < calculate_need_block:
        now_block = eth_util.get_block_height()
        blocks_has_mined += now_block - start_block
        start_block = now_block
        print("现在区块高度{} 已经挖出{}".format(now_block,blocks_has_mined))
        time.sleep(1)

    end_time  = datetime.datetime.now()
    time_used = int( (end_time - start_time).seconds )
    print("挖出{}个块，花费{}s,平均出块时间是{}s".format(calculate_need_block,time_used,time_used/calculate_need_block))

if __name__ == "__main__":
    block_generate_speed()
