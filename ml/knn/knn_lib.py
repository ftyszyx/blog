# coding: utf-8
# 处理
import matplotlib
import matplotlib.pyplot as plt
from numpy import *
import operator
import os


# 每年获得的飞行常客里程数
# 玩视频游戏所耗时间百分比
# 每周消费的冰淇淋公升数

# 标签
# 不喜欢的人
# 魅力一般的人
# 极具魅力的人




# 归一化
def auto_norm(dataset):
    """
    Desc:
        归一化特征值，消除特征之间量级不同导致的影响
    parameter:
        data_set: 数据集
    return:
        归一化后的数据集 normDataSet. ranges和minVals即最小值与范围，并没有用到

    归一化公式：
        Y = (X-Xmin)/(Xmax-Xmin)
        其中的 min 和 max 分别是数据集中的最小特征值和最大特征值。该函数可以自动将数字特征值转化为0到1的区间。
    """
    # 计算每种属性的最大值、最小值、范围
    min_val = dataset.min(0)  # axie=0的
    max_val = dataset.max(0)
    # 极差
    ranges = max_val - min_val
    normal_data = zeros(shape(dataset))
    m = dataset.shape[0]
    # 生成与最小值之差组成的矩阵
    normal_data = dataset - tile(min_val, (m, 1))
    # 将最小值之差除以范围组成矩阵
    normal_data = normal_data / tile(ranges, (m, 1))  # element wise divide
    return normal_data, ranges, min_val


# 分类
def classify0(src_data, data_set, labels, k):
    data_size = data_set.shape[0]
    # 距离度量 度量公式为欧氏距离
    diff_mat = tile(src_data, (data_size, 1)) - data_set
    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances ** 0.5
    # 将距离排序：从小到大
    sorted_dist_dic = distances.argsort()
    # 选取前K个最短距离， 选取这K个中最多的分类类别
    class_count = {}
    for i in range(k):
        vote_label = labels[sorted_dist_dic[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


