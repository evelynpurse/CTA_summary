import pandas as pd
import numpy as np
import statsmodels.api as sm

#coefficient of variation=variance/mean return 方差（标准差）/均值的绝对值 买入高vol品种

##计算coefficient of variation
price=pd.read_csv("../../adjust_price/adjust_price.csv")
price=price.set_index('date')
price=price/price.shift(1)-1
for ranking_period in [36,120,250]:
    var = price.rolling(ranking_period, min_periods=ranking_period).var()
    mean = price.rolling(ranking_period, min_periods=ranking_period).mean()
    cov = var / mean
    cov = cov.reset_index()
    cov.to_csv("cov"+str(ranking_period)+".csv", index=None)

