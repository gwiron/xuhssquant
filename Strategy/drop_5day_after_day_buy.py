# ——————————
# 对前5日均是跌的股票，进行后一天盯盘买入 1% or 1% 则卖出，若不满足条件则后延1天，第五天未满足，则按第五天收盘价卖出
# 1、找到卖出日期，并计算收益率
# 2、统计数据
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

# 计算单日 卖出时机，并填写卖出收益，若无则 0（传入的data为已经过滤过的买入数据）
trade_days = [] # 初始化列表交易日日期，只获取一次
def cnt_seil_signal_after_N_day(data, after_N_day= 1, max_profit= 0.01, min_profit= -0.01, is_deadline= None):
    # 获取交易日期
    if (len(trade_days) == 0):
        start_date = data['date'].values[0]
        end_date = datetime.date.fromisoformat(data['date'].values[-1]) + datetime.timedelta(30)
        trade_days.extend(st.get_trade_days(start_date=start_date,end_date=end_date))
        # print(after_N_day, trade_days)

    # 进度数据登记
    data_len = len(data)
    data_i = 1

    for index, row in data.iterrows():

        print('当前收益率计算进度 ', after_N_day,'-', data_i, '/', data_len)
        data_i += 1

        # 计算卖出日期
        start_date = datetime.date.fromisoformat(row['date'])
        # print(row['date'])
        start_date = trade_days[ trade_days.index(start_date) + after_N_day ]
        end_date = start_date + datetime.timedelta(1)
        # print('股票卖出日期初始化', start_date,'~', end_date)

        # 获取日实时数据
        data_day_1m = st.get_single_price(row['code'],start_date=start_date, end_date=end_date, timefrequency='15m')

        # 获取买入价格
        buy_price = row['close']
        day_close = data_day_1m['close'][-1]

        # data_day_1m['max'] = (buy_price*(1+max_profit))
        # data_day_1m['min'] = (buy_price*(1+min_profit))

        # 计算卖出时机
        data_day_1m['seil_signal'] = np.where( (data_day_1m['close'] >= (buy_price*(1+max_profit)) ) | (data_day_1m['close'] <= (buy_price*(1+min_profit)) ), -1, 0 )
        
        # 过滤卖出时机价格
        data_day_1m = data_day_1m[data_day_1m['seil_signal'] == -1 ]

        # print(data_day_1m)

        # 计算卖出价格
        # print('是否存在卖出点：',len(data_day_1m))
        if len(data_day_1m) != 0:
            proift = (data_day_1m['close'][0] - buy_price) / buy_price

            # 填写卖出价格、后几天
            data.loc[ index, 'seil_signal_N_day' ] = after_N_day
            data.loc[ index, 'profit' ] = proift
            # print(proift)
        elif is_deadline == 'y':
            # 超过最后期限，以收盘价格未卖出价格

            proift = (day_close - buy_price) / buy_price
            data.loc[index, 'seil_signal_N_day'] = after_N_day + 0.1
            data.loc[index, 'profit'] = proift
            # print('超过期限',row['date'], '  ', row['code'], '  ', proift)
        
        # print(data)
        if (data_i % 1000) == 0:
            print('每计算1000个收益进行保存一次，防止每接口获取次数导致丢失')
            data_copy = data.set_index('date')
            st.export_data(data_copy, filename='judge_stock_drop_5day_profit_'+str(after_N_day), type='Select_stock', no_repeat=None)
    
    data_copy = data.set_index('date')
    st.export_data(data_copy[data_copy['seil_signal_N_day'] == 0], filename='judge_stock_drop_5day_profit_'+str(after_N_day), type='Select_stock', no_repeat=None)
    return data


def cnt_seil_signal(data, daadline_N_day= 1, max_profit= 0.01, min_profit= -0.01):
        
    # 字段初始化，当第二次访问时候不需要初始化
    # data['seil_signal_N_day'] = 0
    # data['profit'] = 0
    # print(data)

    is_deadline = None

    for after_N_day in range(daadline_N_day):
        ret_data = data[data['seil_signal_N_day'] == 0]
        
        # 计算收益率
        if len(ret_data) > 0:
            if (after_N_day+1 == daadline_N_day):
                is_deadline = 'y'
            ret_data = cnt_seil_signal_after_N_day(ret_data, after_N_day+1, max_profit=max_profit, min_profit=min_profit, is_deadline=is_deadline)
            # print(ret_data)

            # 计算结果赋值
            data.loc[ret_data.index.values, 'seil_signal_N_day'] = ret_data['seil_signal_N_day'].values
            data.loc[ret_data.index.values, 'profit'] = ret_data['profit'].values
        # print(data)
    return data
        

# data = st.get_csv_price(stock_code='000001.XSHE', timefrequency='daily', start_date='2021-01-01', end_date='2021-02-01')
# data['code'] = '000001.XSHE'
# data['buy_signal'] = 1

if __name__ == '__main__':
    data = st.get_csv_data('judge_stock_drop_5day_profit','Select_stock')
    # data['seil_signal_N_day'] = 0
    
    ret_data = data[(data['drop_5day'] == 1)]
    ret_data = ret_data.sort_values(by='date', ascending=True)
    ret_data = ret_data[ret_data['date'] > '2021-01-01']
    # ret_data = ret_data.head(50)
    # ret_data = ret_data.set_index('date')
    ret_data['buy_signal'] = 1
    # print(data,ret_data)

    ret_data = cnt_seil_signal(ret_data, 3, 0.01, -0.01)

    data.loc[ret_data.index.values, 'seil_signal_N_day'] = ret_data['seil_signal_N_day'].values
    data.loc[ret_data.index.values, 'profit'] = ret_data['profit'].values

    data = data[data['seil_signal_N_day'] != 0 ]

    data = data.set_index('date')
    # 追加输出csv
    st.export_data(data, filename='judge_stock_drop_5day_profit', type='Select_stock', no_repeat=None)


    # 日期格式不对修改
    # data[['date']] = data[['date']].apply(pd.to_datetime)
    # print(data)
    # data = data.set_index('date')
    # st.export_data(data, filename='judge_stock_drop_5day_profit', type='Select_stock', no_repeat=None)
    # exit()