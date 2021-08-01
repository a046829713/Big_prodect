import sqlite3 as sql
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import time


dbfile = "StockData.db"
conn = sql.connect(dbfile)
cursor = conn.cursor()
# s = "2330"
#列出該檔股票近30天的資訊
# df = pd.read_sql("SELECT 收盤價 FROM stock_price where stock_id = '{}' order by date DESC limit 30".format(s), conn)
# close5 = df.rolling(5, min_periods=5).mean()
# close10 = df.rolling(10, min_periods=10).mean()
# close20 = df.rolling(20, min_periods=20).mean()
# print(close20.iloc[-1] > close20.iloc[-2])



# 抓取每檔股票的5,10,20日值並收集成一個字典{"key":[values],}
def pick_stock():
    # 列出所有股票代號
    df2 = pd.read_sql("SELECT DISTINCT stock_id FROM stock_price;", conn)
    id_list = df2["stock_id"].to_list()
    # print(id_list)
    # dic = {}
    for stockid in id_list:
        df = pd.read_sql("SELECT date,成交筆數,收盤價 FROM stock_price WHERE stock_id='{}' order by date DESC limit 30".format(stockid), conn).iloc[::-1]
        

        #5.10.20日均線
        close5 = df["收盤價"].rolling(5, min_periods=5).mean()
        close10 = df["收盤價"].rolling(10, min_periods=10).mean()
        close20 = df["收盤價"].rolling(20, min_periods=20).mean()
        
        volume = df["成交筆數"].mean()

        a = close5.iloc[-1] > close10.iloc[-1] 
        b = close10.iloc[-1] > close20.iloc[-1] 
        c = close5.iloc[-5] < close10.iloc[-5] 
        d = close10.iloc[-5] < close20.iloc[-5]
        e = volume > 5000
        condition = a&b&e
        if condition.all():
            print(stockid)
            df.plot(y="收盤價", label="close")
            close5.plot(label="5m", color ="yellow")
            close10.plot(label="10m", color ="blue")
            close20.plot(label="20m", color ="purple")
            # plt.xlabel('Date', fontsize = 14)
            # plt.xlim(xmax=2)
            # # plt.xticks(rotation=90)
            plt.legend(loc='upper left')
            plt.title(stockid)
            plt.show()
            time.sleep(10)

        

    
        

pick_stock()

