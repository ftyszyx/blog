import matplotlib.pyplot as plt
import numpy as np

x=np.linspace(0,2,100)


# fig,ax=plt.subplots()
# ax.plot(x,x,label="liner")
# ax.plot(x,x**2,label="quater")
# ax.plot(x,x**3,label="cub")
# ax.legend()# 增加说明
# ax.set_xlabel("xlable")
# ax.set_ylabel("ylabel")
# ax.set_title("simple plot")


# 多个图
# fig,(ax1,ax2)=plt.subplots(1,2)
# plt.ion()
# ax1.plot(x,x**2,label="quart",marker="o")
# ax2.plot(x,x**3,label="cub",marker="x")

#各种图
ax = plt.subplot(111)

t = np.arange(0.0, 5.0, 0.01)
s = np.cos(2*np.pi*t)
line, = plt.plot(t, s, lw=2)

plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )

plt.ylim(-2, 2)
plt.show()