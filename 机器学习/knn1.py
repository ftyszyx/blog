#coding: utf-8
import matplotlib
import matplotlib.pyplot as plt
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
if __name__=="__main__":

    datamat,labels=file2matrix("./data/datingTestSet2.txt")
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()

