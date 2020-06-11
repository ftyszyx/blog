# coding="utf-8"
import traceback

from mysave.mysave import Mysave
import  os

import logging
logfile = open("save.log", encoding="utf-8", mode="a")#防止中文乱码
logging.basicConfig(level=logging.INFO,stream=logfile,format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    save=Mysave()
    if save.int()["errno"]==0:
        save.save()