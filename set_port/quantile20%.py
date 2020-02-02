import pandas as pd
import numpy as np

#除了时间序列动量和hp6-8以外都分五组
adjust_price=pd.read_csv("../adjust_price/adjust_price.csv")
adjust_price=adjust_price.set_index('date')
cat_list=pd.read_csv("../data_extraction/cat_list.csv",header=None)
cat_list=pd.Series(cat_list[0])
#新建一个数据框记录持仓信息
port=pd.DataFrame(index=adjust_price.index,columns=adjust_price.columns)
#读入筛选条件
check_vol=pd.read_csv("../check_vol/check_vol.csv")
check_vol=check_vol.set_index('date')
check_vol=check_vol[check_vol==1]

def set_port(df):
    df_return=pd.DataFrame(columns=df.columns,index=df.index)
    sr=pd.Series(data=df.iloc[0,:].dropna(),name=df.index.values[0])
    length=round(0.2*len(sr))
    long_port=sr.sort_values(ascending=False).head(length).index.values
    short_port=sr.sort_values(ascending=False).tail(length).index.values
    df_return.loc[sr.name,long_port]=1
    df_return.loc[sr.name,short_port]=-1
    return df_return


"""
#####cost of carry
#basis_mom
for R in range(10,121,10):
    fac=pd.read_csv("../cost_of_carry/basis_mom/basis_mom_R"+str(R)+".csv")
    for fac_num in [1,2]:
        fac_new=fac[['underlying_symbol','date','basis_mom'+str(fac_num)]]
        fac_new=fac_new.set_index(['underlying_symbol','date'])
        fac_new=fac_new.unstack(level=0)
        fac_new.columns=fac_new.columns.droplevel(level=0)
        fac_new=fac_new*check_vol
        port=fac_new.groupby(level=0).apply(set_port)
        port=port.reset_index()
        port.to_csv("basis_mom"+str(fac_num)+"R"+str(R)+"_port.csv",index=None)
#basis
fac=pd.read_csv("../cost_of_carry/basis/basis.csv")
for fac_num in [1,2]:
    fac_new = fac[['underlying_symbol', 'date', 'basis' + str(fac_num)]]
    fac_new = fac_new.set_index(['underlying_symbol', 'date'])
    fac_new = fac_new.unstack(level=0)
    fac_new.columns = fac_new.columns.droplevel(level=0)
    fac_new = fac_new * check_vol
    port = fac_new.groupby(level=0).apply(set_port)
    port = port.reset_index()
    port.to_csv("basis" + str(fac_num) + "_port.csv", index=None)

#roll_rt
fac=pd.read_csv("../cost_of_carry/roll_rt/roll_rt.csv")
for fac_num in [1,2]:
    fac_new=fac[['underlying_symbol','date','rollrt'+str(fac_num)]]
    fac_new = fac_new.set_index(['underlying_symbol', 'date'])
    fac_new = fac_new.unstack(level=0)
    fac_new.columns = fac_new.columns.droplevel(level=0)
    fac_new = fac_new * check_vol
    port = fac_new.groupby(level=0).apply(set_port)
    port = port.reset_index()
    port.to_csv("rollrt"+str(fac_num)+"_port.csv",index=None)

#warehouse
for R in range(10,101,10):
    fac = pd.read_csv("../cost_of_carry/warehouse/warehouse_fac_R"+str(R)+".csv")
    fac['date']=fac['date'].apply(lambda x:str(x))
    fac['date']=pd.to_datetime(fac['date'])
    fac['date']=fac['date'].apply(lambda x:x.strftime("%Y-%m-%d"))
    fac = fac.set_index('date')
    fac = fac * check_vol
    fac=fac*(-1)
    port = fac.groupby(level=0).apply(set_port)
    port = port.reset_index()
    port.to_csv("warehouse_R" + str(R) + "_port.csv", index=None)
#库存水平 inventory level
fac=pd.read_csv("../cost_of_carry/warehouse/inv_level.csv")
fac=fac.drop(columns=['Unnamed: 0'])
fac=fac.pivot(index='date',columns='underlying_symbol',values='inv_level')
fac=fac.reset_index()
fac['date']=fac['date'].apply(lambda x:str(x))
fac['date']=pd.to_datetime(fac['date'])
fac['date']=fac['date'].apply(lambda x:x.strftime("%Y-%m-%d"))
fac = fac.set_index('date')
fac = fac * check_vol
fac=fac*(-1)
port = fac.groupby(level=0).apply(set_port)
port = port.reset_index()
port.to_csv("inv_level_port.csv",index=None)
###risk_sorted
#cnybeta
for R in [1,2,3,4,5]:
    for typo in ['cnyr','cnyx']:
        fac = pd.read_csv("../risk_sorted/beta/CNY_beta/R"+str(R)+"_"+typo+".csv")
        fac = fac.set_index('date')
        # 新建一个数据框 把因子值记录到每日
        df_new = pd.DataFrame(index=adjust_price.index, columns=adjust_price.columns)
        df_new = df_new.reset_index()
        df_new['date'] = df_new['date'].apply(lambda x: x[0:7])
        df_new = df_new.set_index('date')
        for i in range(0, len(df_new)):
            for j in range(0, df_new.shape[1]):
                df_new.iat[i, j] = fac.at[df_new.index.values[i], df_new.columns.values[j]]
        df_new.index=adjust_price.index
        fac=df_new*check_vol
        port = fac.groupby(level=0).apply(set_port)
        port=(-1)*port
        port = port.reset_index()
        port.to_csv(typo+"_R"+str(R)+"_port.csv",index=None)

##inflation beta
for R in [1,2,3,4,5]:
    for typo in ['mom','yoy']:
        fac = pd.read_csv("../risk_sorted/beta/inflation_beta/R"+str(R)+"_"+typo+".csv")
        fac = fac.set_index('date')
        # 新建一个数据框 把因子值记录到每日
        df_new = pd.DataFrame(index=adjust_price.index, columns=adjust_price.columns)
        df_new = df_new.reset_index()
        df_new['date'] = df_new['date'].apply(lambda x: x[0:7])
        df_new = df_new.set_index('date')
        for i in range(0, len(df_new)):
            for j in range(0, df_new.shape[1]):
                df_new.iat[i, j] = fac.at[df_new.index.values[i], df_new.columns.values[j]]
        df_new.index=adjust_price.index
        fac=df_new*check_vol
        port = fac.groupby(level=0).apply(set_port)
        port = port.reset_index()
        port.to_csv(typo+"_R"+str(R)+"_port.csv",index=None)

#volatility 总波动率 36-120-250
for R in [36,120,250]:
    fac = pd.read_csv("../risk_sorted/volatility/cov"+str(R)+".csv")
    fac = fac.set_index('date')
    fac = fac * check_vol
    port = fac.groupby(level=0).apply(set_port)
    port = port.reset_index()
    port.to_csv("cov"+str(R)+"_port.csv", index=None)


#特质波动率 反向
for R in [120,250]:
    fac = pd.read_csv("../risk_sorted/volatility/idio_vol" + str(R) + ".csv")
    fac=fac.pivot(index='date',columns='underlying_symbol',values='resid')
    fac = fac * check_vol
    port = fac.groupby(level=0).apply(set_port)
    port=port*(-1)
    port = port.reset_index()
    port.to_csv("idio_vol" + str(R) + "_port.csv", index=None)



#
####supply and demand
#hp
for fac_num in [1,2,3,4,5]:
    fac=pd.read_csv("../supply_demand/hp/hp"+str(fac_num)+".csv")
    for R in [1,2,3,4,5,10,20]:
        for rank in [5,10,20]:
            fac_new=fac[['trading_date','underlying_symbol','R'+str(R)+'top'+str(rank)]]
            fac_new=fac_new.rename(columns={'trading_date':'date'})
            fac_new = fac_new.set_index(['underlying_symbol', 'date'])
            fac_new = fac_new.unstack(level=0)
            fac_new.columns = fac_new.columns.droplevel(level=0)
            fac_new = fac_new * check_vol
            port = fac_new.groupby(level=0).apply(set_port)
            port = port.reset_index()
            port.to_csv("hp"+str(fac_num)+"R"+str(R)+"top"+str(rank)+"_port.csv", index=None)

#liquid 负向的
for R in range(5,41,5):
    fac=pd.read_csv("../supply_demand/liquidity/liquidity_R"+str(R)+".csv")
    fac=fac.set_index('date')
    fac=fac*check_vol
    port = fac.groupby(level=0).apply(set_port)
    port = (-1) * port
    port = port.reset_index()
    port.to_csv("liquidity_R"+str(R)+"_port.csv",index=None)


#open interest
fac=pd.read_csv("../supply_demand/open_interest/open_interest_growth.csv")
for R in range(5,41,5):
    fac_new=fac[['date','underlying_symbol','growth'+str(R)]]
    fac_new = fac_new.rename(columns={'trading_date': 'date'})
    fac_new = fac_new.set_index(['underlying_symbol', 'date'])
    fac_new = fac_new.unstack(level=0)
    fac_new.columns = fac_new.columns.droplevel(level=0)
    fac_new = fac_new * check_vol
    port = fac_new.groupby(level=0).apply(set_port)
    port = port.reset_index()
    port.to_csv("open_interest_R"+str(R)+"_port.csv",index=None)


##technique
#mom
for R in range(5,41,5):
    fac=pd.read_csv("../technique/momentum/mom_R"+str(R)+".csv")
    fac=fac.set_index('date')
    fac = fac * check_vol
    port = fac.groupby(level=0).apply(set_port)
    port = port.reset_index()
    port.to_csv("cross_sec_mom_R"+str(R)+"_port.csv", index=None)
#skew
#做多负偏度的
fac=pd.read_csv("../technique/skew/skew.csv")
for R in range(20,181,20):
    fac_new = fac[['date', 'underlying_symbol', 'skew_' + str(R)]]
    fac_new = fac_new.rename(columns={'trading_date': 'date'})
    fac_new = fac_new.set_index(['underlying_symbol', 'date'])
    fac_new = fac_new.unstack(level=0)
    fac_new.columns = fac_new.columns.droplevel(level=0)
    fac_new = fac_new * check_vol
    fac_new=(-1)*fac_new
    port = fac_new.groupby(level=0).apply(set_port)
    port = port.reset_index()
    port.to_csv("skew_R" + str(R) + "_port.csv", index=None)
"""






