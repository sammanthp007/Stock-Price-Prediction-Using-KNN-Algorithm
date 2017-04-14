# import quandl
# 
# mydata = quandl.get("NSX/NUGT", authtoken="umFJsnAKJbkZks7xXAy8", start_date="2012-04-01")
# 
# 
# print(type(mydata))
# print(mydata)

import pandas as pd
# import pandas.io.data as web   # Package and modules for importing data; this code may change depending on pandas version
from pandas_datareader import data, wb
import pandas_datareader as pdr
import datetime
 
# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2016,1,1)
end = datetime.date.today()
 
# Let's get Apple stock data; Apple's ticker symbol is AAPL
# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
# apple = wb.DataReader("AAPL", "yahoo", start, end)
apple = pdr.get_data_yahoo('AAPL')
 
print (type(apple))
print(apple.head())


f = pdr.DataReader("F", "yahoo", start, end)

import matplotlib.pyplot as plt   # Import matplotlib
# This line is necessary for the plot to appear in a Jupyter notebook

# Control the default size of figures in this Jupyter notebook

# pylab.rcParams['figure.figsize'] = (15, 9)   # Change the size of plots
# plt.plot([1,2,3,4])
# plt.show()
apple["Adj Close"].plot(grid = True) # Plot the adjusted closing price of AAPL
print(apple["Adj Close"])
apl = apple["Adj Close"]


plt.plot(apl)
plt.show()
