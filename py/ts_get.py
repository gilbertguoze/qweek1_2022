# %%
import pandas as pd
import tushare as ts
import datetime

class TsGet():
    def __init__(self, st, et):
        token = "24be01b7512bcbc50285bbdea1f9fd315035e784a639bab585990723"
        self.pro = ts.pro_api(token)
        self.st=st
        self.et=et
        pass
    def query(self, fn='daily', td = '20211201'):
        self.df = self.pro.query(fn, trade_date = td)
        return self.df
    def factor_df(self, fnlist, td = '20211201'):
        print(fnlist)
        # daily
        df0 = self.pro.query(fnlist[0], trade_date = td)
        print('df0',df0.info())
        # daily_basic
        df1 = self.pro.query(fnlist[1], trade_date = td)
        print('df1',df1.info())
        # fina_indicator_vip 
        df2 = self.pro.query(fnlist[2], trade_date = td)
        df2 = df2.drop_duplicates('ts_code')
        print('df2',df2.info())
        dff = pd.merge(df0, df1, \
            how='outer', on='ts_code')
        self.df4factor = pd.merge(dff, df2, \
            how='outer', on='ts_code')
        return self.df4factor
# %%
