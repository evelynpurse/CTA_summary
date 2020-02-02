import numpy as np
import pandas as pd
import rqdatac as rq
rq.init()

startdate=pd.to_datetime('20100104')
enddate=pd.to_datetime('20190329')

#get all contracts
future_info=pd.read_csv("future_info.csv")
id=future_info.groupby('order_book_id').count().index.values.tolist()

future_price=rq.get_price(id,start_date=startdate,end_date=enddate,frequency='1d',adjust_type='none')
future_price=future_price.to_frame()
future_price=future_price.reset_index()
future_price=future_price.rename(columns={'minor':'order_book_id'})

#future_price.to_csv("future_price.csv",index=None)