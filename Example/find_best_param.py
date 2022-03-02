import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Data.Stock as st
import Strategy.ma_strategy as ma
import pandas as pd

# 参数1：股票池
code = '000001.XSHE'
data = st.get_single_price(stock_code=code, timefrequency='daily', start_date='2016-01-01', end_date='2021-01-01')
# 参数2：周期参数
params=[5, 10, 20, 60, 120, 250]

#存放参数与收益
res = []

# 匹配，并计算不同的周期参数对：5-10，5-20，...120-150
for short in params:
    for long in params:
        if long > short:
            print("当前周期参数对：", short, long)
            df = ma.ma_strategy(data=data, short_window=short, long_window=long)
            # 获取周期参数，及其对应的累计收益率
            cum_profit = df['cum_profit'].iloc[-1]
            #将参数放入结果列表
            res.append([short, long, cum_profit])

# 将结果李彪转换为df，并找到最优参数
res = pd.DataFrame(res,columns=['short_win', 'long_win', 'cum_profit'])
# 按收益倒叙排列
res = res.sort_values(by='cum_profit', ascending=False)
print(res)