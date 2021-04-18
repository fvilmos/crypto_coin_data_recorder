from utils import cryptoinfo
import time

if __name__=="__main__":

    coin_list='ETH,XRP'
    ci_obj = cryptoinfo.CoinInfo(coin_list=coin_list)

    # keep alive the storage thread
    while True:
        val = ci_obj.get_coin_info()
        print (val)
        time.sleep(5)
