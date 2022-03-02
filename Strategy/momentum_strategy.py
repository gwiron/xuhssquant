import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Data.Stock as st

# 获取沪深300股票池
def get_data(index_symbol = '000300.XSHG'):
    #获取股票列表代码(沪深300、创业板、上证)
    stocks =st.get_index_list(index_symbol=index_symbol)
    #获取股票数据
    for code in stocks:
        data = st.get_single_price(code, 'daily')
        #预览股票数据
        print("================",code, "================")
        print(data.tail())

# 正向动量策略
def momentum():
    get_data()

if __name__ == '__main__':
    momentum()