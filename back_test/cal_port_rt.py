#######calculate portfolio return series
import pandas as pd
import numpy as np
#读入收盘价
adjust_price=pd.read_csv("../adjust_price/adjust_price.csv")
adjust_price=adjust_price.set_index('date')

##########################建立函数##############################
def cal_rt(port_info,H):
    # get port info 保证传入的表无index
    port_info = port_info.set_index('date')
    port_info = port_info.dropna(how='all')
    # 将持仓信息 根据H切片
    port_info = port_info.iloc[range(0, len(port_info), H), :]
    # adjust_price pct_change
    pct_change = adjust_price.shift(-H) / adjust_price - 1

    #####计算组合收益率 扣费前
    # stack rt&port_info then get them merged to multiply
    rt_stack = pct_change.stack().reset_index()
    port_info_stack = port_info.stack().reset_index()
    rt_stack = rt_stack.rename(columns={'level_1': 'underlying_symbol', 0: 'rt'})
    port_info_stack = port_info_stack.rename(columns={'level_1': 'underlying_symbol', 0: 'port'})
    df_combined = port_info_stack.merge(rt_stack, on=['date', 'underlying_symbol'], how='left')

    # 多头收益
    long_rt = df_combined[df_combined['port'] == 1].groupby('date')['rt'].mean()
    # 空头收益
    short_rt =  df_combined[df_combined['port'] == -1].groupby('date')['rt'].mean()
    # 多空
    ###预处理 收益率变为相反数后取均值
    df_combined['rt1']=df_combined['rt']*df_combined['port']
    long_short_rt = df_combined.groupby('date')['rt1'].mean()

    #####计算换手率及费率
    # 多头
    port_long_fill = port_info[port_info == 1].fillna(0)
    turnover_long = (port_long_fill - port_long_fill.shift(1)).abs().sum(axis=1) / port_long_fill.sum(axis=1)
    cost_long = turnover_long * 0.0003
    # 空头
    port_short_fill = port_info[port_info == -1].fillna(0)
    turnover_short = (port_short_fill - port_short_fill.shift(1)).abs().sum(axis=1) / port_short_fill.abs().sum(axis=1)
    cost_short = turnover_short * 0.0003
    # 多空
    port_info_fill = port_info.fillna(0)
    turnover = (port_info_fill - port_info_fill.shift(1)).abs().sum(axis=1) / port_info_fill.abs().sum(axis=1)
    cost_long_short = turnover * 0.0003

    ######扣费
    long_rt = long_rt - cost_long
    short_rt = short_rt - cost_short
    long_short_rt = long_short_rt - cost_long_short

    #####合并并保存
    long_rt = pd.DataFrame(long_rt, columns=['long_rt'])
    short_rt = pd.DataFrame(short_rt, columns=['short_rt'])
    long_short_rt = pd.DataFrame(long_short_rt, columns=['long_short_rt'])
    rt = long_rt.join(short_rt)
    rt = rt.join(long_short_rt)
    rt=rt.reset_index()
    return rt




###cost of carry
#basis_mom
for fac_num in [1,2]:
    for R in range(10,121,10):
        for H in range(5,41,5):
            port_info=pd.read_csv("../set_port/basis_mom"+str(fac_num)+"R"+str(R)+"_port.csv")
            rt=cal_rt(port_info,H)
            rt.to_csv("basis_mom"+str(fac_num)+"R"+str(R)+"H"+str(H)+".csv",index=None)
#basis
for fac_num in [1,2]:
    for H in range(5,41,5):
        port_info = pd.read_csv("../set_port/basis" + str(fac_num) +  "_port.csv")
        rt = cal_rt(port_info, H)
        rt.to_csv("basis" + str(fac_num) +"H"+str(H)+".csv", index=None)

#rollrt
for fac_num in [1,2]:
    for H in range(5,41,5):
        port_info=pd.read_csv("../set_port/rollrt"+str(fac_num)+"_port.csv")
        rt = cal_rt(port_info,H)
        rt.to_csv("rollrt"+str(fac_num)+"H"+str(H)+".csv",index=None)

