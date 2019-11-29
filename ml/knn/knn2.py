# coding: utf-8
from numpy import *
import os
import knn_lib


# 手写数字识别系统
# 将文本转成向量
def img2vector(filename):
    return_vector = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        line_str = fr.readline()
        for j in range(32):
            return_vector[0, 32 * i + j] = int(line_str[j])
    return return_vector


def handwriting_class_test():
    # 1. 导入训练数据
    hw_labels = []
    training_file_list = os.listdir('data/knn/trainingDigits')  # load the training set
    m = len(training_file_list)
    training_mat = zeros((m, 1024))
    # hwLabels存储0～9对应的index位置， trainingMat存放的每个位置对应的图片向量
    for i in range(m):
        file_name_str = training_file_list[i]
        file_str = file_name_str.split('.')[0]  # take off .txt
        class_num_str = int(file_str.split('_')[0])
        hw_labels.append(class_num_str)
        # 将 32*32的矩阵->1*1024的矩阵
        training_mat[i, :] = img2vector('data/knn/trainingDigits/%s' % file_name_str)

    # 2. 导入测试数据
    test_file_list = os.listdir('data/knn/testDigits')  # iterate through the test set
    error_count = 0.0
    m_test = len(test_file_list)
    for i in range(m_test):
        file_name_str = test_file_list[i]
        file_str = file_name_str.split('.')[0]  # take off .txt
        class_num_str = int(file_str.split('_')[0])
        vector_under_test = img2vector('data/knn/testDigits/%s' % file_name_str)
        classifier_result = knn_lib.classify0(vector_under_test, training_mat, hw_labels, 3)
        if classifier_result != class_num_str:
            print("the classifier came back with: %d, the real answer is: %d filename:%s" % (classifier_result, class_num_str,file_name_str))
            error_count += 1.0
    print("\nthe total number of errors is: %d" % error_count)
    print("\nthe total error rate is: %f" % (error_count / float(m_test)))


# 分析数据
if __name__ == "__main__":
    handwriting_class_test()