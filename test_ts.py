# %%
import unittest
from ts_get import TsGet

class test_Ts(unittest.TestCase):
    def setUp(self) -> None:
        st = '20211101'
        et = '20211201'
        self.ts = TsGet(0, 1)
        pass
        # return super().setUp()
    def test_Ts(self):
        td = '20211201'
        fl = ['daily', \
            'daily_basic', \
            'fina_indicator_vip']
        self.df = self.ts.factor_df(fl,td = td)
        self.df.to_hdf('./'+td +'_factor.h5', key= 't'+td)
        print(self.df.info())
        pass

unittest.main(argv=['first-arg-ignored'], exit=False)
# # %%
# import pandas as pd
# with pd.HDFStore('./20211201_factor.h5') as tmp:
#     print(tmp.keys())
#     k = tmp.keys()[0][1:]
#     dftmp = tmp[k]
# # %%
# # print(dftmp.info())
# dftmp['circ_mv'].describe()
# dftmp['pb'].describe()
# # dftmp.loc[dftmp['pb'].isna(), 'ts_code']
# dftmp.loc[dftmp['pb'].isna(), \
#     ['roe_yearly','ts_code', 'circ_mv']].isna().sum()
# # dftmp['roe_yearly'].describe()
# dftmp['roe_yearly'].isna().sum()
# dftmp['circ_mv'].isna().sum()
# dft1 = dftmp[~dftmp['pb'].isna()].copy()
# dft1['roe_yearly'].isna().sum()
# # dft1[dft1['update_flag'] != 1].sum()
# dft2 = dft1[~dft1['roe_yearly'].isna()].copy()
# dft2.info()
# dft2.to_hdf('./20211201_factor.h5', key = 't20211201_factor')

# %%
if __name__ == '__main__':
    unittest.main()
