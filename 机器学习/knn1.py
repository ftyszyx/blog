#coding: utf-8
from numpy import *
from os import listdir
import  operator
from collections import Counter


#处理数据 返回数量和对应标签
def file2matrix(filename):
    fr=open(filename)
    numberOfLines=len(fr.readlines())
    returnMat=zeros(numberOfLines,3)
    classLabelVector=[]
    index=0
    for line in fr.readlines():
        line=line.strip()
        listfromline=line.split('\t')
        returnMat[index,:]=listfromline[0:3]
        classLabelVector.append(int(listfromline[-1]))
        index+=1
    return returnMat,classLabelVector

#分析数据

