import sys,os

from numpy.lib.index_tricks import AxisConcatenator
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Strategy.Base as strat
import Data.Stock as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Data.Lib.Ashare as as_data
import time,datetime

data = st.get_single_price_csv_net(stock_code='000001.XSHE', timefrequency='daily', start_date='2022-02-21', end_date='2022-03-11')

print(data)