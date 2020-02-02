#####to calculate basis

import pandas as pd
import numpy as np

data=pd.read_csv("../roll_rt/ts_price_date.csv")
data=data[['underlying_symbol','date','near1_p','near2_p','far_p','near1_d','near2_d','far_d']]

basis=data[['underlying_symbol','date']]
basis['basis1']=365*(data['near1_p']/data['near2_p']-1)/(pd.to_datetime(data['near2_d'])-pd.to_datetime(data['near1_d'])).dt.days
basis['basis2']=365*(data['near1_p']/data['far_p']-1)/(pd.to_datetime(data['far_d'])-pd.to_datetime(data['near1_d'])).dt.days
basis=basis.set_index(['underlying_symbol','date'])
basis=basis.groupby(level=0).apply(lambda x:x.shift(1))
basis=basis.reset_index()
basis.to_csv("basis.csv",index=None)