import pandas as pd
import numpy as np

#####if 20-day volume avg >10000,can be traded in the next period

future_price=pd.read_csv("../data_extraction/future_price.csv")
future_info=pd.read_csv("../data_extraction/future_info.csv")
combined=future_price.set_index(['order_book_id'])[['date','volume']].join(future_info.set_index('order_book_id')['underlying_symbol'])
combined=combined.reset_index()
combined=combined.groupby(by=['date','underlying_symbol'])['volume'].sum()
combined=combined.reset_index()
combined=combined.set_index(['underlying_symbol','date'])
combined=combined.unstack(level=0)
combined.columns=combined.columns.droplevel(0)

#rolling 20d mean
check_vol=combined.rolling(20).mean()
#if 20d volume mean>10000, set value=1
check_vol[check_vol>=10000]=1
check_vol[check_vol!=1]=0
check_vol=check_vol.reset_index()
check_vol.to_csv("check_vol.csv",index=None)