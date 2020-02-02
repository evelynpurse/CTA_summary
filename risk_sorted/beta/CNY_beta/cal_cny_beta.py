import pandas as pd
import numpy as np
import statsmodels.api as sm
#读入数据
cnyr=pd.read_csv("../../../data_extraction/cnyr.csv")
cnyx=pd.read_csv("../../../data_extraction/cnyx.csv")

future_price=pd.read_csv("../../../adjust_price/adjust_price.csv")
future_price=future_price.set_index('date')
cnyr=cnyr.set_index('date')
cnyx=cnyx.set_index('date')

cat_list=pd.read_csv("../../../data_extraction/cat_list.csv",header=None)
cat_list=pd.Series(cat_list.groupby(cat_list.iloc[:,0]).count().index)
###将两个数据框合并
combined=future_price.join(cnyr,rsuffix='cnyr')
combined=combined.join(cnyx,rsuffix='cnyx')
#计算月度变化率
combined.index=pd.to_datetime(combined.index)
#把日期处理成年月形式
combined.index=combined.index.strftime("%Y-%m")
month_range=pd.Series(combined.index.drop_duplicates().values)

#新建一个数据框 记录月度收益率
df_monrt=pd.DataFrame(index=month_range)
#列循环
for i in range(0,len(cat_list)):
    price=combined.iloc[:,i]
    if(len(price[month_range[0]].dropna())>1):
        single_month= pd.Series(price[month_range[0]].dropna().values)
        df_monrt.loc[month_range[0],cat_list[i]]=single_month[len(single_month)-1]/single_month[0]-1
    for j in range(1,len(month_range)):
        sr1=pd.Series( price[month_range[j-1]].dropna().values)
        sr2=pd.Series( price[month_range[j]].dropna().values)
        if((len(sr1)+len(sr2))>=2):
            if(len(sr1)==0):
                df_monrt.loc[month_range[j],cat_list[i]]=sr2[len(sr2)-1]/sr2[0]-1
            elif(len(sr2)==0):
                df_monrt.loc[month_range[j], cat_list[i]]=None
            else:
                df_monrt.loc[month_range[j],cat_list[i]]=sr2[len(sr2)-1]/sr1[len(sr1)-1]-1
#计算cnyr cnyx 的月度变化率
for col in ['close','closecnyx']:
    sr=combined.loc[:,col]
    for j in range(1,len(month_range)):
        sr1=pd.Series( sr[month_range[j-1]].dropna().values)
        sr2=pd.Series( sr[month_range[j]].dropna().values)
        if((len(sr1)+len(sr2))>=2):
            if(len(sr1)==0):
                df_monrt.loc[month_range[j],col]=sr2[len(sr2)-1]/sr2[0]-1
            elif(len(sr2)==0):
                df_monrt.loc[month_range[j], col]=None
            else:
                df_monrt.loc[month_range[j],col]=sr2[len(sr2)-1]/sr1[len(sr1)-1]-1
df_monrt=df_monrt.reset_index()
df_monrt=df_monrt.rename(columns={'index':'date','close':'cnyr','closecnyx':'cnyx'})
df_monrt.to_csv('monthly_change.csv')

df_monrt=df_monrt.set_index('date')
def cal_beta(R,typo):
    #新建一个数据框记录beta值
    df_beta=pd.DataFrame(index=df_monrt.index)
    if(typo=='cnyr'):
        type_col=51
    else:
        type_col=52
    for i in range(0,len(cat_list)):
        ####此处可以调整 是否需要滞后
        for j in range(R,len(df_monrt)):
            if(len(df_monrt.iloc[j-R:j,[i,type_col]].dropna())==R):
                y=df_monrt.iloc[j-R:j,i].values
                x=df_monrt.iloc[j-R:j,type_col].values
                X=sm.add_constant(x)
                #建立模型
                model=sm.OLS(y,X)
                results=model.fit()
                #取得beta
                df_beta.loc[month_range[j],cat_list[i]]=results.params[1]
            else:
                df_beta.loc[month_range[j],cat_list[i]]=None
    df_beta=df_beta.reset_index()
    return df_beta

cal_beta(12,'cnyr').to_csv("R1_cnyr.csv",index=None)
cal_beta(24,'cnyr').to_csv("R2_cnyr.csv",index=None)
cal_beta(36,'cnyr').to_csv("R3_cnyr.csv",index=None)
cal_beta(48,'cnyr').to_csv("R4_cnyr.csv",index=None)
cal_beta(60,'cnyr').to_csv("R5_cnyr.csv",index=None)

cal_beta(12,'cnyx').to_csv("R1_cnyx.csv",index=None)
cal_beta(24,'cnyx').to_csv("R2_cnyx.csv",index=None)
cal_beta(36,'cnyx').to_csv("R3_cnyx.csv",index=None)
cal_beta(48,'cnyx').to_csv("R4_cnyx.csv",index=None)
cal_beta(60,'cnyx').to_csv("R5_cnyx.csv",index=None)

