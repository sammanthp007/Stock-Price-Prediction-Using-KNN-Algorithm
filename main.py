# import quandl
# 
# mydata = quandl.get("NSX/NUGT", authtoken="umFJsnAKJbkZks7xXAy8", start_date="2012-04-01")
# 
# 
# print(type(mydata))
# print(mydata)

import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
import datetime

import pandas as pd

import matplotlib.pyplot as plt   # Import matplotlib

import plotly.plotly as py
import plotly
import plotly.graph_objs as go

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2015,1,1)
end = datetime.date.today()

# Let's get Apple stock data; Apple's ticker symbol is AAPL
apple = web.DataReader('AAPL', 'yahoo', start, end)
microsoft = web.DataReader("MSFT", "yahoo", start, end)
disney = web.DataReader("DIS", "yahoo", start, end)
nugt = web.DataReader("NUGT", "yahoo", start, end)
dust = web.DataReader("DUST", "yahoo", start, end)

# Below I create a DataFrame consisting of the adjusted closing price of these stocks, first by making a list of these objects and using the join method
stocks = pd.DataFrame({"AAPL": apple["Adj Close"],
                      "DIS": disney["Adj Close"],
                      "NUGT": nugt["Adj Close"],
                      "DUST": dust["Adj Close"]})

print(stocks.head())

ax1 = stocks.plot(secondary_y = ["AAPL", "DIS"],grid=True)
lines, labels = ax1.get_legend_handles_labels()

ax1.legend(lines[:5], labels[:5], loc="best")


# plt.plot(stocks)
plt.show()

df = web.DataReader('AAPL', 'yahoo', start, end)
trace = go.Candlestick(x=df.index,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close
                       )
data = [trace]
# plotly.offline.plot(data)


