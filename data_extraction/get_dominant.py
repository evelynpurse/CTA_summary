import numpy as np
import pandas as pd
import rqdatac as rq
from rqdatac import *
rq.init()

startdate=pd.to_datetime('20100104')
enddate=pd.to_datetime('20190329')
cat_list=pd.read_csv("cat_list.csv",header=None)
cat_list=pd.Series(cat_list.iloc[:,0])
df=pd.DataFrame()
#分品种提取主力合约
for i in range(0,len(cat_list)):
    dominants=rq.get_dominant_future(cat_list[i],start_date=startdate,end_date=enddate)
    df=df.join(pd.DataFrame(dominants),how='outer',rsuffix=cat_list[i])
df=df.reset_index()
df=df.rename(columns={'dominant':'dominantA'})
df.to_csv("dominants.csv",index=None)