import csv
import random
import math

# split the data into a training dataset and test dataset in ratio of 67/33
def loadDataset(filename, split, trainingSet=[], testSet=[]):
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
            for y in range(len(iv)):
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

data1 = [2,3,4,'s']
data2 = [4,4,4,'b']
distance = euclideanDistance(data1, data2, 3)
print(repr(distance))


iv = ["sepal length", "sepal width", "petal length", "petal width"]
trainingSet = []
testSet = []
loadDataset('iris.data', 0.66, trainingSet, testSet)

print("Train: " + repr(len(trainingSet)))
print("Train: " + repr(len(testSet)))
