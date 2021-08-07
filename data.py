"""
to take date in sql
如果使用 read_sql 
會造成需要使用的資料每次都需要connect 
故整合為 物件
"""
# 2021.07.29
import sqlite3
import pandas as pd
import os
import datetime

class Data():
    def __init__(self):

        # 開啟資料庫 
        self.conn = sqlite3.connect(os.path.join('data', "StockData.db"))
        # 將所有table名稱讀取出來
        cursor = self.conn.execute('SELECT name FROM sqlite_master WHERE type = "table"')
        
        # 找到所有的table名稱 回傳形式為(parmes,)
        table_names = [t[0] for t in list(cursor)] 
        
        # 找到所有的column名稱，對應到的table名稱
        self.col2table = {}
        for tname in table_names:

            # 獲取所有column名稱
            c = self.conn.execute('PRAGMA table_info(' + tname + ');')
            for cname in [i[1] for i in list(c)]:

                # 將column名稱對應到的table名稱assign到self.col2table中
                self.col2table[cname] = tname
        # print(self.col2table)
        # 初始self.date（使用data.get時，可以獲得self.date以前的所有資料（以防拿到未來數據）
        self.date = datetime.datetime.now().date()# 用現在時間當作後一天
        
        # 假如self.cache是true的話，
        # 使用data.get的資料，會被儲存在self.data中，之後再呼叫data.get時，就不需要從資料庫裡面找，
        # 直接調用self.data中的資料即可
        self.cache = False
        self.data = {}
        
        # 先將每個table的所有日期都拿出來
        self.dates = {}

        # 對於每個table，都將所有資料的日期取出
        for tname in table_names:
            c = self.conn.execute('PRAGMA table_info(' + tname + ');')
            cnames = [i[1] for i in list(c)]
            if 'date' in cnames:
                if tname == 'stock_price':
                    
                    # 假如table是股價的話，則觀察這三檔股票的日期即可（不用所有股票日期都觀察，節省速度）
                    s1 = (f"SELECT DISTINCT date FROM {tname} where stock_id='0050'")
                    s2 = (f"SELECT DISTINCT date FROM {tname} where stock_id='1101'")
                    s3 = (f"SELECT DISTINCT date FROM {tname} where stock_id='2330'")

                    # 將日期抓出來並排序整理，放到self.dates中
                    df = (pd.read_sql(s1, self.conn)
                          .append(pd.read_sql(s2, self.conn))
                          .append(pd.read_sql(s3, self.conn)))
                    # 將相同的值丟掉(若當天有股價沒收進 也有其他股票會收進資料)(由小到大排序)
                    df = df.drop_duplicates('date').sort_values('date')
                    
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.set_index('date')
                    self.dates[tname] = df
                else:
                    # 將日期抓出來並排序整理，放到self.dates中
                    s = (f"SELECT DISTINCT date FROM {tname}")
                    self.dates[tname] = pd.read_sql(s, self.conn, parse_dates=['date'], index_col=['date']).sort_index()
        
    def get(self, name, n):
        
        # 確認名稱是否存在於資料庫 n=讀取資料筆數
        if name not in self.col2table or n == 0:
            print('Data: **ERROR: cannot find', name, 'in database')
            return pd.DataFrame()
        
        # 找出欲爬取的時間段('收盤價': 'stock_price')（startdate, enddate）
        df = self.dates[self.col2table[name]].loc[:self.date].iloc[-n:]
        
        try:
            startdate = df.index[-1]
            enddate = df.index[0]
        except:
            print('Data: **WARRN: data cannot be retrieve completely:', name)
            enddate = df.iloc[0]
        
        # 假如該時間段已經在self.data中，則直接從self.data中拿取並回傳即可
        # print(self.data)
        if name in self.data and self.contain_date(name, enddate, startdate):
            return self.data[name][enddate:startdate]
        
        # 從資料庫中拿取所需的資料
        s = ("""SELECT stock_id, date, [%s] FROM %s WHERE date BETWEEN '%s' AND '%s'"""%(name, 
            self.col2table[name], str(enddate.strftime('%Y-%m-%d')), 
            str((self.date + datetime.timedelta(days=1)).strftime('%Y-%m-%d'))))
        ret = pd.read_sql(s, self.conn, parse_dates=['date']).pivot(index='date', columns='stock_id')[name]
        
        # 將這些資料存入cache，以便將來要使用時，不需要從資料庫額外調出來
        if self.cache:
            print(self.cache)
            self.data[name] = ret

        return ret
    
    # 確認該資料區間段是否已經存在self.data
    # EX:name = "收盤價"
    def contain_date(self, name, startdate, enddate):
        if name not in self.data:
            return False
        if self.data[name].index[0] <= startdate <= enddate <= self.data[name].index[-1]:
            return True
        
        return False



if __name__ == "__main__":
    app = Data()
    app.get("開盤價",1000)
#     print(app.dates['stock_price'].loc[:app.date])