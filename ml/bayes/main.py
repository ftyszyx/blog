import  sys
from numpy import *
import  re
sys.path.append(r'../../')
import ml.bayes.lib as bayeslib

# email spam
def textParse(bigString):
    listofTokens=re.split(r'\W*',bigString)
    return [tok.lower() for tok in listofTokens if len(tok)>2]


def spamTest():
    docList=[]
    classList=[]
    fullText=[]
    for i in range(1,26):
        wordList=textParse(open('./data/email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('./data/email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=bayeslib.createVocabList(docList)


    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])

    trainMat = [];
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bayeslib.setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])

    p0V, p1V, pSpam = bayeslib.trainNB0((trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bayeslib.setOfWords2Vec(vocabList, docList[docIndex])
        if bayeslib.classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            print('   error : ' )
            errorCount += 1
    print('the error rate is: ', float(errorCount) / len(testSet))

if __name__ == "__main__":
    #
    # listposts,listClass=bayeslib.loadDataSet()
    # myVocabList=bayeslib.createVocabList(listposts)
    # trainmat=[]
    # for post in listposts:
    #     trainmat.append(bayeslib.setOfWords2Vec(myVocabList,post))
    # p0v,p1v,pab=bayeslib.trainNB0(trainmat,listClass)
    # testEntry=['love','my','dalmation']
    # thisdoc=array(bayeslib.setOfWords2Vec(myVocabList,testEntry))
    # print(
    #     "{0} classified as :{1}".format(thisdoc,bayeslib.classifyNB(thisdoc,p0v,p1v,pab))
    # )


    spamTest()

