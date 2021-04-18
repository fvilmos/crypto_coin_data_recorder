#! /usr/bin/python
from datetime import datetime
from . import cryptoinfo
from . import safethread
import sqlite3 as sql
import sys, os, threading


class DataRecorder():
    """
    Store crypto values in a sqlite database based on coin list provided, and defined periodicity
    Author: fvilmos
    Nice tutorial: https://zetcode.com/db/sqlitepythontutorial/
    """

    def __init__(self, dbname='./data/coininfo.db', STORE_CYCLE_SEC=30, coin_list='',url='https://production.api.coindesk.com/v1/currency/ticker?currencies='):
        """
        Defines the init parameters.
        Args:
            dbname (str, optional): database name to store crypto coin values. Defaults to './data/coininfo.db'.
            STORE_CYCLE_SEC (int, optional): Periodicity to record coin data. Defaults to 30.
            coin_list (str, optional): a string of coins to be stored. Defaults to ''.
            url (str, optional): holds the Coindesk default url. Defaults to 'https://production.api.coindesk.com/v1/currency/ticker?currencies='.
        """
        
        self.con = None
        self.dbname = dbname
        self.ci =cryptoinfo.CoinInfo(url=url, coin_list=coin_list)
        
        # timebase for coin info record period
        self.cycle_time=STORE_CYCLE_SEC

        # ticker for timebase
        self.ticker = threading.Event()

        if os.path.isfile(self.dbname) is not True:
            # no database, create one
            try:
                # start with auotocommit
                self.con = sql.connect(self.dbname, isolation_level=None)
            
                with self.con:
                    cur = self.con.cursor()
                    cur.execute("DROP TABLE IF EXISTS coininfo")
                    cur.execute("CREATE TABLE coininfo(date TEXT, name TEXT, currency TEXT, price REAL, change24h_percent REAL, change24h_value REAL, change24h_low REAL, change24h_high REAL)")
                
            except sql.Error:
                print ('Error, db not created...')
                sys.exit(1)

            finally:

                if self.con:
                    self.con.close()

        # we have a database, connect to it
        self.con = sql.connect(self.dbname, isolation_level=None, check_same_thread=False)
        self.cursor = self.con.cursor()

        # start periodic storage
        self.wt = safethread.SafeThread(target=self.__worker).start()
        
    
    def __worker(self):
        """
        worker thread, called periodically
        """
        # time base
        self.ticker.wait(self.cycle_time)

        # following section will be executed periodically
        val = self.ci.get_coin_info()
        
        if val is not None:
            now = datetime.now()
            ts = str(datetime.timestamp(now))

            # tore all values in sqlite
            for coin in val:
                params = (ts,str(coin['name']),str(coin['currency']),str(coin['price']),str(coin['change24Hr_percent']),str(coin['change24Hr_value']), str(coin['change24Hr_low']),str(coin['change24Hr_high']))
                self.cursor.execute("INSERT INTO coininfo VALUES (?, ?, ?, ?, ?, ?, ?, ?)", params)


