import pandas as pd
import numpy as np

dominants=pd.read_csv("../data_extraction/dominants1.csv")
dominants=dominants.set_index('date')
future_price=pd.read_csv("../data_extraction/future_price.csv")
cat_list=pd.read_csv("../data_extraction/cat_list.csv",header=None)
cat_list=pd.Series(cat_list.groupby(cat_list.iloc[:,0]).count().index)

#build a function to adjust prices
def adj_price(sr):
    sr_switch = sr.shift(-1)
    ##set up 2 dfs one with lagged closed price, one with unlagged closed price
    # not lag
    df1 = pd.DataFrame(sr)
    df1 = df1.reset_index()
    df1.columns = ['date', 'order_book_id']
    df1 = df1.set_index(['date', 'order_book_id'])
    df1 = df1.join(future_price.loc[:, 'close'])


    # lag
    df2 = pd.DataFrame(sr_switch)
    df2 = df2.reset_index()
    df2.columns = ['date', 'order_book_id']
    df2 = df2.set_index(['date', 'order_book_id'])
    df2 = df2.join(future_price.loc[:, 'close'])

    ###calculate adjust factors
    ##divide 2 dfs
    # deal with index
    df1 = df1.reset_index()
    df2 = df2.reset_index()
    # divide
    sr_fac1 = (df1['close'] / df2['close']).shift(1)
    sr_fac1=sr_fac1.fillna(1)
    ##calculate factor
    sr_fac2 = sr_fac1.cumprod()
    ##calculate adjusted prices
    sr_adj = sr_fac2 * df1['close']
    sr_adj[0]=df1.ix[0,'close']
    sr_adj.index = sr.index

    return sr_adj
adjusted_price=dominants.apply(adj_price)
adjusted_price.columns=cat_list.values
adjusted_price=adjusted_price.reset_index()
adjusted_price.to_csv("adjust_price.csv",index=None)


test=pd.DataFrame(dominants.I)
test=test.reset_index()
test=test.rename(columns={'I':'order_book_id'})
test=test.merge(future_price[['date','order_book_id','close']],on=['date','order_book_id'])
test.to_excel("test.xls",index=None)

