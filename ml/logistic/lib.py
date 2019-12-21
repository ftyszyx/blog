from math import *
from numpy import *

def sigmoid(inx):
    return 1.0/(1+exp(-inx))

def gradAscent(dataMatIn,classLables):
    dataMatrix=mat(dataMatIn)
    labelMat=mat(classLables).transpose()
    m,n=shape(dataMatrix)
    alpha=0.001
    maxCycles=500
    weights=ones((n,1))
    for k in range(maxCycles):
        h=sigmoid(dataMatrix*weights)
        error=labelMat-h
        weights=weights+alpha*dataMatrix.transpose()*error
    return weights

def stocGradAscent(dataMatrix,classLabels):
    m,n=shape(dataMatrix)
    alpha=0.01
    weights=ones(n)
    for i in range(m):
        h=sigmoid(sum(dataMatrix[i]*weights))
        error = classLabels - h
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights


def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix)
    weights = ones(n)
    #print(weights,type(weights))
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in dataIndex:
            alpha = 4/(1.0+j+i)+0.01
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            datain=array(dataMatrix[randIndex])
            #print(datain, type(datain))
            weights = weights + alpha * error * datain
            del(dataIndex[randIndex])
    return weights
