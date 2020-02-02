import pandas as pd
import numpy as np

future_price=pd.read_csv("../../data_extraction/future_price.csv")
future_info=pd.read_csv("../../data_extraction/future_info.csv")
future_price=future_price.set_index('order_book_id')
future_info=future_info.set_index('order_book_id')
combined=future_price[['date','total_turnover']].join(future_info['underlying_symbol'])
combined=combined.reset_index()
combined=combined.set_index(['date','underlying_symbol'])
amount=combined.groupby(level=[0,1])['total_turnover'].sum()
amount=pd.DataFrame(amount).unstack(level=1)
amount.columns=amount.columns.droplevel(level=0)


adjust_price=pd.read_csv("../../adjust_price/adjust_price.csv",index_col=0)
daily_rt=adjust_price/adjust_price.shift(1)-1
daily_liq=amount/abs(daily_rt)
##可调参处 原文取得是2个月 40day
for R in range(5,41,5):
    single=daily_liq.rolling(R,min_periods=R).mean().shift(1)
    single=single.reset_index()
    single.to_csv("liquidity_R"+str(R)+".csv",index=None)

