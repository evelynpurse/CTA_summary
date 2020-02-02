import pandas as pd
import numpy as np
import statsmodels.api as sm

inflat=pd.read_csv("../../../data_extraction/inflation.csv")
inflat=inflat.set_index('date')

future_price=pd.read_csv("../../../adjust_price/adjust_price.csv")
future_price=future_price.set_index('date')
cat_list=pd.read_csv("../../../data_extraction/cat_list.csv",header=None)
cat_list=pd.Series(cat_list.groupby(cat_list.iloc[:,0]).count().index)
future_price.index=pd.to_datetime(future_price.index)
future_price.index=future_price.index.strftime("%Y-%m")
month_range=pd.Series(future_price.index.drop_duplicates().values)

#新建一个数据框 记录月度收益率
df_monrt=pd.DataFrame(index=month_range)
for i in range(0,len(cat_list)):
    price=future_price.iloc[:,i]
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

combined=df_monrt.join(inflat)
combined['yoy']=combined['yoy'].apply(lambda x:x*0.01)
combined['mom']=combined['mom'].apply(lambda x:x*0.01)

def cal_beta(R,typo):
    #新建一个数据框记录beta值
    df_beta=pd.DataFrame(index=df_monrt.index)
    if(typo=='yoy'):
        type_col=51
    else:
        type_col=52
    for i in range(0,len(cat_list)):
        ####此处可以调整 是否需要滞后
        for j in range(R,len(combined)):
            if(len(combined.iloc[j-R:j,[i,type_col]].dropna())==R):
                y=combined.iloc[j-R:j,i].values
                x=combined.iloc[j-R:j,type_col].values
                X=sm.add_constant(x)
                #建立模型
                model=sm.OLS(y,X)
                results=model.fit()
                #取得beta
                df_beta.loc[month_range[j],cat_list[i]]=results.params[1]
            else:
                df_beta.loc[month_range[j], cat_list[i]]=None
    df_beta=df_beta.reset_index()
    df_beta=df_beta.rename(columns={'index':'date'})
    return df_beta


cal_beta(12,'yoy').to_csv("R1_yoy.csv",index=None)
cal_beta(24,'yoy').to_csv("R2_yoy.csv",index=None)
cal_beta(36,'yoy').to_csv("R3_yoy.csv",index=None)
cal_beta(48,'yoy').to_csv("R4_yoy.csv",index=None)
cal_beta(60,'yoy').to_csv("R5_yoy.csv",index=None)

cal_beta(12,'mom').to_csv("R1_mom.csv",index=None)
cal_beta(24,'mom').to_csv("R2_mom.csv",index=None)
cal_beta(36,'mom').to_csv("R3_mom.csv",index=None)
cal_beta(48,'mom').to_csv("R4_mom.csv",index=None)
cal_beta(60,'mom').to_csv("R5_mom.csv",index=None)