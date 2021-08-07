import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from data import Data
from month_report_day import month_repot_day


# 取得資料
data = Data()

# 可以查詢table 的名稱
# data.col2table

# 取得要使用的data
Open = data.get("開盤價",1000)
High = data.get("最高價",1000)
Low = data.get("最低價",1000)
Close = data.get("收盤價",1000)
Volume = data.get("成交股數",1000)
Volume_money = data.get("成交金額",1000)
Volume_Multiple = data.get("成交筆數",1000)
monthly_flow = data.get("當月營收",1000)
before_monthly_flow = data.get("上月營收",1000)
before_year_monthly_flow = data.get("去年當月營收",1000)
total_monthly_flow = data.get("當月累計營收",1000)

# =============
# 取得時間權重物件
MRD = month_repot_day()
# =============

# 股票標的
# stock_test = "4919"


def stock_all_train_data(stock_test):
    weight = []

    for date_take in Close[stock_test].index:
        datestr = date_take.strftime('%Y-%m-%d')
        MRD.date_count(datetime.strptime(datestr, "%Y-%m-%d").date())
        weight.append(MRD.month_weight())
        
    # 如果現在的時間 介於(這個月的10號 和下個月的10號)(讀取這個月的財報)
    time_list = []
    for time in Close[stock_test].index:
        time = time.strftime('%Y-%m-%d')
        time = datetime.strptime(time, "%Y-%m-%d").date()
        if time.day>10:
            take_month = time.month
            take_year = time.year
        elif time.day<=10:
            if time.month ==1 :
                take_month = 12
                take_year = time.year-1
            else:
                take_month = time.month-1
                take_year = time.year
        
        time_list.append([take_year,take_month])

    new_flow = []
    bm_flow = []
    bym_flow = []
    tm_flow =[]

    # 開始讀取營收 
    for i,j in time_list:
        # 讀取相同的時間
        new_flow.append(monthly_flow[stock_test].loc[str(i)+"-"+str(j)+"-10"])
        bm_flow.append(before_monthly_flow[stock_test].loc[str(i)+"-"+str(j)+"-10"])
        bym_flow.append(before_year_monthly_flow[stock_test].loc[str(i)+"-"+str(j)+"-10"])
        tm_flow.append(total_monthly_flow[stock_test].loc[str(i)+"-"+str(j)+"-10"])

    new_df = pd.DataFrame()

    # 以下Series 都要*上權重
    new_df["weight"] = pd.Series(weight)
    new_df["monthly_flow"] = pd.Series(new_flow) * new_df["weight"]
    new_df["before_monthly_flow"] = pd.Series(bm_flow) * new_df["weight"]
    new_df["before_year_monthly_flow"] = pd.Series(bym_flow) * new_df["weight"]
    new_df["total_monthly_flow"] = pd.Series(tm_flow) * new_df["weight"]


    # 資料都不加上時間 最後重設最方便
    df = pd.DataFrame()
    df["Open"] = Open[stock_test].ffill().values
    df["High"] = High[stock_test].ffill().values
    df["Low"] = Low[stock_test].ffill().values
    df["Close"] = Close[stock_test].ffill().values
    df["Volume"] = Volume[stock_test].ffill().values
    df["Volume_money"]=Volume_money[stock_test].ffill().values
    df["Volume_Multiple"]=Volume_Multiple[stock_test].ffill().values

    # 可以查看資料圖形
    # Close['0050'].plot(color='gray')


    from backtesting.test import SMA
    # 借用 SMA 來做出指標
    def BBANDS(data, n_lookback, n_std):
        """Bollinger bands indicator"""
        hlc3 = (df["High"] + df["Low"] + df["Close"]) / 3
        mean, std = hlc3.rolling(n_lookback).mean(), hlc3.rolling(n_lookback).std()
        upper = mean + n_std*std
        lower = mean - n_std*std
        # 取得
        return upper, lower


    close = df.Close.to_numpy()
    sma10 = SMA(df["Close"], 10)
    sma20 = SMA(df["Close"], 20)
    sma50 = SMA(df["Close"], 50)
    sma100 = SMA(df["Close"], 100)
    upper, lower = BBANDS(df, 20, 2)

    # Design matrix / independent features:

    # Price-derived features
    df['X_SMA10'] = (close - sma10) / close
    df['X_SMA20'] = (close - sma20) / close
    df['X_SMA50'] = (close - sma50) / close
    df['X_SMA100'] = (close - sma100) / close

    df['X_DELTA_SMA10'] = (sma10 - sma20) / close
    df['X_DELTA_SMA20'] = (sma20 - sma50) / close
    df['X_DELTA_SMA50'] = (sma50 - sma100) / close

    # Indicator features
    df['X_MOM'] = df["Close"].pct_change(periods=2)
    df['X_BB_upper'] = (upper - close) / close
    df['X_BB_lower'] = (lower - close) / close
    df['X_BB_width'] = (upper - lower) / close


    df = pd.concat([df,new_df],axis=1)
    df = df.set_index(Close[stock_test].index)
    # Some datetime features for good measure
    df['X_day'] = df.index.dayofweek+1 # 改變其索引直 星期一 0 +1
    df = df.dropna().astype(float)
    return df





def get_y(data):
    """Return dependent variable y"""
    # pct_change 變化率 （后一个值-前一个值）／前一个值
    # shift(往後排序) periods=3 後退3個
    y = data.Close.pct_change(1).shift(-1)  # Returns after roughly two days
    y[y.between(-.004, .004)] = 0             # Devalue returns smaller than 0.4%
    y[y > 0] = 1
    y[y < 0] = 2
    # 空值還未整理
    return y
def get_clean_Xy(df):
    """Return (X, y) cleaned of NaN values"""
    X = df
    y = get_y(df).to_numpy()
    isnan = np.isnan(y)
    X = X[~isnan]
    y = y[~isnan]
    # 將 兩者長度更改等長
    return X,y
# 尚未預處理

X,y = get_clean_Xy(stock_all_train_data(str(4919)))

print(y)