from datetime import date

# 取得時間權重的物件
class month_repot_day():
    def __init(self):
        pass
        
    
    def date_count(self,start_date):
        """
        使用datetime.date計算
        """
        self.date = start_date
        self.year = start_date.year
        self.month = start_date.month
        self.day = start_date.day
        
        if self.day>10:
            # 如小於12 年份不用進位
            if self.month <12:
                self.end_month = self.month + 1
                self.end_year = self.year
            else :
                self.end_month = 1
                self.end_year = self.year+1
        else :
            # 保持不變
            self.end_year = self.year
            self.end_month = self.month

        # 將日期轉換成字串處理
        out_day = str(date(self.end_year,self.end_month,10)-self.date).split()
        if len(out_day)>2:
            if int(out_day[0])>0 :
                days = int(out_day[0])
            # 因其權重不希望為0 故給予最小權重分子
            else :
                days = 1
        else:
            days = 1
        self.days = days
        
        
        
    def month_weight(self):
        # 計算當月權重
        # 因為要計算上個月(1月要讀取12月)
        if self.month>1 :
            # 10號以後讀取下個月的權重
            if self.day>10:
                all_day = date(self.end_year,self.end_month,10)-date(self.year,self.month,10)
            elif self.day<=10:
                all_day = date(self.end_year,self.end_month,10)-date(self.year,self.month-1,10)
        elif self.month == 1:
            # 讀取下月權重保持不變
            if self.day>10:
                all_day = date(self.end_year,self.end_month,10)-date(self.year,self.month,10)
            # 讀取前年權重 年分減1
            elif self.day<=10:
                all_day = date(self.end_year,self.end_month,10)-date(self.year-1,12,10)

        return self.days/(int(str(all_day).split()[0]))
