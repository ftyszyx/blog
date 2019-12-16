# coding: utf-8
from math import log
import operator
import pickle

#get shannon
def calShannonEnt(dataSet):
    numEntries=len(dataSet)
    # get all label count
    labelCounts={}
    for feat_vec in dataSet:
        current_label=feat_vec[-1]
        if current_label not in labelCounts.keys():
            labelCounts[current_label]=0
        labelCounts[current_label]+=1
    shannon=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        shannon -= prob*log(prob,2)
    return shannon

#split value
def splitDataSet(dataset,axis,value):
    retDataSet=[]
    for featVec in dataset:
        if featVec[axis]==value:
            reduceFeatVec=featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet

# split to get remain shannon value minest
def chooseBestFeatureToSplit(dataset):
    numFeature=len(dataset[0])-1
    baseEntropy=calShannonEnt(dataset)
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numFeature):
        featList=[example[i] for example in dataset]
        uniqueVals=set(featList)
        newEntropy=0
        for value in uniqueVals:
            subdataSet=splitDataSet(dataset,i,value)
            prob =len(subdataSet)/float(len(dataset))
            newEntropy+=prob*calShannonEnt(subdataSet)
        infoGain=baseEntropy-newEntropy
        if infoGain>bestInfoGain:
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

# get the most num class
def majorityCnt(classList):
    classcount={}
    for vote in classList:
        if vote not in classcount.keys():
            classcount[vote]=0
        classcount[vote]+=1
    sortedClassCount=sorted(classcount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]


def createTree(dataset,labels):
    classList=[example[-1] for example in dataset]
    #all class is same
    if classList.count(classList[0])==len(classList):
        return classList[0]
    ## only one feature
    if len(dataset[0])==1:
        return  majorityCnt(classList)
    bestFeature=chooseBestFeatureToSplit(dataset)
    bestFeatureLabel=labels[bestFeature]
    myTree={bestFeatureLabel:{}}
    del(labels[bestFeature])
    featureValues=[example[bestFeature] for example in dataset]
    uniqueValues=set(featureValues)
    for value in uniqueValues:
        sublabels=labels[:]
        myTree[bestFeatureLabel][value]=createTree(splitDataSet(dataset,bestFeature,value),sublabels)
    return myTree

def storeTree(inputTree,filename):
    fw=open(filename,'wb')
    pickle.dump(inputTree,fw)
    fw.close()

def gradTree(filename):
    fr=open(filename,'rb')
    return pickle.load(fr)
