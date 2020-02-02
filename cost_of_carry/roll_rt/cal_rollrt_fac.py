#to get delivery date and price of these contracts
import pandas as pd
import numpy as np

id=pd.read_csv("term_struct_id.csv")
future_info=pd.read_csv("../../data_extraction/future_info.csv")
future_price=pd.read_csv("../../data_extraction/future_price.csv")
future_info=future_info.set_index('order_book_id')
future_price=future_price.set_index(['date','order_book_id'])


##建立函数，连接三张表
def get_datenprice(df_single_date):
    df_single_date=df_single_date.reset_index()
    df_return=pd.DataFrame(index=[0],columns=['near1_p','near2_p','far_p','domain1_p','domain2_p','near1_d','near2_d','far_d','domain1_d','domain2_d'])
    #填上收盘价
    df_return.iloc[0,0]=future_price.loc[(df_single_date.ix[0,'date'],df_single_date.ix[0,'near1']),'close']
    df_return.iloc[0, 1] = future_price.loc[(df_single_date.ix[0,'date'], df_single_date.ix[0,'near2']), 'close']
    df_return.iloc[0, 2] = future_price.loc[(df_single_date.ix[0,'date'], df_single_date.ix[0,'far']), 'close']
    df_return.iloc[0, 3] = future_price.loc[(df_single_date.ix[0,'date'], df_single_date.ix[0,'domain1']), 'close']
    df_return.iloc[0, 4] = future_price.loc[(df_single_date.ix[0,'date'], df_single_date.ix[0,'domain2']), 'close']
    #填上交割日期
    df_return.iloc[0,5]=future_info.loc[df_single_date.ix[0,'near1'],'maturity_date']
    df_return.iloc[0, 6] = future_info.loc[df_single_date.ix[0,'near2'], 'maturity_date']
    df_return.iloc[0, 7] = future_info.loc[df_single_date.ix[0,'far'], 'maturity_date']
    df_return.iloc[0, 8] = future_info.loc[df_single_date.ix[0,'domain1'], 'maturity_date']
    df_return.iloc[0, 9] = future_info.loc[df_single_date.ix[0,'domain2'], 'maturity_date']

    return df_return



df_info=id.groupby(by=['underlying_symbol','date']).apply(get_datenprice)
df_info.index=df_info.index.droplevel(level=2)
df_info=df_info.reset_index()
df_info.to_csv("ts_price_date.csv",index=None)