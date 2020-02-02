import pandas as pd
import numpy as np



def cal_long(source):
    rt=pd.DataFrame(source['long_short_rt'].dropna())
    rt['prod'] = np.cumprod(rt['long_short_rt'] + 1)
    holding_period = pd.to_datetime(rt.index.values[-1]) - pd.to_datetime(rt.index.values[0])
    #年化收益率
    annual_ret = pow(rt['prod'][-1], 365 / holding_period.days) - 1
    return ("%.2f%%")%(annual_ret*100)

###cost of carry
#basis_mom
for fac_num in [1,2]:
    df=pd.DataFrame(index=range(10,121,10),columns=range(5,41,5))
    for R in range(10,121,10):
        for H in range(5,41,5):
            rt=pd.read_csv("../../basis_mom"+str(fac_num)+"R"+str(R)+"H"+str(H)+".csv")
            rt=rt.set_index('date')
            df.loc[R,H]=cal_long(rt)
    df.to_csv("basis_mom"+str(fac_num)+".csv")

#rollrt
df_rollrt=pd.DataFrame(index=['roll_rt1','roll_rt2'],columns=range(5,41,5))
for fac_num in [1,2]:
    for H in range(5,41,5):
        rt=pd.read_csv("../../rollrt"+str(fac_num)+"H"+str(H)+".csv")
        rt=rt.set_index('date')
        df_rollrt.loc["roll_rt"+str(fac_num),H] = cal_long(rt)
df_rollrt.to_csv("rollrt.csv")
#basis
df_basis=pd.DataFrame(index=['basis1','basis2'],columns=range(5,41,5))
for fac_num in [1,2]:
    for H in range(5,41,5):
        rt=pd.read_csv("../../basis"+str(fac_num)+"H"+str(H)+".csv")
        rt=rt.set_index('date')
        df_basis.loc["basis"+str(fac_num),H]=cal_long(rt)
df_basis.to_csv("basis.csv")
#warehouse
df=pd.DataFrame(index=range(10,101,10),columns=range(5,41,5))
for R in range(10,101,10):
    for H in range(5,41,5):
        rt = pd.read_csv("../../warehouseR"+str(R)+"H"+str(H)+".csv")
        rt = rt.set_index('date')
        df.loc[R,H] = cal_long(rt)
df.to_csv("warehouse.csv")
#inv level
df=pd.DataFrame(index=['inv_level'],columns=range(5,41,5))
for H in range(5,41,5):
    rt = pd.read_csv("../../inv_level_H" + str(H) + ".csv")
    rt = rt.set_index('date')
    df.loc['inv_level', H] = cal_long(rt)
df.to_csv("inv_level.csv")
#beta
for typo in ['cnyr','cnyx','mom','yoy']:
    df=pd.DataFrame(index=[1,2,3,4,5],columns=[40,50,60,80,100,120])
    for R in [1,2,3,4,5]:
        for H in [40,50,60,80,100,120]:
            rt=pd.read_csv("../../"+typo+"R"+str(R)+"H"+str(H)+".csv")
            rt=rt.set_index('date')
            df.loc[R,H]=cal_long(rt)
    df.to_csv(typo+".csv")

#volatility
df=pd.DataFrame(columns=range(5,41,5),index=[36,120,250])
for R in [36,120,250]:
    for H in range(5, 41, 5):
        rt = pd.read_csv("../../covR" + str(R) + "H" + str(H) + ".csv")
        rt = rt.set_index('date')
        df.loc[R, H] = cal_long(rt)
df.to_csv("cov.csv")
#idio volatility
df=pd.DataFrame(columns=range(5,41,5),index=[120,150,200,250])
for R in [120,150,200,250]:
    for H in range(5, 41, 5):
        rt = pd.read_csv("../../idio_vol" + str(R) + "H" + str(H) + ".csv")
        rt = rt.set_index('date')
        df.loc[R, H] = cal_long(rt)
df.to_csv("idio_vol.csv")
"""
###supply and demand
#hp
for fac_num in range(1,9):
    for rank in [5,10,20]:
        df=pd.DataFrame(index= [1,2,3,4,5,10,20],columns=[1,2,3,4,5,10,15,20] )
        for R in [1,2,3,4,5,10,20]:
            for H in [1,2,3,4,5,10,15,20]:
                rt=pd.read_csv("../hp"+str(fac_num)+"R"+str(R)+"top"+str(rank)+"H"+str(H)+".csv")
                rt=rt.set_index('date')
                df.loc[R,H] = cal_long(rt)
        df.to_csv("hp"+str(fac_num)+"top"+str(rank)+".csv")
"""

#liquidity
df=pd.DataFrame(index=range(5,41,5),columns=range(5,41,5))
for R in range(5,41,5):
    for H in range(5,41,5):
        rt=pd.read_csv("../../liquidityR"+str(R)+"H"+str(H)+".csv")
        rt=rt.set_index('date')
        df.loc[R,H]=cal_long(rt)
df.to_csv("liquidity.csv")


#open interest
df=pd.DataFrame(index=range(5,41,5),columns=range(5,41,5))
for R in range(5,41,5):
    for H in range(5,41,5):
        rt=pd.read_csv("../../open_interestR"+str(R)+"H"+str(H)+".csv")
        rt=rt.set_index('date')
        df.loc[R,H]=cal_long(rt)
df.to_csv("open_interest.csv")

###technique
#横截面动量 cross sec mom
df=pd.DataFrame(index=[5,10,15,20,25,30,35,40,100,120,250],columns=range(5,41,5))
for R in [5,10,15,20,25,30,35,40,100,120,250]:
    for H in range(5,41,5):
        rt=pd.read_csv("../../cs_momR"+str(R)+"H"+str(H)+".csv")
        rt=rt.set_index('date')
        df.loc[R,H]=cal_long(rt)
df.to_csv("cs_mom.csv")

#时间序列动量 ts mom
df=pd.DataFrame(index=[5,10,15,20,25,30,35,40,100,120,250],columns=range(5,41,5))
for R in [5,10,15,20,25,30,35,40,100,120,250]:
    for H in range(5,41,5):
        rt = pd.read_csv("../../ts_momR" + str(R) + "H" + str(H) + ".csv")
        rt = rt.set_index('date')
        df.loc[R, H] = cal_long(rt)
df.to_csv("ts_mom.csv")

#skew
df=pd.DataFrame(index=range(20,181,20),columns=range(5,41,5))
for R in range(20,181,20):
    for H in range(5,41,5):
        rt=pd.read_csv("../../skewR"+str(R)+"H"+str(H)+".csv")
        rt = rt.set_index('date')
        df.loc[R,H] = cal_long(rt)
df.to_csv("skew.csv")
