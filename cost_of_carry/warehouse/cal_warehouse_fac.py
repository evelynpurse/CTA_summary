#to calculate warehouse receipt growth and inventory level
import pandas as pd
import numpy as np
#read data
warehouse=pd.read_csv("../../data_extraction/warehouse.csv")
cat_list=pd.read_csv("../../data_extraction/cat_list.csv",header=None)
####warehouse receipt change
warehouse=warehouse.set_index(['date','underlying_symbol'])
warehouse=pd.DataFrame(warehouse['on_warrant'])
warehouse=warehouse.unstack()
warehouse.columns=warehouse.columns.droplevel(0)
#rolling window size 10-100
for R in range(10,101,10):
    warehouse1=warehouse.shift(R)
    warehouse_change=(warehouse/warehouse1-1).shift(1)
    #deal with inf
    warehouse_change[warehouse_change==float('inf')]=np.nan
    warehouse_change.to_csv("warehouse_fac_R"+str(R)+".csv")

####inventort level
warehouse['date']=pd.to_datetime(warehouse['date'].astype('str'))
warehouse=warehouse.drop(columns='exchange')
#新建两列用来记录年和月
warehouse['year']=warehouse['date'].dt.year
warehouse['month']=warehouse['date'].dt.month
#月度总仓单数 每个月的天数
sum=warehouse.groupby(by=['underlying_symbol','year','month']).sum()
count=warehouse.groupby(by=['underlying_symbol','year','month']).count()
sum=sum.reset_index()
count=count.reset_index()
count=count.drop(columns={'date'})
count=count.rename(columns={'on_warrant':'count'})
sum=sum.rename(columns={'on_warrant':'sum'})
#计算前12个月均值
##先将count 与 sum拼接
df_combined=count.merge(sum,left_on=['underlying_symbol','year','month'],right_on=['underlying_symbol','year','month'],how='outer')
#前12个月的总天数
df_combined['trading_days']=df_combined[['count','underlying_symbol']].groupby('underlying_symbol').rolling(12,min_periods=1).sum().reset_index()['count']
#前12个月的总库存水平
df_combined['sum_inv']=df_combined[['sum','underlying_symbol']].groupby('underlying_symbol').rolling(12,min_periods=1).sum().reset_index()['sum']
#前12个月的平均库存水平
df_combined['avg_inv']=df_combined['sum_inv']/df_combined['trading_days']
#记到下一个月
df_combined['avg_inv_shift1']=df_combined.groupby('underlying_symbol')['avg_inv'].apply(lambda x:x.shift(1))
#再和warehouse合并
warehouse=warehouse.merge(df_combined[['underlying_symbol','year','month','avg_inv_shift1']],left_on=['underlying_symbol','year','month'],right_on=['underlying_symbol','year','month'],how='left')
#计算当前库存水平
warehouse['inv_level']=warehouse['on_warrant']/warehouse['avg_inv_shift1']
df_to_save=warehouse[['date','underlying_symbol','inv_level']]
df_to_save['inv_level']=df_to_save.groupby('underlying_symbol').apply(lambda x:x['inv_level'].shift(1)).reset_index()['inv_level']
df_to_save.to_csv("inv_level.csv")
