from fileinput import filename
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from jqdatasdk import *
import pandas as pd
import time,datetime

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
        if end_date is None:
            end_date = datetime.datetime.today()

        data = get_price(stock_code, start_date=start_date, end_date=end_date, frequency=timefrequency)
    else :
        if end_date is None:
            end_date = datetime.datetime.today()
        data = get_price(stock_code, count=count, end_date=end_date, frequency=timefrequency)
    return data

# 导出股票相关的数据(type:存储的文件夹的名称[Finace/Price])
def export_data(data, filename, type, mode=None):
    finalname = BASE_DIR + '/Data/' + type +'/' + filename + '.csv'
    data.index.names = ['date']
    if mode == 'a':
        data.to_csv(finalname, mode=mode, header=False)
        # 刪除重复值
        data = pd.read_csv(finalname)
        data = data.drop_duplicates(subset=['date']) # 以日期列为准
        data = data.set_index(['date']) # 设置索引为 date
        data.to_csv(finalname) # 再次写入
    else:
        data.to_csv(finalname)
    print('保存成功，存储路径是：', finalname)
    # data.index.names = ['date']
    # data.to_csv(finalname)
    # print('已经存储成功，存储路径为', finalname)

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

# 从本地获取股票行情数据
def get_csv_price(code, start_date, end_date, type='Price'):
    # 使用update获取
    update_daily_price(code, type=type)
    # 读取数据库对应的股票csv文件
    finalname = BASE_DIR + '/Data/' + type + '/' + code + '.csv'
    data = pd.read_csv(finalname, index_col='date')
    # 根据起始终止日期筛选数据
    return  data[(data.index >= start_date) & (data.index <= end_date)]

#涨跌幅计算
def calculate_change_pct(data):
    """
    公式：(当期收盘价-前期收盘价)/前期收盘价
    :param data:dataframe 带有收盘价
    :return: dataframe 带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data

# 每日获取数据
def update_daily_price(stockCode, type='Price'):
    # 0是否存在文件：不存在-再次获取，存在-3.2
    finalname = BASE_DIR + '/Data/' + type +'/' + stockCode + '.csv'
    if os.path.exists(finalname):
        # 1获取增量数据（code, startdate=对应股票csv中日期，enddate=今天）
        startdate = pd.read_csv(finalname, usecols=['date'])['date'].iloc[-1]
        print(startdate)
        df = get_single_price(stockCode, 'daily', startdate, datetime.datetime.today())
        # 2追加到已有文件中（是否存在文件：创建csv,追加数据）
        export_data(df, stockCode, 'Price', 'a')
        print("股票数据已经从远程增强获取成功：", stockCode)
    else:
        # 首次获取股票行情数据
        df = get_single_price(stockCode, 'daily', None, None)
        export_data(df, stockCode, 'Price')
        print("股票数据已经从远程首次获取成功：", stockCode)

# 股票数据库全量下载 or 更新
def update_price_db():
    # 1.获取所有的股票代码
    stocks = get_stock_list()
    # 2.存储到csv文件中
    for stockCode in stocks:
        update_daily_price(stockCode, 'Price')