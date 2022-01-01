"""
计算factor, 需要的是h
h是一个df, 其中需要包括如下的列:
1 ts_code
2 trade_day(ts_code 同一天的)
3 circ_mv
4 pb
5 roe_yearly
6 pct_chg
输出的是, 因子列, 包括:
smb, hml, rmw
"""
import pandas as pd


class CalFactor(object):
    def __init__(self ):
        self.columns = ['smb', 'hml', 'rmw']
        self.h = pd.DataFrame(columns=self.columns)
        self.result = []

    def cal_factor(self, df):

# 四因子面板数据：计算规模SMB、价值HML、盈利RMW
# [guoze] so 我需要的是一个df,其中包括了`circ_mv`, `pb`, `roe_yearly`, `close`
# [guoze] 其中df是每日的, 居然!!!, 不是历史的, 是日线的, it means, 每天的行情是这样的
# [guoze] 那么问题来了, 日线的因子和日线的return回归, 得到的alpha是什么
    
    # 1、划分大小市值公司：流通市值30分位以下为小市值组（S）、中位数以上为大市值组（B）
# [guoze] circ_mv是流通市值,median是中位数, 中位数以上是大, 中位数一下是小
        print('in__call__')
        df['SB'] = df['circ_mv'].map(lambda x: 'B' if x >= df['circ_mv'].median() else 'S')
        
        # 2、划分高、中、低账面市值比公司：BM 30分位以下为成长组（L）、70分位以上为价值组（H），之间的为中间组（M）
    # [guoze] pb是啥, 账面市值比
    # [guoze] 按照之前的了解,账面市值比应该是股东权益和市值的比值, pb就直接可以算了,pb来自于哪里
        # 先求账面市值比：PB的倒数

        df['BM'] = 1 / df['pb']
        
        bm_border_down, bm_border_up = df['BM'].quantile([0.3, 0.7])
        bm_border_down, bm_border_up
        df['HML'] = df['BM'].map(lambda x: 'H' if x >= bm_border_up else 'M')
        df['HML'] = df.apply(lambda row: 'L' if row['BM'] <= bm_border_down else row['HML'], axis=1)
        
        # 3、划分高、中、低盈利的公司：ROE 30分位以下为低盈利
        roe_border_down, roe_border_up = df['roe_yearly'].quantile([0.3, 0.7])
        roe_border_down, roe_border_up
        df['RMW'] = df['roe_yearly'].map(lambda x: 'R' if x >= roe_border_up else 'N')
        df['RMW'] = df.apply(lambda row: 'W' if row['roe_yearly'] <= roe_border_down else row['RMW'], axis=1)
        
        # 4、组合划分
        # 4.1、价值因子（HML）分组和计算:
        # 组合划分为6组
        df_SL = df.query('(SB=="S") & (HML=="L")')
        df_SM = df.query('(SB=="S") & (HML=="M")')
        df_SH = df.query('(SB=="S") & (HML=="H")')
        df_BL = df.query('(SB=="B") & (HML=="L")')
        df_BM = df.query('(SB=="B") & (HML=="M")')
        df_BH = df.query('(SB=="B") & (HML=="H")')
        
        # 计算各组收益率
        R_SL = (df_SL['pct_chg'] * df_SL['circ_mv'] / 100).sum() / df_SL['circ_mv'].sum()
        R_SM = (df_SM['pct_chg'] * df_SM['circ_mv'] / 100).sum() / df_SM['circ_mv'].sum()
        R_SH = (df_SH['pct_chg'] * df_SH['circ_mv'] / 100).sum() / df_SH['circ_mv'].sum()
        R_BL = (df_BL['pct_chg'] * df_BL['circ_mv'] / 100).sum() / df_BL['circ_mv'].sum()
        R_BM = (df_BM['pct_chg'] * df_BM['circ_mv'] / 100).sum() / df_BM['circ_mv'].sum()
        R_BH = (df_BH['pct_chg'] * df_BH['circ_mv'] / 100).sum() / df_BH['circ_mv'].sum()
        
        # 计算HML
        hml = (R_SH + R_BH - R_SL - R_BL) / 2
        
        # 4.2、盈利因子（RMW）分组和计算：
        # 组合划分为6组
        df_SR = df.query('(SB=="S") & (RMW=="R")')
        df_SN = df.query('(SB=="S") & (RMW=="N")')
        df_SW = df.query('(SB=="S") & (RMW=="W")')
        df_BR = df.query('(SB=="B") & (RMW=="R")')
        df_BN = df.query('(SB=="B") & (RMW=="N")')
        df_BW = df.query('(SB=="B") & (RMW=="W")')
        
        # 计算各组收益率
        R_SR = (df_SR['pct_chg'] * df_SR['circ_mv'] / 100).sum() / df_SR['circ_mv'].sum()
        R_SN = (df_SN['pct_chg'] * df_SN['circ_mv'] / 100).sum() / df_SN['circ_mv'].sum()
        R_SW = (df_SW['pct_chg'] * df_SW['circ_mv'] / 100).sum() / df_SW['circ_mv'].sum()
        R_BR = (df_BR['pct_chg'] * df_BR['circ_mv'] / 100).sum() / df_BR['circ_mv'].sum()
        R_BN = (df_BN['pct_chg'] * df_BN['circ_mv'] / 100).sum() / df_BN['circ_mv'].sum()
        R_BW = (df_BW['pct_chg'] * df_BW['circ_mv'] / 100).sum() / df_BW['circ_mv'].sum()
        
        # 计算RMW
        rmw = (R_SR + R_BR - R_SW - R_BW) / 2
        
        # 4.3、规模因子（SMB）分组和计算：
        # 组合划分。这里的规模因子较传统Fama三因子SMB不同，由于SMB分别和RMW和HML做过分组排序。这里需要考虑和计算之前与HML和RMW共同的反向交集
        # 即：SMB需要拆分为：SMB_BM 和 SMB_ROE 两部分：(SMB_BM + SMB_ROE)/2
        smb_bm = (R_SH + R_SM + R_SL - R_BH - R_BM - R_BL) / 3
        smb_roe = (R_SR + R_SN + R_SW - R_BR - R_BN - R_BW) / 3
        smb = (smb_bm + smb_roe) / 2
        
        self.result = [smb, hml, rmw]
    
    
