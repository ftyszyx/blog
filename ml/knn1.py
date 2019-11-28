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

# 处理数据 返回数量和对应标签
def file2matrix(filename):
    fr = open(filename)
    lines = fr.readlines()
    number_of_lines = len(lines)
    return_mat = zeros((number_of_lines, 3))
    label_vector = []
    index = 0
    for line in lines:
        line = line.strip()
        list_of_line = line.split('\t')
        return_mat[index, :] = list_of_line[0:3]
        label_vector.append(int(list_of_line[-1]))
        index += 1
    return return_mat, label_vector


# 归一化
def auto_norm(dataset):
    """
    Desc:
        归一化特征值，消除特征之间量级不同导致的影响
    parameter:
        dataSet: 数据集
    return:
        归一化后的数据集 normDataSet. ranges和minVals即最小值与范围，并没有用到

    归一化公式：
        Y = (X-Xmin)/(Xmax-Xmin)
        其中的 min 和 max 分别是数据集中的最小特征值和最大特征值。该函数可以自动将数字特征值转化为0到1的区间。
    """
    # 计算每种属性的最大值、最小值、范围
    min_val = dataset.min(0) # axie=0的
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


# 分析数据
if __name__ == "__main__":
    data_mat, dataLabels = file2matrix("./data/datingTestSet2.txt")
    normMat, ranges, minVals = auto_norm(data_mat)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # x ,y 横坐标  纵坐标  圆的大小  颜色
    ax.scatter(data_mat[:, 0], data_mat[:, 1], 15.0 * array(dataLabels), 15.0 * array(dataLabels))
    plt.show()
