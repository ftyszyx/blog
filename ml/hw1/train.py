import sys
import pandas as pd
import numpy as np
import  math
data=pd.read_csv("./train.csv",encoding="big5")
data=data.iloc[:,3:]# 取数据
data[data=="NR"]=0
raw_data=data.values#转数组 18

#将数据
#以月为单位
#12个月  每个月20天  一天24小时 ，每小时18个数据
#
#每9小时生成一份data,
#每9小时有18*9个特征，然后这些特征对应一个p2.5的值
#每个月对应471个特征组

#以月为单位操作，所以把数据按月排列先
month_data={}
for month in range(12):
    sample=np.empty([18,480])
    for day in range(20):
        sample[:,day*24:(day+1)*24]=raw_data[18*(20*month+day):18*(20*month+day+1),:]
    month_data[month]=sample

#生成x和y
x=np.empty([12*471,18*9],dtype=float)
y=np.empty([12*471,1],dtype=float)
for month in range(12):
    for day in range(20):
        for hour in range(24):
            if day==19 and hour>14: #day和hour都是从0开始
                continue
            row = month*471+day*24+hour
            #第n行是把当前小时+9小时的数据取出来，按照特征1*小时1 特征1*小时2
            x[row,:]=month_data[month][:,day*24+hour:day*24+hour+9].reshape(1,-1)#
            y[row,0]=month_data[month][9,day*24+hour+9]#值

#print(x)
#对x的特征做归一化，u=0
meanx=np.mean(x,axis=0)
std_x=np.std(x,axis=0)
for i in range(len(x)):
    for j in range(len(x[0])):
        if std_x[j]!=0:
            x[i][j]=(x[i][j]-meanx[j])/std_x[j]


#将数据分成训练和测试数据
x_train_set=x[:math.floor(len(x)*0.8),:]
y_train_set=y[:math.floor(len(y)*0.8),:]
x_validation=x[math.floor(len(x)*0.8):,:]
y_validation=y[math.floor(len(y)*0.8):,:]

#开始训练
#y=wx+b==>