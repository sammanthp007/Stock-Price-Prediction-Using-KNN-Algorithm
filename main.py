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

import matplotlib.pyplot as plt   # Import matplotlib

import plotly.plotly as py
import plotly
import plotly.graph_objs as go

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2015,1,1)
end = datetime.date.today()

# Let's get Apple stock data; Apple's ticker symbol is AAPL
apple = web.DataReader('AAPL', 'yahoo', start, end)

print(apple.head())

# apple["Adj Close"].plot(grid = True) # Plot the adjusted closing price of AAPL
print(apple["Adj Close"])
apl = apple["Adj Close"]


plt.plot(apl)
# plt.show()

df = web.DataReader('AAPL', 'yahoo', start, end)
trace = go.Candlestick(x=df.index,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close
                       )
data = [trace]
plotly.offline.plot(data)
