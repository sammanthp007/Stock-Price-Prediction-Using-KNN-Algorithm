import csv
import random
import math
import operator

import pandas_datareader.data as web
import datetime

# split the data into a trainingdataset and testdataset in ratio of 67/33
def loadDataset(filename, split, trainingSet=[], testSet=[], content_header=[]):
    # open the file
    # data format:
    # sepal length, sepal width, petal length, petal width, classification
    # e.g 
    # 5.9, 3.0, 5.1, 1.8, Iris-virginica
    with open(filename, 'rb') as csvfile:
        # returns a reader object which will iterate over lines
        lines = csv.reader(csvfile)
        # dataset is a list of all data, where each item is a line as list
        dataset = list(lines)
        for x in range(len(dataset) - 1):
            # convert the content to float
            for y in range(len(content_header)):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])






def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


# get k nearest neighbors of the <array><num> testInstance among <array><array>
# trainingSet
def getNeighbors(trainingSet, testInstance, k):
    distance = []
    # minus 1 because we are splitting our data and test also has known class
    length = len(testInstance) - 1

    for x in range((len(trainingSet))):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distance.append((trainingSet[x], dist))
    # sort based on the the item at index 1 i.e the distance
    distance.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distance[x][0])
    return neighbors


# make all responses vote their classification, the one with the highest vote
# wins
def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0


def main():
    iv = ["sepal length", "sepal width", "petal length", "petal width"]
    trainingSet = []
    testSet = []
    # changable values
    split = 0.67
    k = 3
    loadDataset('iris.data', split, trainingSet, testSet, iv)

    # generate predictions
    predictions = []
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        # print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))

    accuracy = getAccuracy(testSet, predictions)

# [5.1, 3.5, 1.4, 0.2, 'Iris-setosa']
# [4.7, 3.2, 1.3, 0.2, 'Iris-setosa']

    print(trainingSet[0])
    print(testSet[0])
    print("Train: " + repr(len(trainingSet)))
    print("Train: " + repr(len(testSet)))
    print('Accuracy: ' + repr(accuracy) + '%')

main()

def getData():
    start = datetime.datetime(2001,1,1)
    end = datetime.date.today()
    apple = web.DataReader('AAPL', 'yahoo', start, end)
    print(type(apple))
    for key in apple:
        print key
    print(apple)

getData()
