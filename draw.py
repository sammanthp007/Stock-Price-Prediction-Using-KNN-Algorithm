import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
import datetime

import matplotlib.pyplot as plt   # Import matplotlib

import plotly.plotly as py
import plotly
import plotly.graph_objs as go

line_up, = plt.plot([1,2,3], label='Line 2')
line_down, = plt.plot([3,2,1], label='Line 1')
plt.legend(handles=[line_up, line_down])

plt.show()
