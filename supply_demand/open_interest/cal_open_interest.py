####计算累计持仓量的变化率 作为因子
import pandas as pd
import numpy as np
#取得每个品种的openinterest
open_interest=pd.read_csv("../../data_extraction/future_price.csv")
future_info=pd.read_csv("../../data_extraction/future_info.csv")
open_interest=open_interest.set_index('order_book_id')
future_info=future_info.set_index('order_book_id')
open_interest=open_interest.join(pd.DataFrame(future_info['underlying_symbol']))
open_interest=open_interest.reset_index()
open_interest= open_interest.groupby(by=['date','underlying_symbol'])['open_interest'].sum()
open_interest=open_interest.reset_index()
#R取5-40，计算持仓量变化率
def cal_growth(df):
    df1=df[['date','underlying_symbol']]
    for R in range(5,41,5):
        df1['growth'+str(R)]=(df['open_interest']/df['open_interest'].shift(R)).shift(1)
    return df1
growth=open_interest.groupby('underlying_symbol').apply(cal_growth)
growth.to_csv("open_interest_growth.csv",index=None)

####需要注意，有些品种在某个时间点累计持仓量为0
###计算组合时 剔除那些因子值为infinite的
