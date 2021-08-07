from pandas.io.sql import to_sql
from tqdm import tqdm
import sqlite3
import datetime
import pandas as pd
import requests
from crawler import crawl_price ,crawl_monthly_report,requests_get
from crawler import update_table,table_latest_date,table_earliest_date,add_to_sql
from crawler import date_range ,month_range
import time
import os
import random
#==========================================================================
conn = sqlite3.connect(os.path.join("data","StockData.db"))

# 每次執行一個系統(放入的crawl_cunc)
def last_date(conn,table_name,crawl_func,range_date):
    # 讀取第一天
    SQL_firstime = table_earliest_date(conn,table_name)
    # 讀取最後一天
    SQL_lastime = table_latest_date(conn,table_name)
    # 現在時間
    today = datetime.datetime.now().date()
    dates = range_date(SQL_lastime, today)

    print(f"資料庫擁有時間:{SQL_firstime.date()},結束時間:{SQL_lastime.date()},搜索資料庫為:{table_name}")
    # 由於已經是今天 所以直接限制時間
    if range_date ==date_range:
        # 希望可以在收盤後再收入數據 以免造成錯誤
        if time.localtime(time.time()).tm_hour>17:
            # 更新資料庫
            update_table(conn,table_name,crawl_func,dates)
    else:
        # 更新資料庫
            update_table(conn,table_name,crawl_func,dates)
    


# 將擁有的時間讀取出來
def first_date(conn,table_name,crawl_func,range_date,begin_search_date):
    # 讀取第一天
    SQL_firstime = table_earliest_date(conn,table_name)
    # 讀取最後一天
    SQL_lastime = table_latest_date(conn,table_name)
    dates = range_date(begin_search_date, SQL_firstime)
    print(f"資料庫擁有時間:{SQL_firstime.date()},結束時間:{SQL_lastime.date()},搜索資料庫為:{table_name}")
    # 更新資料庫
    # update_table(conn,table_name,crawl_func,dates)


# 向後跑取資料
# last_date(conn,"stock_price",crawl_price,date_range)
# last_date(conn,"monthly_report",crawl_monthly_report,month_range)


# 向前爬取資料 # conn 資料庫 , table_name ,fuction , range_type , date>>to update first day
# first_date(conn,"monthly_report",crawl_monthly_report,month_range,datetime.date(2014,1,10))
first_date(conn,"stock_price",crawl_price,date_range,datetime.date(2015,1,1))







conn.commit()  # 關閉
conn.close()   # 關閉資料庫連線


# =================================================================
# 若資料庫不存在 請先新增 (若不新增會報錯)(1.30.0 pandas)
# df = crawl_price(datetime.date(2021,7,30))
# df.to_sql("stock_price",conn,)

# df = crawl_monthly_report(datetime.date(2021,7,10))
# df.to_sql("monthly_report",conn)
# =================================================================
