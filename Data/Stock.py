from fileinput import filename
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from jqdatasdk import *
import pandas as pd
import time

auth('17606513012','3344Woaini')

# 获取所有A股股票列表
def get_stock_list():
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list

# 获取单个股票行情数据
def get_single_price(stock_code, timefrequency, start_date=None, end_date=None, count=None):        
    if count == None:
        #如果start_date为None你默认从上市日期开始计算
        if start_date is None:
            start_date = get_security_info(stock_code).start_date
        # print(stock_code, ' 的上市时间是 ', start_date)

        data = get_price(stock_code, start_date=start_date, end_date=end_date, frequency=timefrequency)
    else :
        data = get_price(stock_code, count=count, end_date=end_date, frequency=timefrequency)
    return data

# 导出股票相关的数据(type:存储的文件夹的名称[Finace/Price])
def export_data(data, filename, type):
    fileroot = BASE_DIR + '/Data/' + type +'/' + filename + '.csv'
    data.index.names = ['date']
    data.to_csv(fileroot)
    print('已经存储成功，存储路径为', fileroot)

# 将数据转换股票行情指定周期
def transfer_price_freq(data, timefrequency):
    df_trans = pd.DataFrame()
    df_trans["open"] = data["open"].resample(timefrequency).first()
    df_trans['close'] = data['close'].resample(timefrequency).last()
    df_trans['high'] = data['high'].resample(timefrequency).max()
    df_trans['low'] = data['low'].resample(timefrequency).min()
    df_trans['volume(sum)'] = data['volume'].resample(timefrequency).sum()
    df_trans['money(sum)'] = data['money'].resample(timefrequency).sum()
    return df_trans

# 获取单个股票财务指标 
def get_single_finance(code, date, statDate):
    data = get_fundamentals(query(indicator).filter(indicator.code == code), date = date, statDate=statDate)
    return data

# 获取单个股票估值指标
def get_single_valuation(code, date, statDate):
    data = get_fundamentals(query(valuation).filter(valuation.code == code), date = date, statDate=statDate)
    return data

# 读取本地csv文件数据
def get_csv_data(code, type):
    fileroot = BASE_DIR + '/Data/' + type +'/' + code + '.csv'
    return pd.read_csv(fileroot)

#涨跌幅计算
def calculate_change_pct(data):
    """
    公式：(当期收盘价-前期收盘价)/前期收盘价
    :param data:dataframe 带有收盘价
    :return: dataframe 带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data