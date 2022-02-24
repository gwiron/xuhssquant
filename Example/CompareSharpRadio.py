import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Data.Stock as st
import Strategy.Base as stb
import matplotlib.pyplot as plt
import pandas as pd

#计算3只股票的数据(比亚迪、宁德时代、隆基)
codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']

#存放sharp的容器
sharps = []
for code in codes:
    data = st.get_single_price(stock_code=code, timefrequency='daily', start_date='2018-10-01', end_date='2021-05-19')
    # 计算每只股票的夏普比率
    dailySharp, annualSharp = stb.calculate_sharp(data)
    sharps.append([code, annualSharp])

# 可视化3只股票并比较
sharps = pd.DataFrame(sharps, columns = ['code', 'sharpe']).set_index('code')
print(sharps)
sharps.plot.bar(title='compare annual sharp ratio')
plt.xticks(rotation=30)
plt.show()