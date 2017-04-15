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


With a candlestick chart, a black candlestick indicates a day where the closing
price was higher than the open (a gain), while a red candlestick indicates a
day where the open was higher than the close (a loss). The wicks indicate the
high and the low, and the body the open and close (hue is used to determine
which end of the body is the open and which the close). Candlestick charts are
popular in finance and some strategies in technical analysis use them to make
trading decisions, depending on the shape, color, and position of the candles.
I will not cover such strategies today.

We may wish to plot multiple financial instruments together; we may want to
compare stocks, compare them to the market, or look at other securities such as
exchange-traded funds (ETFs). Later, we will also want to see how to plot a
financial instrument against some indicator, like a moving average. For this
you would rather use a line chart than a candlestick chart. (How would you plot
multiple candlestick charts on top of one another without cluttering the
chart?)

Below, I get stock data for some other tech companies and plot their adjusted
close together.


However, the chart we get does not give us much information

While absolute price is important (pricy stocks are difficult to purchase,
which affects not only their volatility but your ability to trade that stock),
when trading, we are more concerned about the relative change of an asset
rather than its absolute price. Google’s stocks are much more expensive than
Apple’s or Microsoft’s, and this difference makes Apple’s and Microsoft’s
stocks appear much less volatile than they truly are.

One solution would be to use two different scales when plotting the data; one
scale will be used by Apple and Microsoft stocks, and the other by Google.

```
stocks.plot(secondary_y = ["AAPL", "MSFT"], grid = True)
```

A “better” solution, though, would be to plot the information we actually want:
the stock’s returns. This involves transforming the data into something more
useful for our purposes. There are multiple transformations we could apply.

One transformation would be to consider the stock’s return since the beginning
of the period of interest. In other words, we plot:

return = (price at t / price at 0)

In python:

```
# df.apply(arg) will apply the function arg to each column in df, and return a
# DataFrame with the result
# Recall that lambda x is an anonymous function accepting parameter x; in this
# case, x will be a pandas Series object
stock_return = stocks.apply(lambda x: x / x[0])
stock_return.head()
```

All this information can be found in [this
blog](https://ntguardian.wordpress.com/2016/09/19/introduction-stock-market-data-python-1/)
