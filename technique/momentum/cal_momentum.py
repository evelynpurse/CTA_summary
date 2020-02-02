import pandas as pd
import numpy as np

price=pd.read_csv("../../adjust_price/adjust_price.csv")
price=price.set_index('date')
for R in range(5,41,5):
    mom=(price/price.shift(R)-1).shift(1)
    mom=mom.reset_index()
    mom.to_csv("mom_R"+str(R)+".csv",index=None)
#再测一下长期动量
for R in [100,120,250]:
    mom=(price/price.shift(R)-1).shift(1)
    mom=mom.reset_index()
    mom.to_csv("mom_R"+str(R)+".csv",index=None)