#warehouse 库存变化率
for R in range(10,101,10):
    for H in range(5,41,5):
        port_info = pd.read_csv("../set_port/warehouse_R"+str(R)+"_port.csv")
        rt = cal_rt( port_info,H)
        rt.to_csv("warehouseR"+str(R)+"H"+str(H)+".csv", index=None)
#inv level
for H in range(5,41,5):
    port_info=pd.read_csv("../set_port/inv_level_port.csv")
    rt = cal_rt(port_info, H)
    rt.to_csv("inv_level_H"  + str(H) + ".csv", index=None)


#beta
for typo in ['cnyr','cnyx','mom','yoy']:
    for R in [1,2,3,4,5]:
        for H in [40,50,60,80,100,120]:
            port_info=pd.read_csv("../set_port/"+typo+"_R"+str(R)+"_port.csv")
            rt=cal_rt(port_info,H)
            rt.to_csv(typo+"R"+str(R)+"H"+str(H)+".csv",index=None)

#volatility
for H in range(5,41,5):
    for R in [36,120,250]:
        port_info = pd.read_csv("../set_port/cov"+str(R)+"_port.csv")
        rt = cal_rt(port_info,H)
        rt.to_csv("covR"+str(R) +"H" +str(H) + ".csv", index=None)
#idiosyncratic volatility
for R in [120,150,200,250]:
    for H in range(5,41,5):
        port_info=pd.read_csv("../set_port/idio_vol"+str(R)+"_port.csv")
        rt=cal_rt(port_info,H)
        rt.to_csv("idio_vol"+str(R)+"H"+str(H)+".csv",index=None)
"""        
###supply and demand
#hp
for fac_num in range(1,9):
    for rank in [5,10,20]:
        for R in [1,2,3,4,5,10,20]:
            for H in [1,2,3,4,5,10,15,20]:
                port_info=pd.read_csv("../set_port/hp"+str(fac_num)+"R"+str(R)+"top"+str(rank)+"_port.csv")
                port_info=port_info.set_index('date')
                rt = cal_rt(H, port_info)
                rt.to_csv("hp"+str(fac_num)+"R"+str(R)+"top"+str(rank)+"H"+str(H)+".csv",index=None)
"""
#liquidity
for R in range(5,41,5):
    for H in range(5,41,5):
        port_info=pd.read_csv("../set_port/liquidity_R"+str(R)+"_port.csv")
        rt=cal_rt(port_info,H)
        rt.to_csv("liquidityR"+str(R)+"H"+str(H)+".csv",index=None)
#open interest
for R in range(5,41,5):
    for H in range(5,41,5):
        port_info=pd.read_csv("../set_port/open_interest_R"+str(R)+"_port.csv")
        rt=cal_rt(port_info,H)
        rt.to_csv("open_interestR"+str(R)+"H"+str(H)+".csv",index=None)

###technique
#横截面动量 cross sec mom
for R in [5,10,15,20,25,30,35,40,100,120,250]:
    for H in range(5,41,5):
        port_info=pd.read_csv("../set_port/cross_sec_mom_R"+str(R)+"_port.csv")
        rt=cal_rt(port_info,H)
        rt.to_csv("cs_momR"+str(R)+"H"+str(H)+".csv",index=None)

#时间序列动量 ts mom
for R in [5,10,15,20,25,30,35,40,100,120,250]:
    for H in range(5,41,5):
        port_info=pd.read_csv("../set_port/ts_mom_R"+str(R)+"_port.csv")
        rt=cal_rt(port_info,H)
        rt.to_csv("ts_momR"+str(R)+"H"+str(H)+".csv",index=None)
#skew
for R in range(20,181,20):
    for H in range(5,41,5):
        port_info=pd.read_csv("../set_port/skew_R"+str(R)+"_port.csv")
        rt = cal_rt(port_info,H)
        rt.to_csv("skewR" + str(R) + "H" + str(H) + ".csv", index=None)


