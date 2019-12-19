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

