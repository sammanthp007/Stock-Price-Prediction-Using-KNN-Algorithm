import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
import datetime

import matplotlib.pyplot as plt   # Import matplotlib

import plotly.plotly as py
import plotly
import plotly.graph_objs as go

# We will look at stock prices over the past year, starting at January 1, 2016
# CHANGABLE VARIABLES
start = datetime.datetime(2015,1,1)
end = datetime.date.today()

# Let's get Apple stock data; Apple's ticker symbol is AAPL
apple = web.DataReader('AAPL', 'yahoo', start, end)
microsoft = web.DataReader("MSFT", "yahoo", start, end)
disney = web.DataReader("DIS", "yahoo", start, end)
nugt = web.DataReader("NUGT", "yahoo", start, end)
dust = web.DataReader("DUST", "yahoo", start, end)

# Below I create a DataFrame consisting of the adjusted closing price of these
# stocks, first by making a list of these objects and using the join method
stocks1 = pd.DataFrame({"AAPL": apple["Adj Close"],
                      "DIS": disney["Adj Close"]})
plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(stocks1)
plt.grid(True)
# lines1, labels1 = ax1.get_legend_handles_labels()
# 
# ax1.legend(lines1[:2], labels1[:2], loc="best")

plt.subplot(2, 1, 2)
stock_return = stocks1.apply(lambda x: x / x[0])
plt.plot(stock_return)
plt.grid(True)
plt.legend("a", "b")
plt.axhline(y=1, linewidth=2, color = 'k')
# stock_return.plot(grid = True).axhline(y = 1, color = "black", lw = 2)

# For NUGT and DUST

plt.figure(2)
plt.subplot(2, 2, 1)
stocks2 = pd.DataFrame({"NUGT": nugt["Adj Close"],
                      "DUST": dust["Adj Close"]})
plt.plot(stocks2)
plt.grid(True)
# lines2, labels2 = ax2.get_legend_handles_labels()

plt.subplot(2, 1, 2)
stock_return2= stocks2.apply(lambda x: x / x[0])
plt.plot(stock_return2)
plt.grid(True)
plt.legend("a", "b")
plt.axhline(y=1, linewidth=2, color = 'k')
#ax1.legend(lines2[:2], labels2[:2], loc="best")
plt.show()
