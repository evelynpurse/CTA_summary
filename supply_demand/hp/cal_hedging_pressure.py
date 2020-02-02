import pandas as pd
import numpy as np

long_rank=pd.read_csv("../../data_extraction/long_rank.csv")
short_rank=pd.read_csv("../../data_extraction/short_rank.csv")
long_rank=long_rank.rename(columns={'commodity_id':'underlying_symbol'})
short_rank=short_rank.rename(columns={'commodity_id':'underlying_symbol'})
def cumulate(df_raw):
    #新建一个数据框 存储各种top
    sr=df_raw['volume']
    df=pd.DataFrame(index=[0],columns=['top5','top10','top20'])
    #先判断长度
    if(len(sr)<5):
        df.iloc[0,0]=sr.sum()
        df.iloc[0,1]=None
        df.iloc[0,2]=None
    elif(len(sr)<10):
        df.iloc[0,0]=sr[:5].sum()
        df.iloc[0,1]=sr.sum()
        df.iloc[0,2]=None
    else:
        df.iloc[0,0]=sr[:5].sum()
        df.iloc[0,1]=sr[:10].sum()
        df.iloc[0,2]=sr.sum()
    return df



long_df=long_rank.groupby(['trading_date','underlying_symbol']).apply(cumulate)
long_df.index=long_df.index.droplevel(2)
long_df=long_df.reset_index()

short_df=short_rank.groupby(['trading_date','underlying_symbol']).apply(cumulate)
short_df.index=short_df.index.droplevel(2)
short_df=short_df.reset_index()

long_df.to_csv("long_count.csv")
short_df.to_csv("short_count.csv")