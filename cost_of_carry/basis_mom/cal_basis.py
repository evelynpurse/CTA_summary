####calculate basis momentum
import pandas as pd
import numpy as np

data=pd.read_csv("../roll_rt/ts_price_date.csv")

data=data[['underlying_symbol','date','near1_p','near2_p','far_p']]

def cal_basis(df,R):
    #front, second front contract
    df['basis_mom1']=((df['near1_p']/df['near1_p'].shift(R))-(df['near2_p']/df['near2_p'].shift(R))).shift(1)
    
    #front, far contract
    df['basis_mom2'] = ((df['near1_p'] / df['near1_p'].shift(R))-(df['far_p']/df['far_p'].shift(R))).shift(1)

    df=df[['underlying_symbol','date','basis_mom1','basis_mom2']]
    return df
for R in range(10,121,10):
    fac=data.groupby('underlying_symbol').apply(cal_basis,R)
    fac.to_csv("basis_mom_R"+str(R)+".csv",index=None)