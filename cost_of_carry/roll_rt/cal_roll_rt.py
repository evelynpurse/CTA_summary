#to determine front dominant second-front second-dominant contract
import pandas as pd
import numpy as np

##read data
future_info=pd.read_csv("../../data_extraction/future_info.csv")
future_price=pd.read_csv("../../data_extraction/future_price.csv")
future_price=future_price.set_index(['order_book_id'])[['date','close','volume']]
future_info=future_info[['order_book_id','maturity_date','underlying_symbol']]
future_info=future_info.set_index('order_book_id')

df=future_info.join(future_price,how='outer')
df=df.reset_index()
#build a function

def func1(df1):
    df_return = pd.DataFrame(index=[0],columns=['near1','near2','far','domain1','domain2'])
    df1=df1.reset_index()
    df1=df1.set_index('order_book_id')
    if(len(df1)>=2):
        near1 = df1.sort_values(by='maturity_date', ascending=True).index.values[0]
        near2 = df1.sort_values(by='maturity_date', ascending=True).index.values[1]
        far = df1.sort_values(by='maturity_date', ascending=False).index.values[0]
        domain1=df1.sort_values(by='volume',ascending=False).index.values[0]
        domain2=df1.sort_values(by='volume',ascending=False).index.values[1]
    else:
        near1=df1.sort_values(by='maturity_date', ascending=True).index.values[0]
        near2=near1
        far=near1
        domain1=near1
        domain2=near1
    df_return.iloc[0,0]=near1
    df_return.iloc[0,1]=near2
    df_return.iloc[0,2]=far
    df_return.iloc[0,3]=domain1
    df_return.iloc[0,4]=domain2
    return df_return

df_id=df.groupby(by=['underlying_symbol','date']).apply(func1)
df_id.index=df_id.index.droplevel(level=2)
df_id=df_id.reset_index()
df_id.to_csv("term_struct_id.csv",index=None)



