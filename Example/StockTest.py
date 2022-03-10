# import sys,os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)

# import Data.Stock as st

# code = '000001.XSHE'

# #调用一直股票的行情数据
# # data = st.get_single_price(stock_code=code, timefrequency='daily', start_date='2021-02-01', end_date='2021-03-03')

# # #存入csv中
# # st.export_data(data=data, filename='000001.XSHE', type='Price')
# # print(data)

# # # 从csv中读取数据
# # data = st.get_csv_data(code, 'Price')
# # data = data.set_index(keys=['date'])
# # print(data)

# #获取平安银行行情数据（日K）
# data = st.get_single_price(stock_code='000001.XSHE', timefrequency='daily', start_date='2021-02-01', end_date='2021-03-01')
# print(data)

# #计算涨跌幅 验证准确性
# data =  st.calculate_change_pct(data)
# print(data) #多了一列


URL=f'http://web.ifzq.gtimg.cn'
print(URL)