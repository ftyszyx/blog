import sys
import pandas as pd
import numpy as np
data=pd.read_csv("./train.csv",encoding="big5")

data=data.iloc[:,3:]
data[data=='NR']=0
raw_data=data.values

month_data={}
#一个月20天*24小时，有18个数据项
#相当于一个月480小时
for month in range(12):
    sample=np.empty([18,480])
    for day in range(20):
        sample[:,day*24:(day+1)*24]=raw_data[18 * (20 * month + day) : 18 * (20 * month + day + 1), :]
    month_data[month]=sample
#每個月會有 480hrs，每 9 小時形成一個 data，每個月會有 471 個 data，故總資料數為 471 * 12 筆，而每筆 data 有 9 * 18 的 features (一小時 18 個 features * 9 小時)。
#對應的 target 則有 471 * 12 個(第 10 個小時的 PM2.5)
x = np.empty([12 * 471, 18 * 9], dtype = float)
y = np.empty([12 * 471, 1], dtype = float)
for month in range(12):
    for day in range(20):
        for hour in range(24):
            if day == 19 and hour > 14:
                continue
            x[month * 471 + day * 24 + hour, :] = month_data[month][:,day * 24 + hour : day * 24 + hour + 9].reshape(1, -1) #vector dim:18*9 (9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9)
            y[month * 471 + day * 24 + hour, 0] = month_data[month][9, day * 24 + hour + 9] #value
print(x)
print(y)


mean_x = np.mean(x, axis = 0) #18 * 9
std_x = np.std(x, axis = 0) #18 * 9
for i in range(len(x)): #12 * 471
    for j in range(len(x[0])): #18 * 9
        if std_x[j] != 0:
            x[i][j] = (x[i][j] - mean_x[j]) / std_x[j]
x