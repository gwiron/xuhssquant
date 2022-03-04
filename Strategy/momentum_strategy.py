import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Data.Stock as st
import pandas as pd
import numpy as np

# 获取沪深300股票池
def get_data(start_date, end_date, index_symbol = '000300.XSHG'):
    #获取股票列表代码(沪深300、创业板、上证)
    stocks =st.get_index_list(index_symbol=index_symbol)
    #拼接收盘价数据
    data_concat = pd.DataFrame()
    #获取股票数据
    for code in stocks[0:5]:
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
def momentum(data_concat, shift_N = 1, top_N=2):
    #转换时间频率：日转换为月
    data_month = data_concat.resample('M').last()
    #计算过去N个月的收益率 = 期末值/期初值 -1
    shift_return = data_month / data_month.shift(shift_N) -1

    #生成交易信号：收益率排前N的赢家组合-买入，收益率排后N的输家组合-卖出
    buy_signals = get_top_stocks(shift_return, top_N=top_N)
    sell_signals = get_top_stocks(shift_return*-1, top_N=top_N)
    # print(buy_signals)
    # print(sell_signals)
    signal = buy_signals - sell_signals
    print(signal)
    # print(data_month.head())
    # print(shift_return.head(10))
    return shift_return

#找到前N位的极大值，并转换为信号返回
def get_top_stocks(data, top_N):
    signals = pd.DataFrame(index=data.index, columns=data.columns)
    #对data的每一行进行遍历，找到里面的最大值，并利用Bool值去标注0或者1信号
    for index, row in data.iterrows():
        #print(row.isin(row.nlargest(top_N)).astype(np.int))
        signals.loc[index]=row.isin(row.nlargest(top_N)).astype(np.int)

    return signals

if __name__ == '__main__':
    # 测试获取沪深300 前9个个股数据
    data_concat = get_data('2020-01-01', '2021-04-01')
    # 测试 动量策略
    momentum(data_concat)