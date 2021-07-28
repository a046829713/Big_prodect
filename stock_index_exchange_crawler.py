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

    index_df = pd.DataFrame()
    ex_df = pd.DataFrame()
    for month in month_list:
        # 大盤指數
        url = "https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json&date=" + month
        res = req.get(url)
        stock_json = res.json()
        stock_df = pd.DataFrame.from_dict(stock_json["data"])
        index_df = index_df.append(stock_df, ignore_index=True)
        # 成交量
        url2 = "https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date="+ month
        res2 = req.get(url2)
        exchange_json = res2.json()
        exchange_df = pd.DataFrame.from_dict(exchange_json["data"])
        ex_df = ex_df.append(exchange_df, ignore_index=True)
        time.sleep(random.randint(15, 20))

    df = pd.concat([index_df, ex_df], axis=1, ignore_index=True)
    df = df.drop([5,9], axis=1)
    df.columns = ['Date', '開盤價', '最高價', '最低價', '收盤價', '成交股數', '成交金額', '成交筆數', '漲跌點數']
    return df

stock = get_stock_data(start_year = 2018, start_month = 7, end_year = 2021, end_month = 7)
conn = sql.connect("stock_index_exchange.db")

stock.to_sql("stock_index_exchange.db", conn, if_exists="replace")
# print(stock)