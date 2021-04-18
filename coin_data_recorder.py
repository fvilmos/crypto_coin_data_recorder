from utils import datarecorder
import time
import argparse

if __name__=="__main__":

    # input arguments
    parser = argparse.ArgumentParser(description='Crypto coin data recorder.\n Deaults: -db ./data/coininfo.db -c 30 -coins "ETH"')
    parser.add_argument('-db', type=str, help='database to store info', default='./data/coininfo.db')
    parser.add_argument('-c', type=int, help='Frequency in seconds to asks for new data the recorder', default=30)
    parser.add_argument('-coins', type=str, help='String with a list of coins to be tracked, like "ETH,XRP"', default='ETH')

    args = parser.parse_args()

    # start to store info in sqlite
    cs = datarecorder.DataRecorder(STORE_CYCLE_SEC=args.c,coin_list=args.coins,dbname=args.db)

    # keep alive the storage thread
    while True:
        time.sleep(1)

