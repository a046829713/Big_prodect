import requests as req
import pandas as pd
from datetime import date
import time
import random
import sqlite3 as sql


def get_stock_data(start_year, start_month, end_year, end_month):
    start_date = str(date(start_year, start_month, 1))
    end_date = str(date(end_year, end_month, 1))
    month_list = pd.date_range(start_date, end_date, freq="MS").strftime("%Y%m%d").tolist()

    df = pd.DataFrame()
    for month in month_list:
        url = "https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json&date=" + month
        res = req.get(url)
        stock_json = res.json()
        stock_df = pd.DataFrame.from_dict(stock_json["data"])
        df = df.append(stock_df, ignore_index=True)
        time.sleep(random.randint(15, 20))

    df.columns = ['Date', '開盤價', '最高價', '最低價', '收盤價']
    return df


stock = get_stock_data(start_year = 2018, start_month = 1, end_year = 2021, end_month = 7)
conn = sql.connect("stock_index.db")

stock.to_sql("stock_index.db", conn, if_exists="replace")
