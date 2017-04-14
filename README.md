# Stock Prediction Using *K*-Nearest Neighbor (*k*NN) Algorithm

I applied k-nearest neighbor algorithm and non-linear regression approach in
order to predict stock proces for a sample of six major companies listed on the
NASDAQ stock exchange to assist investors, management, decision makers, and
users in making correct and informed investments decisions.

## To run
```
sources py2/bin/activate
pip install -r requirements.txt

python predictStockRiseOrFall.py
```

**OPEN** is the proce of the stock at tha beginning of the trading day (it 
need not be the closing price of the previous day).

**High** is the highest price of the stock at closing time.

**Low** is the lowest price of the stock on that trading day.

**Close** is the price of the stock at closing time.

**Volume** indicates how many stocks were traded.

**Adjusted Close** is the closing price of the stock that adjusts the price of 
the stock for corporate actions.

While stock prices are considered to be set mostly by traders, **stock** splits
(when the company makes each extant stock worth two and halves the price) and
**dividends** (payout of company profits per share) also affect the price of a 
stock and should be accounted for.

### Visualizing data using matplotlib
A linechart is fine, but we are considering 5 data points as important data.
They include Trading Volume, Open, Highest, Lowest, and Closing prices. So, we
would like to visualize these data in a way that all five variables can be shown
in the same graph, and not in 5 separate graphs. *Financial data is ofter 
plotted with a* **Japanese candlestick plot**. We can create such diagram in
matplotlib, but we have implemented the diagram in `plotting_functions.py`.



