import pandas as pd
import numpy as np
import datetime as dt
import math
#输入H 文件名


def cal_riskrt(H,source):
    source=source.iloc[:,0:6]
    source=source.drop(columns=["Unnamed: 0"])
    source=source.set_index('date').dropna(subset=['long_rt','short_rt','long_short_rt'],how='all')

    #新建一个数据框记录各种指标
    df=pd.DataFrame(columns=['rt','volatility','mdd','sharpe','calmar'],index=['long','short','long_short','excess'])
    #计算多头各项指标
    rt=pd.DataFrame(source['long_rt'])
    rt['prod'] = np.cumprod(rt['long_rt'] + 1)
    holding_period = pd.to_datetime(rt.index.values[-1]) - pd.to_datetime(rt.index.values[0])
    # #年化收益率
    annual_ret = pow(rt['prod'][-1], 365 / holding_period.days) - 1
    # #年化波动率
    volatility = rt['long_rt'].std() * (math.sqrt(250 / H))
    # #sharpe
    sharpe = annual_ret / volatility
    # #计算最大回撤
    rt['max2here'] = rt['prod'].expanding(1).max()
    rt['dd2here'] = (rt['prod'] / rt['max2here']) - 1
    mdd = rt['dd2here'].min()
    calmar = annual_ret / abs(mdd)
    df.loc['long','rt']=annual_ret
    df.loc['long','volatility']=volatility
    df.loc['long','mdd']=mdd
    df.loc['long','sharpe']=sharpe
    df.loc['long','calmar']=calmar

    #计算空头组合的指标（对照组）
    rt = pd.DataFrame(source['short_rt'])
    rt['short_rt']=rt['short_rt']
    rt['prod'] = np.cumprod(rt['short_rt'] + 1)
    holding_period = pd.to_datetime(rt.index.values[-1]) - pd.to_datetime(rt.index.values[0])
    # #年化收益率
    annual_ret = pow(rt['prod'][-1], 365 / holding_period.days) - 1
    # #年化波动率
    volatility = rt['short_rt'].std() * (math.sqrt(250 / H))
    # #sharpe
    sharpe = annual_ret / volatility
    # #计算最大回撤
    rt['max2here'] = rt['prod'].expanding(1).max()
    rt['dd2here'] = (rt['prod'] / rt['max2here']) - 1
    mdd = rt['dd2here'].min()
    calmar = annual_ret / abs(mdd)
    df.loc['short', 'rt'] = annual_ret
    df.loc['short', 'volatility'] = volatility
    df.loc['short', 'mdd'] = mdd
    df.loc['short', 'sharpe'] = sharpe
    df.loc['short', 'calmar'] = calmar

    # 计算多空组合的指标
    rt = pd.DataFrame(source['long_short_rt'])
    rt['long_short_rt'] = rt['long_short_rt']
    rt['prod'] = np.cumprod(rt['long_short_rt'] + 1)
    holding_period = pd.to_datetime(rt.index.values[-1]) - pd.to_datetime(rt.index.values[0])
    # #年化收益率
    annual_ret = pow(rt['prod'][-1], 365 / holding_period.days) - 1
    # #年化波动率
    volatility = rt['long_short_rt'].std() * (math.sqrt(250 / H))
    # #sharpe
    sharpe = annual_ret / volatility
    # #计算最大回撤
    rt['max2here'] = rt['prod'].expanding(1).max()
    rt['dd2here'] = (rt['prod'] / rt['max2here']) - 1
    mdd = rt['dd2here'].min()
    calmar = annual_ret / abs(mdd)
    df.loc['long_short', 'rt'] = annual_ret
    df.loc['long_short', 'volatility'] = volatility
    df.loc['long_short', 'mdd'] = mdd
    df.loc['long_short', 'sharpe'] = sharpe
    df.loc['long_short', 'calmar'] = calmar


    # 计算超额收益的指标
    rt = pd.DataFrame(source['long_rt']-source['benchmark'])
    rt.columns=['excess_rt']
    rt['prod'] = np.cumprod(rt['excess_rt'] + 1)
    holding_period = pd.to_datetime(rt.index.values[-1]) - pd.to_datetime(rt.index.values[0])
    # #年化收益率
    annual_ret = pow(rt['prod'][-1], 365 / holding_period.days) - 1
    # #年化波动率
    volatility = rt['excess_rt'].std() * (math.sqrt(250 / H))
    # #sharpe
    sharpe = annual_ret / volatility
    # #计算最大回撤
    rt['max2here'] = rt['prod'].expanding(1).max()
    rt['dd2here'] = (rt['prod'] / rt['max2here']) - 1
    mdd = rt['dd2here'].min()
    calmar = annual_ret / abs(mdd)
    df.loc['excess', 'rt'] = annual_ret
    df.loc['excess', 'volatility'] = volatility
    df.loc['excess', 'mdd'] = mdd
    df.loc['excess', 'sharpe'] = sharpe
    df.loc['excess', 'calmar'] = calmar

    return df

rt_df=pd.read_csv("../draw/inv_level_H30.csv")
risk_rt=cal_riskrt(20,rt_df)
risk_rt.to_csv("inv_level.csv")

rt_df=pd.read_csv("../draw/warehouseR90H5.csv")
risk_rt=cal_riskrt(5,rt_df)
risk_rt.to_csv("warehouse.csv")

rt_df=pd.read_csv("../draw/rollrt2H35.csv")
risk_rt=cal_riskrt(35,rt_df)
risk_rt.to_csv("roll_rt.csv")

rt_df=pd.read_csv("../draw/basis2H35.csv")
risk_rt=cal_riskrt(35,rt_df)
risk_rt.to_csv("basis.csv")

rt_df=pd.read_csv("../draw/basis_mom2R120H35.csv")
risk_rt=cal_riskrt(35,rt_df)
risk_rt.to_csv("basis_mom.csv")

rt_df=pd.read_csv("../draw/open_interestR5H30.csv")
risk_rt=cal_riskrt(30,rt_df)
risk_rt.to_csv("open_interest.csv")

rt_df=pd.read_csv("../draw/ts_momR120H30.csv")
risk_rt=cal_riskrt(30,rt_df)
risk_rt.to_csv("ts_mom.csv")

rt_df=pd.read_csv("../draw/cs_momR5H30.csv")
risk_rt=cal_riskrt(30,rt_df)
risk_rt.to_csv("cs_mom.csv")

rt_df=pd.read_csv("../draw/skewR120H30.csv")
risk_rt=cal_riskrt(30,rt_df)
risk_rt.to_csv("skew.csv")

rt_df=pd.read_csv("../draw/liquidityR15H30.csv")
risk_rt=cal_riskrt(30,rt_df)
risk_rt.to_csv("liquidity.csv")

rt_df=pd.read_csv("../draw/covR120H30.csv")
risk_rt=cal_riskrt(30,rt_df)
risk_rt.to_csv("cov.csv")

rt_df=pd.read_csv("../draw/idio_volR200H25.csv")
risk_rt=cal_riskrt(25,rt_df)
risk_rt.to_csv("idio_vol.csv")

rt_df=pd.read_csv("../draw/momR5H40.csv")
risk_rt=cal_riskrt(40,rt_df)
risk_rt.to_csv("inflation.csv")

rt_df=pd.read_csv("../draw/cnyrR3H40.csv")
risk_rt=cal_riskrt(40,rt_df)
risk_rt.to_csv("cny.csv")