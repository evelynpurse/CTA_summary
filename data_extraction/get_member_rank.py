import numpy as np
import pandas as pd
import rqdatac
from rqdatac import *
rqdatac.init()

startdate=pd.to_datetime('20100104')
enddate=pd.to_datetime('20190329')

cat_list=pd.read_csv("cat_list.csv",header=None)
trade_dates= get_trading_dates(start_date=startdate, end_date=enddate)
df_long=pd.DataFrame()
df_short=pd.DataFrame()
for i in range(0,len(trade_dates)):
    for j in range(0,len(cat_list)):
        print(cat_list.iloc[j,0]+str(trade_dates[i]))
        single_long=pd.DataFrame(futures.get_member_rank(cat_list.iloc[j,0],trading_date=trade_dates[i],rank_by='long'))
        single_short = pd.DataFrame(futures.get_member_rank(cat_list.iloc[j, 0], trading_date=trade_dates[i],rank_by='short')
                                   )
        df_long=df_long.append(single_long)
        df_short=df_short.append(single_short)
df_long=df_long.reset_index()
df_short=df_short.reset_index()
df_long.to_csv("long_rank.csv",index=None)
df_short.to_csv("short_rank.csv",index=None)