# coding: utf-8
import  sys
sys.path.append(r'../../')
import ml.decisiontree.treelib as treelib;
import ml.decisiontree.decisionTreePlot as dtPlot

def ContactLensesTest():
    """
    Desc:
        预测隐形眼镜的测试代码，并将结果画出来
    Args:
        none
    Returns:
        none
    """

    # 加载隐形眼镜相关的 文本文件 数据
    fr = open('../data/tree/lenses.txt')
    # 解析数据，获得 features 数据
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    # 得到数据的对应的 Labels
    #数据对应的标签
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    # 使用上面的创建决策树的代码，构造预测隐形眼镜的决策树
    lensesTree = treelib.createTree(lenses, lensesLabels)
    print(lensesTree)
    # 画图可视化展现
    dtPlot.createPlot(lensesTree)


if __name__ == "__main__":
    # fishTest()
    ContactLensesTest()