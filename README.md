# Stock Prediction Using *K*-Nearest Neighbor (*k*NN) Algorithm

I applied k-nearest neighbor algorithm and non-linear regression approach in
order to predict stock proces for a sample of six major companies listed on the
NASDAQ stock exchange to assist investors, management, decision makers, and
users in making correct and informed investments decisions.

## To run
```
pip install -r requirements.txt

python main.py
```

## Some Stock Market terminologies

**OPEN** is the price of the stock at the beginning of the trading day (it 
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

## *K* Nearest Neighbor (*k*NN) Algorithm

The model for kNN is the entire training dataset. When a prediction is required
for a unseen data instance, the kNN algorithm will search through the training 
dataset for the k-most similar instances. The prediction attribute of the most 
similar instances is summarised and returned as the prediction for the unseen
instance.

The similarity measure is dependent on the type of data. For real-valued data, 
the Euclidean distance can be used. For other types of data, such as categorical
or binary data, Hamming distance can be used.

In the case of regression problems, the average of the predicted attribute may 
be returned.

In case of classification, the most prevalent class may be returned.

### How does it work?
The kNN algorithm belongs to the family of
[instance-based](https://en.wikipedia.org/wiki/Instance-based_learning "In
machine learning, instance-based learning, sometimes called memory-based
learning, is a family of learning algorithms that, instead of performing
explicit generalization, compares new problem instances with instances seen in
training, which have been stored in memory."), competitive learning and lazy
learning algorithms.
