import pandas as pd
import  numpy as np
import statsmodels.api as sm
import time

time_start=time.time()

#用品种日度收益率对动量 期限结构 市场β 回归
#按照文献原始定义 动量取前12个月涨跌幅 R=250
mom=pd.read_csv("../../technique/momentum/mom_R250.csv")
mom=mom.set_index('date')
mom=mom.shift(-1)
mom=mom.stack(dropna=False).reset_index()
mom=mom.rename(columns={'level_1':'underlying_symbol',0:'mom'})
#期限结构取 basis1 近月 次近月
basis=pd.read_csv("../../cost_of_carry/basis/basis.csv")
basis=basis[['date','underlying_symbol','basis1']]
#市场β取 nh
market=pd.read_csv("../../data_extraction/NH.csv")
market=market.set_index('date')
market=market.pct_change()
market=market.reset_index()
market['date']=pd.to_datetime(market['date']).dt.date
market['date']=market['date'].apply(lambda x:x.strftime("%Y-%m-%d"))
market=market.rename(columns={'close':'market'})

#读取品种复权收盘价
price=pd.read_csv("../../adjust_price/adjust_price.csv")
price=price.set_index('date')
price=price.pct_change()
price=price.stack(dropna=False).reset_index()
price=price.rename(columns={'level_1':'underlying_symbol',0:'price'})
#把这些数据拼接起来
df_combined=price.merge(basis,left_on=['date','underlying_symbol'],right_on=['date','underlying_symbol'],how='left')
df_combined=df_combined.merge(mom,left_on=['date','underlying_symbol'],right_on=['date','underlying_symbol'],how='left')
df_combined=df_combined.merge(market,left_on=['date'],right_on=['date'],how='left')
#由于basis中存在inf 把inf转化为nan
df_combined['basis1'][df_combined['basis1']==float('inf')]=np.nan
######回归部分
#函数1 fun1 rolling
def fun1(df,R):
    resid_df=df[['date']]
    resid_df=pd.DataFrame(data=resid_df.values)
    resid_df=resid_df.rename(columns={0:'date'})
    resid_df['resid']=None
    for i in range(0,len(df)-R):
        all_data=df.iloc[i:i+R,1:].dropna()
        if (len(all_data)>=R-20):
            y = all_data.iloc[:,0].values
            x = all_data.iloc[:, 1:].values
            X=sm.add_constant(x)
            model=sm.OLS(y,X)
            results=model.fit()
            resid=results.resid.std()
        else:
            resid=np.nan
        resid_df.iloc[i+R,1]=resid
    return resid_df


for R in [120,150,200,250]:
    df = df_combined.groupby(by='underlying_symbol').apply(fun1,R)
    df = df.reset_index()
    df = df.drop(columns=['level_1'])
    df=df.pivot(index='date',columns='underlying_symbol',values='resid')
    #shift1
    df=df.shift(1)
    df=df.stack(dropna=False).reset_index()
    df=df.rename(columns={0:'resid'})
    df.to_csv("idio_vol"+str(R)+".csv",index=None)
time_end=time.time()
print('totally cost',time_end-time_start)
