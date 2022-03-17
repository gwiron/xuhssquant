# ——————————
# 寻找近制定日期的前5日均是跌的股票，打印后5天的数据表现
# ——————————

import sys,os
from types import CodeType

from numpy.lib.index_tricks import AxisConcatenator
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Strategy.Base as strat
import Data.Stock as st
import Data.Stock_codes as Stock_codes
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Data.Lib.Ashare as as_data

# 股票池
# stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE'] 
# stocks = st.get_stock_list()
stocks = Stock_codes.data
# print(stocks)

def judge_stock_drop_5day(data):
    data['drop_5day'] = np.where(\
        (data['close'] < data['close'].shift(1)) &\
        (data['close'].shift(1) < data['close'].shift(2)) &\
        (data['close'].shift(2) < data['close'].shift(3)) &\
        (data['close'].shift(3) < data['close'].shift(4)) &\
        (data['close'].shift(4) < data['close'].shift(5)), 1, 0)
    return data

def judge_stock_rise_5day(data):
    data['rise_5day'] = np.where(\
        (data['close'] > data['close'].shift(1)) &\
        (data['close'].shift(1) > data['close'].shift(2)) &\
        (data['close'].shift(2) > data['close'].shift(3)) &\
        (data['close'].shift(3) > data['close'].shift(4)) &\
        (data['close'].shift(4) > data['close'].shift(5)), 1, 0)
    return data

def data_filter(data, type):
    data[type + '_5day_after_in_5day'] = np.where( (\
        (data[type + '_5day'].shift(1) == 1 ) |\
        (data[type + '_5day'].shift(2) == 1 ) |\
        (data[type + '_5day'].shift(3) == 1 ) |\
        (data[type + '_5day'].shift(4) == 1 ) |\
        (data[type + '_5day'].shift(5) == 1 )  ), 1, 0)
        
    # data[type + '_5day_before_in_5day'] = np.where( (\
    #     (data[type + '_5day'].shift(-1) == 1 ) |\
    #     (data[type + '_5day'].shift(-2) == 1 ) |\
    #     (data[type + '_5day'].shift(-3) == 1 ) |\
    #     (data[type + '_5day'].shift(-4) == 1 ) |\
    #     (data[type + '_5day'].shift(-5) == 1 )  ), 1, 0)

    data = data[ (data[type + '_5day'] == 1 ) |\
        (data[type + '_5day_after_in_5day'] == 1)]
        # (data[type + '_5day_before_in_5day'] == 1) ]
    return data

res_stocks = []
mode = None
finalname = BASE_DIR + '/Data/Select_stock/' + 'judge_stock_drop_5day' + '.csv'

is_loc_fil = False
loc_stocks_data = pd.DataFrame()
if os.path.exists(finalname):
    loc_stocks_data = pd.read_csv(finalname, usecols=['code'])
    is_loc_fil = True

# 找出指定日期连续跌的股票
for code in stocks:
    if (is_loc_fil == False) or ( not (code in loc_stocks_data['code'].values) ):
        # data = as_data.get_price(code=code, count=2892)
        # data['money'] = ''
        data = st.get_csv_price(stock_code=code, timefrequency='daily', start_date='2010-01-01', end_date='2022-03-11')
        print('获取代码',code,'数据成功')
        data['code'] = code

        data = judge_stock_drop_5day(data)
        data = data_filter(data, 'drop')
        data = data[['code','open','close','high','low','volume','money','drop_5day','drop_5day_after_in_5day']]
        # print(data)

        # 追加输出csv
        st.export_data(data, filename='judge_stock_drop_5day', type='Select_stock',mode=mode,no_repeat=None)
        mode = 'a'
    else:
        print('股票代码',code, '已经存在')





# def judge_stock_drop_5day(data):
    # if data['close'].iloc[-1] < data['close'].iloc[-2] and\
    # data['close'].iloc[-2] < data['close'].iloc[-3] and\
    # data['close'].iloc[-3] < data['close'].iloc[-4] and\
    # data['close'].iloc[-4] < data['close'].iloc[-5] and\
    # data['close'].iloc[-5] < data['close'].iloc[-6] :
    #     return 1
    # else :
    #     return 0
# 3月1日 之前5天连续跌的股票代码
# res_stocks = ['000826.XSHE', '001965.XSHE', '002146.XSHE', '002614.XSHE', '002917.XSHE', '002918.XSHE', '003037.XSHE', '300096.XSHE', '300640.XSHE', '300679.XSHE', '600346.XSHG', '600823.XSHG', '603979.XSHG']
