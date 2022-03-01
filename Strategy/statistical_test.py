import re
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Data.Stock as st
import Strategy.Base as stb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Strategy.ma_strategy as ma
from scipy import stats

# 对策略收益进行ttest检验
def ttest(data_return): 
    # 调用假设检验tt est函数：scipy
    t, p =  stats.ttest_1samp(data_return, 0, nan_policy='omit')
    # 获取单边P值
    p_value = p/2 
    # 打印t、P
    print("t value:" , t)
    print("p value:" , p_value)

    # 判断是否与理论均值有显著性差异
    print("是否拒绝H0:收益均值=0：", p < 0.05)
    return t, p_value

if __name__ == '__main__':
    code = '000001.XSHE'
    data = st.get_single_price(stock_code=code, timefrequency='daily', start_date=None, end_date='2021-01-01')
    data = ma.ma_strategy(data)
    # print(data)
    # 策略的单次收益率
    returns = data['profit_pct']
    print(returns)
    # 绘制一下分布图用于观察
    # plt.hist(returns, bins=30)
    # plt.show()
    #对多个股票进行计算和测试
    ttest(returns)

# if __name__ == '__main__':
#     stocks = ['000001.XSHE','000858.XSHE','002594.XSHE']
#     for code in stocks:
#         data = st.get_single_price(stock_code=code, timefrequency='daily', start_date='2016-12-01', end_date='2021-01-01')
#         data = ma.ma_strategy(data)
#         # 策略的单次收益率
#         returns = data['profit_pct']
#         # print(returns)
#         # 绘制一下分布图用于观察
#         # plt.hist(returns, bins=30)
#         # plt.show()
#         #对多个股票进行计算和测试
#         print(code)
#         ttest(returns)