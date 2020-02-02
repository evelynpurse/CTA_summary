import pandas as pd
import numpy as np

#读入会员持仓数据
long_count=pd.read_csv("long_count.csv",index_col=0)
short_count=pd.read_csv("short_count.csv",index_col=0)
long_count=long_count.set_index(['trading_date','underlying_symbol'])
short_count=short_count.set_index(['trading_date','underlying_symbol'])
#将两张表拼接起来
df_count=long_count.join(short_count,how='outer',rsuffix='short')
##持仓变化率类
#hp1净多头持仓量变化率
#建立函数 计算净多头持仓量变化率
def cal_hp1(df):
    #新建一个数据框用于返回
    df_return=pd.DataFrame(index=df.index)
    for R in [1,2,3,4,5,10,20]:
        for rank in [5,10,20]:
            print(str(R)+str(rank))
            single=(df['top'+str(rank)]-df['top'+str(rank)+'short'])/(df['top'+str(rank)]-df['top'+str(rank)+'short']).shift(R)-1
            single=pd.DataFrame(single)
            single.columns=['R'+str(R)+'top'+str(rank)]
            df_return=df_return.join(single)
    df_return=df_return.shift(1)
    return df_return

hp1=df_count.groupby(level=1).apply(cal_hp1)
#hp2多头持仓量变化率
def cal_hp2(df):
    df_return=pd.DataFrame(index=df.index)
    for R in [1,2,3,4,5,10,20]:
        for rank in [5,10,20]:
            single=df['top'+str(rank)]/df['top'+str(rank)].shift(R)-1
            single=pd.DataFrame(single)
            single.columns=['R'+str(R)+'top'+str(rank)]
            df_return=df_return.join(single)
    df_return = df_return.shift(1)
    return df_return

hp2=df_count.groupby(level=1).apply(cal_hp2)
#hp3 空头持仓量变化率
def cal_hp3(df):
    df_return=pd.DataFrame(index=df.index)
    for R in [1,2,3,4,5,10,20]:
        for rank in [5,10,20]:
            single=1-df['top'+str(rank)+'short']/df['top'+str(rank)+'short'].shift(R)
            single=pd.DataFrame(single)
            single.columns=['R'+str(R)+'top'+str(rank)]
            df_return=df_return.join(single)
    df_return = df_return.shift(1)
    return df_return
hp3=df_count.groupby(level=1).apply(cal_hp3)
##持仓占比变化类
#hp4 多仓占比变化
def cal_hp4(df):
    df_return = pd.DataFrame(index=df.index)
    for R in [1, 2, 3, 4, 5, 10, 20]:
        for rank in [5, 10, 20]:
            single =(df['top'+str(rank)]/(df['top'+str(rank)]+df['top'+str(rank)+'short']))-(df['top'+str(rank)]/(df['top'+str(rank)]+df['top'+str(rank)+'short'])).shift(R)
            single = pd.DataFrame(single)
            single.columns = ['R' + str(R) + 'top' + str(rank)]
            df_return = df_return.join(single)
    df_return = df_return.shift(1)
    return df_return
hp4=df_count.groupby(level=1).apply(cal_hp4)
#hp5 空仓占比变化
def cal_hp5(df):
    df_return = pd.DataFrame(index=df.index)
    for R in [1, 2, 3, 4, 5, 10, 20]:
        for rank in [5, 10, 20]:
            single =((df['top'+str(rank)+'short']/(df['top'+str(rank)]+df['top'+str(rank)+'short']))-(df['top'+str(rank)+'short']/(df['top'+str(rank)]+df['top'+str(rank)+'short'])).shift(R))*(-1)
            single = pd.DataFrame(single)
            single.columns = ['R' + str(R) + 'top' + str(rank)]
            df_return = df_return.join(single)
    df_return = df_return.shift(1)
    return df_return
hp5=df_count.groupby(level=1).apply(cal_hp5)
##持仓变化方向类 不能分层 全部买入。。。。
#hp6多头与空头持仓变化方向
def cal_hp6(df):
    df_return = pd.DataFrame(index=df.index)
    for R in [1, 2, 3, 4, 5, 10, 20]:
        for rank in [5, 10, 20]:
            single =np.sign(df['top'+str(rank)]/df['top'+str(rank)].shift(R)-1)+np.sign(1-df['top'+str(rank)+'short']/df['top'+str(rank)+'short'].shift(R))
            single = pd.DataFrame(single)
            single.columns = ['R' + str(R) + 'top' + str(rank)]
            df_return = df_return.join(single)
    df_return = df_return.shift(1)
    return df_return
hp6=df_count.groupby(level=1).apply(cal_hp6)
#hp7多头持仓变化方向
def cal_hp7(df):
    df_return = pd.DataFrame(index=df.index)
    for R in [1, 2, 3, 4, 5, 10, 20]:
        for rank in [5, 10, 20]:
            single =np.sign(df['top'+str(rank)]/df['top'+str(rank)].shift(R)-1)
            single = pd.DataFrame(single)
            single.columns = ['R' + str(R) + 'top' + str(rank)]
            df_return = df_return.join(single)
    df_return = df_return.shift(1)
    return df_return
hp7=df_count.groupby(level=1).apply(cal_hp7)
#hp8空头持仓变化方向
def cal_hp8(df):
    df_return = pd.DataFrame(index=df.index)
    for R in [1, 2, 3, 4, 5, 10, 20]:
        for rank in [5, 10, 20]:
            single =np.sign(1-df['top'+str(rank)+'short']/df['top'+str(rank)+'short'].shift(R))
            single = pd.DataFrame(single)
            single.columns = ['R' + str(R) + 'top' + str(rank)]
            df_return = df_return.join(single)
    df_return = df_return.shift(1)
    return df_return
hp8=df_count.groupby(level=1).apply(cal_hp8)

hp1.reset_index().to_csv("hp1.csv",index=None)
hp2.reset_index().to_csv("hp2.csv",index=None)
hp3.reset_index().to_csv("hp3.csv",index=None)
hp4.reset_index().to_csv("hp4.csv",index=None)
hp5.reset_index().to_csv("hp5.csv",index=None)
hp6.reset_index().to_csv("hp6.csv",index=None)
hp7.reset_index().to_csv("hp7.csv",index=None)
hp8.reset_index().to_csv("hp8.csv",index=None)