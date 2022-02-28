import sys,os

from numpy.lib.index_tricks import AxisConcatenator
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Strategy.Base as strat
import Data.Stock as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 双均线策略
def ma_strategy(data, short_window=5, long_window=20):
    #计算技术指标：ma短期、ma长期
    data['short_ma'] = pd.DataFrame(data['close']).rolling(window=short_window).mean()
    data['long_ma'] = pd.DataFrame(data['close']).rolling(window=long_window).mean()
    #生成信号：金叉买入、死叉卖出
    data['buy_signal'] = np.where(data['short_ma']>data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma']<data['long_ma'], -1, 0)
    # print(data)
    #过滤信号：st.compose_signal
    data = strat.compose_signal(data=data)
    # #删除多余的columns
    data = data.drop(labels=['buy_signal', 'sell_signal'], axis = 1)
    # print(data)
    return data

if __name__ == '__main__':
    data = st.get_single_price(stock_code ='000001.XSHE', timefrequency='daily', start_date='2020-01-01', end_date='2021-04-01')
    data = ma_strategy(data)
    #筛选有信号点的数据
    data = data[data['signal']!=0]
    #预览数据
    # print("开仓次数：", int(len(data)/2))
    print(data)