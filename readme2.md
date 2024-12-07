# bridge_test

## 测试方法一：

运行backtrader_test.py文件，输入股票代码和周期，即可运行，按照均线策略进行投资

输出该投资策略的收益与期末净值，并绘图



## 测试方法二：

运行flask_test.py文件，然后打开网页中打开templates目录下的index.html，输入股票代码与周期，获取数据。

- 若成果获取数据，则在当前url中后面添加/backtest，即可获得股票期末净值与收益率

- 示例

  ```bash
  http://localhost:5000/backtest
  ```

- 若获取股票数据失败，则返回前一步进行重新输入股票相关数据



参考：

- backtrader参考：（[从零开始掌握BackTrader量化框架_C与Python实战的博客-CSDN博客](https://blog.csdn.net/yaoyefengchen/category_12544415.html)）

- python后端flask参考：（https://xugaoxiang.com/2020/03/18/flask-5-get-post/）
- 获取数据：tushare



- backtest.py：均线量化策略
- backtrader_test.py：backtest.py测试程序
- flask_test.py: python后端
- get_data.py: 获取股票数据
- index.html: html页面