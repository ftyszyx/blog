# coding: utf-8
from math import log
import operator

#计算信息商
def calc_cannon_ent(dataset):
    # 求list的长度，表示计算参与训练的数据量
    num_entries = len(dataset)
    # 计算分类标签label出现的次数
    label_counts = {}
    # the the number of unique elements and their occurrence
    for featVec in dataset:
        # 将当前实例的标签存储，即每一行数据的最后一个数据代表的是标签
        current_label = featVec[-1]
        # 为所有可能的分类创建字典，如果当前的键值不存在，则扩展字典并将当前键值加入字典。每个键值都记录了当前类别出现的次数。
        if current_label not in label_counts.keys():
            label_counts[current_label] = 0
        label_counts[current_label] += 1

    # 对于 label 标签的占比，求出 label 标签的香农熵
    shannon_ent = 0.0
    for key in label_counts:
        # 使用所有类标签的发生频率计算类别出现的概率。
        prob = float(label_counts[key]) / num_entries
        # 计算香农熵，以 2 为底求对数
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent

def split_data_set(data_set, index, value):
    """
    Desc：
        划分数据集
        splitDataSet(通过遍历dataSet数据集，求出index对应的colnum列的值为value的行)
        就是依据index列进行分类，如果index列的数据等于 value的时候，就要将 index 划分到我们创建的新的数据集中
    Args:
        dataSet  -- 数据集                 待划分的数据集
        index -- 表示每一行的index列        划分数据集的特征
        value -- 表示index列对应的value值   需要返回的特征的值。
    Returns:
        index 列为 value 的数据集【该数据集需要排除index列】
    """
    # -----------切分数据集的第一种方式 start------------------------------------
    ret_data_set = []
    for featVec in data_set:
        # index列为value的数据集【该数据集需要排除index列】
        # 判断index列的值是否为value
        if featVec[index] == value:
            # chop out index used for splitting
            # [:index]表示前index行，即若 index 为2，就是取 featVec 的前 index 行
            reducedFeatVec = featVec[:index]
            reducedFeatVec.extend(featVec[index+1:])
            # [index+1:]表示从跳过 index 的 index+1行，取接下来的数据
            # 收集结果值 index列为value的行【该行需要排除index列】
            ret_data_set.append(reducedFeatVec)
    # -----------切分数据集的第一种方式 end------------------------------------

    # # -----------切分数据集的第二种方式 start------------------------------------
    # retDataSet = [data[:index] + data[index + 1:] for data in dataSet for i, v in enumerate(data) if i == index and v == value]
    # # -----------切分数据集的第二种方式 end------------------------------------
    return ret_data_set

#获取最好的分节点
def choose_best_feature_Split(dataset):
    """chooseBestFeatureToSplit(选择最好的特征)
    Args:
        dataset 数据集
    Returns:
        bestFeature 最优的特征列
    """
    # 求第一行有多少列的 Feature, 最后一列是label列嘛
    num_features = len(dataset[0]) - 1
    # 数据集的原始信息熵
    base_entropy = calc_cannon_ent(dataset)
    # 最优的信息增益值, 和最优的Featurn编号
    best_info_gain, best_feature = 0.0, -1
    # iterate over all the features
    for i in range(num_features):
        # create a list of all the examples of this feature
        # 获取对应的feature下的所有数据
        feat_list = [example[i] for example in dataset]
        # get a set of unique values
        # 获取剔重后的集合，使用set对list数据进行去重
        unique_val = set(feat_list)
        # 创建一个临时的信息熵
        new_entropy = 0.0
        # 遍历某一列的value集合，计算该列的信息熵
        # 遍历当前特征中的所有唯一属性值，对每个唯一属性值划分一次数据集，计算数据集的新熵值，并对所有唯一特征值得到的熵求和。
        for value in unique_val:
            sub_data_set = split_data_set(dataset, i, value)
            # 计算概率
            prob = len(sub_data_set)/float(len(dataset))
            # 计算信息熵
            new_entropy += prob * calc_cannon_ent(sub_data_set)
        # gain[信息增益]: 划分数据集前后的信息变化， 获取信息熵最大的值
        # 信息增益是熵的减少或者是数据无序度的减少。最后，比较所有特征中的信息增益，返回最好特征划分的索引值。
        info_gain = base_entropy - new_entropy
        print('infoGain=', info_gain, 'bestFeature=', i, base_entropy, new_entropy)
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature

def majorityCnt(classList):
    """
    Desc:
        选择出现次数最多的一个结果
    Args:
        classList label列的集合
    Returns:
        bestFeature 最优的特征列
    """
    # -----------majorityCnt的第一种方式 start------------------------------------
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    # 倒叙排列classCount得到一个字典集合，然后取出第一个就是结果（yes/no），即出现次数最多的结果
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # print('sortedClassCount:', sortedClassCount)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]#获取结果
    if classList.count(classList[0]) == len(classList):# 所有的结果都是一样的
        return classList[0]
    if len(dataSet[0]) == 1:  #没有条件，只有结果列，取结果出现最多的传为最终结果
        return majorityCnt(classList)

    # 选择最优的列，得到最优列对应的label含义
    bestFeat = choose_best_feature_Split(dataSet)
    # 获取label的名称
    bestFeatLabel = labels[bestFeat]
    # 初始化myTree
    myTree = {bestFeatLabel: {}}
    # 注：labels列表是可变对象，在PYTHON函数中作为参数时传址引用，能够被全局修改
    # 所以这行代码导致函数外的同名变量被删除了元素，造成例句无法执行，提示'no surfacing' is not in list
    del(labels[bestFeat])
    # 取出最优列，然后它的branch做分类
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        # 求出剩余的标签label
        subLabels = labels[:]
        # 遍历当前选择特征包含的所有属性值，在每个数据集划分上递归调用函数createTree()
        myTree[bestFeatLabel][value] = createTree(split_data_set(dataSet, bestFeat, value), subLabels)
        # print 'myTree', value, myTree
    return myTree

def classify(inputTree, featLabels, testVec):
    """classify(给输入的节点，进行分类)

    Args:
        inputTree  决策树模型
        featLabels Feature标签对应的名称
        testVec    测试输入的数据
    Returns:
        classLabel 分类的结果值，需要映射label才能知道名称
    """
    # 获取tree的根节点对于的key值
    firstStr = inputTree.keys()[0]
    # 通过key得到根节点对应的value
    secondDict = inputTree[firstStr]
    # 判断根节点名称获取根节点在label中的先后顺序，这样就知道输入的testVec怎么开始对照树来做分类
    featIndex = featLabels.index(firstStr)
    # 测试数据，找到根节点对应的label位置，也就知道从输入的数据的第几位来开始分类
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    print('+++', firstStr, 'xxx', secondDict, '---', key, '>>>', valueOfFeat)
    # 判断分枝是否结束: 判断valueOfFeat是否是dict类型
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        classLabel = valueOfFeat
    return classLabel