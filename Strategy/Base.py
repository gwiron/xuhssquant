import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Data.Stock as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#整合信号
def compose_signal(data):
    data['buy_signal'] = np.where((data['buy_signal']==1) & (data['buy_signal'].shift(1)==1),0,data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal']==-1) & (data['sell_signal'].shift(1)==-1),0,data['sell_signal'])
    #合并信号
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

#计算单次收益率：开仓、平仓（开仓的全部股数）
def calculate_profit_pct(data):
    data = data[data['signal']!=0]
    data = data.copy() # 防止报错提醒
    data['profit_pct'] = ((data['close']-data['close'].shift(1))/data['close'].shift(1))
    data = data[data['signal']!=1]
    return data

# 计算累计收益率
def calculate_cum_prof(data):
    data['cum_profit'] = pd.DataFrame(1+data['profit_pct']).cumprod()-1
    return data

#计算最大回撤率
def caculate_max_drawndown(data):
    #选取时间周期（时间窗口）
    window = 252 #(7代表过去一周的时间窗口，这里根据你的时间轴的单位而定，这里是7天)
    #选取时间周期中的最大净值(min_periods表示每个窗口至少要的观测值)
    data['rolling_max'] = data['close'].rolling(window=7, min_periods=1).max()
    #计算当天的回撤比：[回撤比 = (谷值-峰值) / 峰值 = 谷值/峰值-1]也就是历史的最大净值和今天比，回撤了多少，这个回撤可能是负的，负的代表的是亏的。
    data['daily_drawndown'] = data['close']/data['rolling_max']-1
    #选取时间周期内最大的回撤比及最大回撤。
    data['max_drawndown'] = data['daily_drawndown'].rolling(window, min_periods=1).min()#为什么是min最小，比如说回撤比，他可能是-10%，-50%,越是负，值越小，回撤其实就是越大的，
    return data

#计算夏普率
def calculate_sharp(data):
    #公式 夏普率 = (回报率均值 - 无风险率) / 回报率的标准差
    # pct_change()是pandas里面的自带的计算每日增长率的函数，它和calculate_profit_pct函数功能是一样的，用于计算股票的单次收益率。
    daily_return = data['close'].pct_change()
    # 回报率均值 
    avg_return = daily_return.mean()
    # 回报率标准差
    std_return = daily_return.std()
    #计算夏普
    sharp = avg_return / std_return
    #计算夏普 年华夏普
    sharp_year = sharp * np.sqrt(252)
    return sharp, sharp_year

#用来创建交易策略、生成交易信号
def week_period_strategy(stock_code, timefrequency, start_date=None, end_date=None):
    #获取数据
    data = st.get_single_price(stock_code, timefrequency, start_date, end_date)
    # print(data)
    #创建周期字段
    data['weekday'] = data.index.weekday
    #周四交易：买入(0:不操作 1:买入)
    # data['buy_signal'] = np.where((data['weekday']==3),1,0) 
    #周一交易：卖出(0:不操作 1:卖出)
    data['sell_signal'] = np.where((data['weekday']==0),-1,0)
    data['buy_signal'] = np.where((data['weekday']==3) | (data['weekday']==4),1,0) 

    #特殊情况处理
    data = compose_signal(data)
    #计算单次收益率：开仓、平仓（开仓的全部股数）
    data = calculate_profit_pct(data)
    # 计算累计收益率 
    data = calculate_cum_prof(data)

    return data

if __name__ == '__main__':
    data = week_period_strategy(stock_code='000001.XSHE', timefrequency='daily', end_date='2021-06-01',)
    print(data)

    # # pandas 表格的描述计算
    # print(data.describe())

    # # 单次收益输出为需要绘图
    # # data['profit_pct'].plot()
    # # 累计收益输出为需要绘图
    # data['cum_profit'].plot()
    # plt.show()

    # data = st.get_single_price(stock_code='000001.XSHE', timefrequency='daily', start_date='2015-06-01', end_date='2021-01-01')
    # # 计算最大回撤率
    # data = caculate_max_drawndown(data)
    # print(data)
    # data[['daily_drawndown', 'max_drawndown']].plot()
    # plt.show()

    # data = st.get_single_price(stock_code='000001.XSHE', timefrequency='daily', start_date='2006-06-01', end_date='2021-06-01')
    # # 计算最大回撤率
    # sharp = calculate_sharp(data)
    # print(sharp)