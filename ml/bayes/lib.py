#!/usr/bin/python
# -*- coding:utf-8 -*-
from numpy import *
def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him','to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute','I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how','to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec

def createVocabList(dataset):
    vocabSet=set([])
    for document in dataset:
        vocabSet=vocabSet|set(document)
    return list(vocabSet)

# conver sentense to verctor
def setOfWords2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print("the word:%s is not in my vocabulary" % word)
    return returnVec

def bagOfWords2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec

# trainmatrix:all document verctor   trainCategory:class result
def trainNB0(trainmatrix,trainCategory):
    numTrainDocs=len(trainmatrix)
    numWords=len(trainmatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    p0Num=ones(numWords)
    p0Denom=2.0
    p1Num=ones(numWords)
    p1Denom=2.0
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            p1Num+=trainmatrix[i]
            p1Denom+=sum(trainmatrix[i])
        else:
            p0Num += trainmatrix[i]
            p0Denom += sum(trainmatrix[i])
    p1vect=log(p1Num/p1Denom) #in class 1 the word appear probability
    p0vect = log(p0Num / p0Denom)#in class 0 the word appear probability
    return p0vect,p1vect,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


