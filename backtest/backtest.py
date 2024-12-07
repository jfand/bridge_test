import backtrader as bt
from backtrader import *
from datetime import datetime
import pandas as pd



class StrategyMA(bt.Strategy):
    """
    创建一个回测策略，MA均线策略
    当MA12大于MA26时买入，小于时卖出
    买入:本金的20%
    卖出:全部平仓
    """

    # 定义MA均线策略的周期参数变量，分别是12天均线周期和26天均线周期
    params = (
        ('ma12',12), # 12天均线周期
        ('ma26',26)  # 26天均线周期
    )

    def __init__(self):
        # 获取第一个数据源的收盘价，使用self.data或self.datas[0]
        self.dataclose = self.datas[0].close    # 获取收盘价close
        # self.buy_money = 0.2*cerebro.broker.startingcash    # 每次购买的金额数，本金的20%
        self.buy_money = 0.2*1000000

        # 订单，默认为None
        self.order = None

        # 获取12天和26天MA均线指标
        self.sma12 = bt.indicators.SimpleMovingAverage(
            self.datas[0],period=self.params.ma12
        )
        self.sma26 = bt.indicators.SimpleMovingAverage(
            self.datas[0],period = self.params.ma26
        )


    def log(self,txt):
        # log记录函数
        dt = self.datas[0].datetime.date(0) # 获取当前日期
        print('%s, %s' % (dt.isoformat(),txt))  # 将dt日期对象转换为iso格式化字符串

    def notify_order(self, order):
        """
        当订单order状态改变时自动调用
        :param order: self.order
        """
        if order.status in [order.Submitted, order.Accepted]:
            # 检查订单执行状态order.status：
            # Buy/Sell order submitted/accepted to/by broker
            # broker经纪人：submitted提交/accepted接受,Buy买单/Sell卖单
            # 正常流程，无需额外操作
            return

        # 检查订单order是否完成
        # 注意: 如果现金不足，经纪人broker会拒绝订单reject order
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买单执行BUY EXECUTED, 报价：%.2f' % order.executed.price)
            elif order.issell():
                self.log('卖单执行SELL EXECUTED,报价： %.2f' % order.executed.price)

            # self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单Order： 取消Canceled/保证金Margin/拒绝Rejected')

        # 检查完成，没有交易中订单
        self.order = None

    def notify_trade(self,trade):
        """
        当一个sell或buy策略执行结束时自动调用
        :param trade:策略，如buy或sell
        """
        # 检查交易trade时否关闭，若交易未关闭，则直接返回；若trade正常关闭，则继续执行
        if not trade.isclosed:
            return

        self.log('交易利润，毛利： %.2f，净利： %.2f'% (trade.pnl,trade.pnlcomm))   # 更新输出日志

    def next(self):
        # 每进行一个bar都会执行一次next

        self.log('Close 收盘价，%.2f' % self.dataclose[0])  # 更新收盘价日志

        if self.order:  # 若订单未完成，不为None，则不继续往后执行
            return

        # 使用均线MA策略
        if self.broker.get_cash() >= self.buy_money:    # 当经纪人账户余额大于一次购买金额时，才能进行buy策略
            if self.sma12[0] > self.sma26[0]:   # 当ma12 大于 ma26时，执行buy策略
                self.log('设置买单BUY,%.2f'  # 更新日志
                         % (self.dataclose[0]))

                # 购买数量，使用每次购买金额除以当日收盘价来获取购买数量
                size = self.buy_money/self.data.close[0]

                self.order = self.buy(size=size)    # 执行buy策略

        # self.position检测仓位，只有仓位不为空时才能进行卖操作
        if self.position.size > 0 :
            if self.sma12[0] < self.sma26[0]:   # ma12 小于 ma26时，执行sell策略
                self.log('设置卖单SELL, %.2f' %
                         self.dataclose[0])     # 更新日志
                # 执行sell策略
                self.order = self.sell(size=self.position.size)


# 测试部分
# cerebro = bt.Cerebro()  # 创建量化回测程序入口
#
# # 设置初始投资金额
# dmoney0 = 1000000
# cerebro.broker.setcash(dmoney0)
# dcash0 = cerebro.broker.startingcash    # 获取初始投资金额
#
# # 获取数据文件，csv格式
# fdat = 'stock_data.csv'
#
# # 读取csv文件
# df = pd.read_csv(fdat)
# df['date'] = pd.to_datetime(df['date'])     # 将date列转换未datetime形式
#
# # 将读取的df转换未cerebro可读取的形式
# data = bt.feeds.PandasData(dataname = df,   # dataframe类型数据
#                            datetime='date', # 日期
#                            open='open',     # 开盘价
#                            high='high',     # 最高价
#                            low='low',       # 最低价
#                            close='close',   # 收盘价
#                            volume='volume') # 规模
#
# cerebro.adddata(data)  # cerebro添加数据
# cerebro.addstrategy(StrategyMA)     # cerebro添加策略
#
# cerebro.broker.set_slippage_perc(perc=0.0001)   # 设置滑点为万分之一
#
# cerebro.run()   # 执行量化回测
#
# # 量化回测结束，获取相关数据
# dval9 = cerebro.broker.getvalue()   # 获取经纪人账户的总价值，包括现金余额和持仓市值
# kret = (dval9-dcash0)/dcash0 * 100  # 计算投资回报率
# print('\t 期初资金:%.2f' % dcash0)
# print('\t 期末资金:%.2f' % dval9)
# print('\t 投资回报率：%.2f %%' % kret)
#
# # 绘制BT量化投资图像
# cerebro.plot()

