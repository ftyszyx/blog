# coding="utf-8"
import traceback

from mysave.mysave import Mysave
import  os

import logging
logfile = open("save.log", encoding="utf-8", mode="a")#防止中文乱码
logging.basicConfig(level=logging.INFO,stream=logfile,format='%(asctime)s - %(levelname)s - %(message)s')

def testLanzou():
    lanzou=Lanzou()
    lanzou.log=logging

    #文件（不要密码）
    lanzou.Download(os.path.join(os.curdir, "test"), "https://wws.lanzous.com/iY1rEdjrw4f")
    # lanzou.Download(os.path.join(os.curdir,"test"),"https://wws.lanzous.com/iu3RBdj33eh")
    # 文件夹（不要密码）
    #lanzou.Download(os.path.join(os.curdir, "test"), "https://wws.lanzous.com/b01bgsveh")

    # 文件(要密码）
    #lanzou.Download(os.path.join(os.curdir, "test"), "https://wws.lanzous.com/iMPDUdj38xg","38t0")
    #文件夹(要密码）
    #res=lanzou.Download(os.path.join(os.curdir, "test"), "https://wws.lanzous.com/b01bgsvdg","e3oz")
    # if res["errno"]!=0:
    # 	msg = traceback.format_exc()  # 方式1
    # 	print(msg)

if __name__ == '__main__':
    #testLanzou()
    save=Mysave()
    save.save()