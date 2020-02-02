import numpy as np
import pandas as pd
import rqdatac as rq
rq.init()

#backtest period
startdate=pd.to_datetime('20100104')
enddate=pd.to_datetime('20190329')


future_info=rq.all_instruments(type='Future')

#####exclude ineffective contracts#######
#exclude index
future_info=future_info[~future_info['listed_date'].isin(['0000-00-00'])]
#keep contracts valid in the backtesting period
future_info=future_info[future_info.maturity_date>str(startdate)]
future_info=future_info[future_info.listed_date<str(enddate)]
#exclude financial futures and GN RS
future_info=future_info[future_info['underlying_symbol']!='T']
future_info=future_info[future_info['underlying_symbol']!='TF']
future_info=future_info[future_info['underlying_symbol']!='TS']
future_info=future_info[future_info['underlying_symbol']!='IC']
future_info=future_info[future_info['underlying_symbol']!='IF']
future_info=future_info[future_info['underlying_symbol']!='IH']
future_info=future_info[future_info['underlying_symbol']!='GN']
future_info=future_info[future_info['underlying_symbol']!='RS']

####modifying underlying symbol
future_info['underlying_symbol'][future_info['underlying_symbol']=='TC']='ZC'
future_info['underlying_symbol'][future_info['underlying_symbol']=='ME']='MA'
future_info['underlying_symbol'][future_info['underlying_symbol']=='ER']='RI'
future_info['underlying_symbol'][future_info['underlying_symbol']=='RO']='OI'
future_info['underlying_symbol'][future_info['underlying_symbol']=='WH']='WS'

#####get all future varieties######
cat_list=future_info.groupby('underlying_symbol').count().index.values
cat_list=pd.Series(cat_list)

cat_list.to_csv("cat_list.csv",index=None)
future_info.to_csv("future_info.csv",index=None)