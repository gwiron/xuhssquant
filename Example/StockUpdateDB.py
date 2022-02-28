import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Data.Stock as st

code = '000001.XSHE'
#先获取初始数据用于验证
# data = st.get_single_price(stock_code=code, timefrequency='daily', start_date='2021-01-01', end_date='2021-02-01')
# #存入csv中
# st.export_data(data=data, filename=code, type='Price')

# 获取数据
# st.update_daily_price(code, 'Price')

st.update_price_db()