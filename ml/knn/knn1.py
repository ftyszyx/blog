# coding: utf-8
# 处理
import knn_lib
from numpy import *



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

def dating_class_test():
    """
    约会网站测试
    :return:
    """
    hoRatio = 0.1
    # 从文件中加载数据
    dating_data_mat, dating_labels = file2matrix('data/knn/datingTestSet2.txt')  # load data setfrom file
    # 归一化数据
    norm_mat, ranges, min_vals = knn_lib.auto_norm(dating_data_mat)
    # m 表示数据的行数，即矩阵的第一维
    m = norm_mat.shape[0]
    # 设置测试的样本数量， numTestVecs:m表示训练样本的数量
    num_test_vecs = int(m * hoRatio)
    print('numTestVector=', num_test_vecs)
    error_count = 0.0
    for i in range(num_test_vecs):
        # 对数据测试
        classifier_result = knn_lib.classify0(norm_mat[i, :], norm_mat[num_test_vecs:m, :], dating_labels[num_test_vecs:m], 3)
        if classifier_result != dating_labels[i]:
            print("the classifier came back with: %d, the real answer is: %d" % (classifier_result, dating_labels[i]))
            error_count += 1.0
    print("the total error rate is: %f" % (error_count / float(num_test_vecs)))
    print("the total error count is: %d" % error_count)


# 分析数据
if __name__ == "__main__":
    dating_class_test()