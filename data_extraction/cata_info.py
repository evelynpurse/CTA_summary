#####统计商品期货品种及上市日期
import pandas as pd
import numpy as np
futures_info=pd.read_csv("future_info.csv")
futures_info.to_excel("future_info.xls",encoding='utf-8')