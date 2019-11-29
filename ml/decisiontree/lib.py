# coding: utf-8
from math import log

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
    bestInfoGain, bestFeature = 0.0, -1
    # iterate over all the features
    for i in range(num_features):
        # create a list of all the examples of this feature
        # 获取对应的feature下的所有数据
        featList = [example[i] for example in dataset]
        # get a set of unique values
        # 获取剔重后的集合，使用set对list数据进行去重
        uniqueVals = set(featList)
        # 创建一个临时的信息熵
        newEntropy = 0.0
        # 遍历某一列的value集合，计算该列的信息熵
        # 遍历当前特征中的所有唯一属性值，对每个唯一属性值划分一次数据集，计算数据集的新熵值，并对所有唯一特征值得到的熵求和。
        for value in uniqueVals:
            subDataSet = splitDataSet(dataset, i, value)
            # 计算概率
            prob = len(subDataSet)/float(len(dataset))
            # 计算信息熵
            newEntropy += prob * calcShannonEnt(subDataSet)
        # gain[信息增益]: 划分数据集前后的信息变化， 获取信息熵最大的值
        # 信息增益是熵的减少或者是数据无序度的减少。最后，比较所有特征中的信息增益，返回最好特征划分的索引值。
        infoGain = base_entropy - newEntropy
        print 'infoGain=', infoGain, 'bestFeature=', i, base_entropy, newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
