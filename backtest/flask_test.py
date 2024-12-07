from flask import Flask, request
import get_data as gd
import backtrader as bt
from backtrader import *
from datetime import datetime
import pandas as pd
from backtest import StrategyMA

app = Flask(__name__)

@app.route('/', methods=['POST'])
def getdt():
    """
    通过web输入股票代码、开始日期、结束日期来获取股票数据并保存为csv格式
    :return:
    """
    try:
        ts_code = request.form['ts_code']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        get_data = gd.get_data(ts_code,start_date,end_date)     # get_data为bool类型，获取数据成功则为True，否则为False
    except:
        return f"<html><body>输入信息无效，请返回上一步重新输入！</body></html>"

    if get_data:
        return f"<html><body>你已经成功获取到股票数据！</body></html>"
    else:
        return f"<html><body>未成功获取到股票数据,请返回上一步重新测试！</body></html>"

@app.route('/backtest', methods=['GET'])
def backtest():

    cerebro = bt.Cerebro()  # 创建量化回测程序入口

    # 设置初始投资金额
    dmoney0 = 1000000
    cerebro.broker.setcash(dmoney0)
    dcash0 = cerebro.broker.startingcash    # 获取初始投资金额

    # 获取数据文件，csv格式
    fdat = 'stock_data.csv'

    try:
        # 尝试读取 CSV 文件
        df = pd.read_csv(fdat)

        # 尝试将 'date' 列转换为 datetime 格式
        df['date'] = pd.to_datetime(df['date'])

        # 将读取的df转换未cerebro可读取的形式
        data = bt.feeds.PandasData(dataname=df,  # dataframe类型数据
                                   datetime='date',  # 日期
                                   open='open',  # 开盘价
                                   high='high',  # 最高价
                                   low='low',  # 最低价
                                   close='close',  # 收盘价
                                   volume='volume')  # 规模

        cerebro.adddata(data)  # cerebro添加数据
        # my_startegy = StrategyMA()
        cerebro.addstrategy(StrategyMA)  # cerebro添加策略

        cerebro.broker.set_slippage_perc(perc=0.0001)  # 设置滑点为万分之一

        cerebro.run()  # 执行量化回测

        # 量化回测结束，获取相关数据
        dval9 = cerebro.broker.getvalue()  # 获取经纪人账户的总价值，包括现金余额和持仓市值
        kret = (dval9 - dcash0) / dcash0 * 100  # 计算投资回报率
        print('\t 期初资金:%.2f' % dcash0)
        print('\t 期末资金:%.2f' % dval9)
        print('\t 投资回报率：%.2f %%' % kret)

        # 绘图并保存
        # cerebro.plot(savefig=r'backtest.png',iplot=False)

        return (f"<html>"
                f"<body>"
                f"测试成功！"
                f"<p>总权益为：{dval9}</p>"
                f"<p>收益率为：{kret}%</p>"
                f"<p>"
                # f"<img src='backtest.png' alt='回测图表'></p>"
                f"</body>"
                f"</html>")

        # return (f"<!DOCTYPE html>"
        #         f"<html lang='en'>"
        #         f"<head>"
        #         f"    <meta charset='UTF-8'>"
        #         f"    <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
        #         f"    <title>Backtest Results</title>"
        #         f"    <style>"
        #         f"        body {{ font-family: Arial, sans-serif; margin: 20px; }}"
        #         f"        img {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}"
        #         f"    </style>"
        #         f"</head>"
        #         f"<body>"
        #         f"    <h1>测试成功！</h1>"
        #         f"    <p>总权益为: {dval9}</p>"
        #         f"    <p>收益率为: {kret}%</p>"
        #         f"    <p><img src='backtest.png' alt='回测图表'></p>"
        #         f"</body>"
        #         f"</html>")



    except FileNotFoundError:
        # 如果文件未找到，返回错误消息
        return f"<html><body>文件未找到！</body></html>"

    except pd.errors.EmptyDataError:
        # 如果文件为空，返回错误消息
        return f"<html><body>文件为空！</body></html>"




if __name__ == '__main__':
    app.run(debug=True)
