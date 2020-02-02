import numpy as np
import pandas as pd
import rqdatac
from rqdatac import *
rqdatac.init()

startdate=pd.to_datetime('20100104')
enddate=pd.to_datetime('20190329')

cat_list=pd.read_csv("cat_list.csv",header=None)
df_warehouse=pd.DataFrame()
for i in range(0,len(cat_list)):
    single_warrant=futures.get_warehouse_stocks(cat_list.iloc[i,0], start_date=startdate, end_date=enddate)
    df_warehouse=df_warehouse.append(single_warrant)
df_warehouse=df_warehouse.reset_index()
df_warehouse.to_csv("warehouse.csv",index=None)
