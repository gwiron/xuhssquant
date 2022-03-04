import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Data.Stock as st
import pandas as pd

# 获取沪深300股票池
def get_data(start_date, end_date, index_symbol = '000300.XSHG'):
    #获取股票列表代码(沪深300、创业板、上证)
    stocks =st.get_index_list(index_symbol=index_symbol)
    #拼接收盘价数据
    data_concat = pd.DataFrame()
    #获取股票数据
    for code in stocks[0:9]:
        data = st.get_single_price(code, 'daily', start_date=start_date, end_date=end_date)
        #取出收盘价这一列
        res = pd.DataFrame(data,columns=['close'])
        #修改收盘价这一列的名称为股票代码
        res.columns = [code]
        #拼接多个股票的收盘价（日期、股票A收盘价、股票B收盘价）
        data_concat = pd.concat([data_concat, res],axis = 1)

    #预览股票数据
    return data_concat

# 动量策略
def momentum(data_concat, shift_N = 1):
    #转换时间频率：日转换为月
    data_month = data_concat.resample('M').last()
    print(data_month.head())
    #计算过去N个月的收益率 = 期末值/期初值 -1
    shift_return = data_month / data_month.shift(shift_N) -1
    print(shift_return.head())
    return shift_return

if __name__ == '__main__':
    # 测试获取沪深300 前9个个股数据
    data_concat = get_data('2020-01-01', '2021-04-01')
    # 测试 动量策略
    momentum(data_concat)