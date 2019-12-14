import  sys
sys.path.append(r'../../')
import ml.decisiontree.mytreelib as mytreelib
import ml.decisiontree.treeplot_lib as treeplot

def createDataSet():
    dataset=[[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataset,labels


if __name__ == "__main__":
     mydat,labels=createDataSet()
     mytree=mytreelib.createTree(mydat,labels)
     treeplot.createPlot()