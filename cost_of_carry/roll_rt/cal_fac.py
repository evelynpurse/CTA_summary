import pandas as pd
import numpy as np
import datetime

####calculate roll return
#read data
data=pd.read_csv("ts_price_date.csv")
data['date']=pd.to_datetime(data['date'])
data['near1_d']=pd.to_datetime(data['near1_d'])
data['near2_d']=pd.to_datetime(data['near2_d'])
data['far_d']=pd.to_datetime(data['far_d'])
data['domain1_d']=pd.to_datetime(data['domain1_d'])
data['domain2_d']=pd.to_datetime(data['domain2_d'])
def cal_rollrt(df):
    df=df.reset_index()
    new_df=pd.DataFrame(index=['haha'],columns=['rollrt1','rollrt2'])
    #front contract, second front contract
    if(df.ix[0,'near1_d']==df.ix[0,'near2_d']):
        rollrt1=None
    else:
        rollrt1=365*(np.log(df.ix[0,'near1_p'])-np.log(df.ix[0,'near2_p']))/(df.ix[0,'near2_d']-df.ix[0,'near1_d']).days

    #front contract, far contract
    if(df.ix[0,'near1_d']==df.ix[0,'far_d']):
        rollrt2=None
    else:
        rollrt2=365*(np.log(df.ix[0,'near1_p'])-np.log(df.ix[0,'far_p']))/(df.ix[0,'far_d']-df.ix[0,'near1_d']).days
    new_df.loc['haha','rollrt1']=rollrt1
    new_df.loc['haha', 'rollrt2'] = rollrt2
    return new_df

roll_rt=data.groupby(by=['underlying_symbol','date']).apply(cal_rollrt)
roll_rt.index=roll_rt.index.droplevel(level=2)
roll_rt=roll_rt.reset_index()
roll_rt['date']=roll_rt['date'].apply(lambda x:x.strftime(format='%Y-%m-%d'))

roll_rt.to_csv("roll_rt.csv",index=None)

####shift factor value
roll_rt=pd.read_csv("roll_rt.csv")
roll_rt=roll_rt.set_index(['date','underlying_symbol'])
roll_rt=roll_rt.groupby(level=1).apply(lambda x:x.shift(1))
roll_rt=roll_rt.reset_index()
roll_rt.to_csv("roll_rt.csv",index=None)

