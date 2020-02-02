import pandas as pd
import numpy as np

#主要针对时间序列动量和hp6-8 这几个没法分组
adjust_price=pd.read_csv("../adjust_price/adjust_price.csv")
adjust_price=adjust_price.set_index('date')
cat_list=pd.read_csv("../data_extraction/cat_list.csv",header=None)
cat_list=pd.Series(cat_list[0])
#新建一个数据框记录持仓信息
port=pd.DataFrame(index=adjust_price.index,columns=adjust_price.columns)
#读入筛选条件
check_vol=pd.read_csv("../check_vol/check_vol.csv")
check_vol=check_vol.set_index('date')
check_vol=check_vol[check_vol==1]

def set_port(df):
    df_return=pd.DataFrame(index=check_vol.index,columns=check_vol.columns)
    df=df*check_vol
    df_return[df>0]=1
    df_return[df<0]=-1
    df_return=df_return.reset_index()
    return df_return

#时间序列动量
for R in [100,120,250]:
    df=pd.read_csv("../technique/momentum/mom_R"+str(R)+".csv")
    df=df.set_index('date')
    set_port(df).to_csv("ts_mom_R"+str(R)+"_port.csv",index=None)
"""
#hp6-8
for fac_num in [6,7,8]:
    fac=pd.read_csv("../supply_demand/hp/hp"+str(fac_num)+".csv")
    for R in [1,2,3,4,5,10,20]:
        for rank in [5,10,20]:
            fac_new=fac[['trading_date','underlying_symbol','R'+str(R)+'top'+str(rank)]]
            fac_new=fac_new.rename(columns={'trading_date':'date'})
            fac_new = fac_new.set_index(['underlying_symbol', 'date'])
            fac_new = fac_new.unstack(level=0)
            fac_new.columns = fac_new.columns.droplevel(level=0)
            port = set_port(fac_new)
            port.to_csv("hp"+str(fac_num)+"R"+str(R)+"top"+str(rank)+"_port.csv", index=None)
"""