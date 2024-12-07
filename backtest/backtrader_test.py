import backtrader as bt
from backtrader import *
from datetime import datetime
import pandas as pd
import sys

from get_data import get_data
from backtest import StrategyMA

# 用于测试backtrader并生成图像

ts_code = input('请输入股票代码（例：000001.SZ）：')
start_date = input('请输入开始日期（例：20230101）：')
end_date = input('请输入结束日期（例：20231231）：')

try:
    get_data(ts_code=ts_code,start_date=start_date,end_date=end_date)
except:
    print('输入的信息无效，请重新运行')
    sys.exit()

cerebro = bt.Cerebro()  # 创建量化回测程序入口

# 设置初始投资金额
dmoney0 = 1000000
cerebro.broker.setcash(dmoney0)
dcash0 = cerebro.broker.startingcash    # 获取初始投资金额

# 获取数据文件，csv格式
fdat = 'stock_data.csv'

# 读取csv文件
df = pd.read_csv(fdat)
df['date'] = pd.to_datetime(df['date'])     # 将date列转换未datetime形式

# 将读取的df转换未cerebro可读取的形式
data = bt.feeds.PandasData(dataname = df,   # dataframe类型数据
                           datetime='date', # 日期
                           open='open',     # 开盘价
                           high='high',     # 最高价
                           low='low',       # 最低价
                           close='close',   # 收盘价
                           volume='volume') # 规模

cerebro.adddata(data)  # cerebro添加数据
cerebro.addstrategy(StrategyMA)     # cerebro添加策略

cerebro.broker.set_slippage_perc(perc=0.0001)   # 设置滑点为万分之一

cerebro.run()   # 执行量化回测

# 量化回测结束，获取相关数据
dval9 = cerebro.broker.getvalue()   # 获取经纪人账户的总价值，包括现金余额和持仓市值
kret = (dval9-dcash0)/dcash0 * 100  # 计算投资回报率
print('\t 期初资金:%.2f' % dcash0)
print('\t 期末资金:%.2f' % dval9)
print('\t 投资回报率：%.2f %%' % kret)

# 绘制BT量化投资图像
cerebro.plot()
