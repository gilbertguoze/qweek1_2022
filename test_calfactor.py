# %%
import unittest

import pandas as pd
from CalFactor import CalFactor
class CFtestcase(unittest.TestCase):

    def setUp(self):
        with pd.HDFStore('./20211201_factor.h5') as tmp:
            print(tmp.keys())
            self.tdf = tmp['t20211201_factor']
        pass
    def test_calfactor(self):
        # 这个method只能针对行或者列, 不能使用df
        c = CalFactor()
        c.cal_factor(self.tdf)
        print(c.result)
        print(self.tdf[['SB','BM','HML','RMW']])
res = unittest.main(argv=[''], verbosity=3, exit=False)
# %%
# if __name__ == "__main__":
#     print('unittest===')
#     unittest.main()

# %%
# pro.query('stock_basic', name = '国科微')