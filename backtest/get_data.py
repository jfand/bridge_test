import tushare as ts
import pandas as pd
from datetime import datetime

# 获取股票数据并保存为csv文件
def get_data(ts_code,start_date,end_date):
    """
    通过输入股票代码，周期（开始时间和结束时间）获取股票数据并保存为csv文件
    :param ts_code: 股票代码，例：000001.SZ
    :param start_date: 开始时间，例：20230101
    :param end_date: 结束时间，例：20231231
    :return: None
    """

    # 设置Token
    ts.set_token('027a9090fcb4fdf9e405d01f6304f2e8fda69d30fe5f082c07ad9cc0')

    # 创建Tushare API接口对象
    pro = ts.pro_api()

    # 设置获取参数信息
    # ts_code = '000001.SZ' # 股票代码
    # start_date = '20230101' # 开始时间
    # end_date = '20231231' # 结束时间

    df = pro.daily(ts_code = ts_code, start_date = start_date, end_date = end_date)

    # 判断是否获取数据成功，认为获取数据size大于周期/2即为获取成功
    s_date = datetime.strptime(start_date,'%Y%m%d')
    e_date = datetime.strptime(end_date,'%Y%m%d')
    num = (e_date-s_date).days/2
    if len(df) > num:
        # 转换格式以符合Backtrader的要求
        df['date'] = pd.to_datetime(df['trade_date'])
        df.set_index('date',inplace=True)
        df.sort_index(inplace=True)

        df.rename(columns={'vol':'volume'},inplace=True)
        df = df[['open','high','low','close','volume']]
        df.reset_index(inplace = True)

        # 保存数据到CSV文件
        df.to_csv('stock_data.csv',index=False)
        return True

    else:
        return False
