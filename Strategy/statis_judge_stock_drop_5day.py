# ——————————
# 对前5日均是跌的股票，进行后一天盯盘买入 1% or 1% 则卖出，若不满足条件则后延1天，第五天未满足，则按第五天收盘价卖出
# 统计数据
# - 总共多少只、总共产生多少个这个的买入时机、平均每只股票多少
# - 产生多少个买入时机、合计收益、平均单次收益、胜率
# ——————————
from statistics import mode
import sys,os
from types import CodeType

from numpy.lib.index_tricks import AxisConcatenator
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Strategy.Base as strat
import Data.Stock as st
import Data.Stock_codes as Stock_codes
import Data.Lib.Ashare as Ashare
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

data = st.get_csv_data('judge_stock_drop_5day_profit','Select_stock')
data = data[data['seil_signal_N_day'] != 0]
data['count'] = 0
data['make_money'] = np.where( data['profit'] > 0, 1, 0)
data['seil_signal_1_day'] = np.where( data['seil_signal_N_day'] == 1, 1, 0)

data_groupby = data.groupby('code')

ret_data = data_groupby.count()[['count']]
ret_data['累计收益'] = data_groupby.sum()['profit']
ret_data['胜率'] = data_groupby.sum()['make_money'] / ret_data['count']
ret_data['次日交易'] = data_groupby.sum()['seil_signal_1_day'] / ret_data['count']

ret_data.loc['all'] = ([ data.count()['count'], data['profit'].sum(), data.sum()['make_money'] / data.count()['count'], data.sum()['seil_signal_1_day'] / data['count'].count() ])

print(ret_data)
st.export_data(ret_data, filename='近一年连续跌5日买入策略统计', type='Select_stock', no_repeat=None)

