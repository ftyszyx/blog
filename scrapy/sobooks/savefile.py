# coding="utf-8"
from mysave.mysave import Mysave
import sys
import urllib3

import logging

#输出到pinmu
root = logging.getLogger()
logfile = open("save.log", encoding="utf-8", mode="a")#防止中文乱码
logging.basicConfig(level=logging.INFO,stream=logfile,format='%(asctime)s - %(levelname)s - %(message)s')
printhandle = logging.StreamHandler(sys.stdout)
printhandle.setLevel(logging.INFO)
root.addHandler(printhandle)
if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    save=Mysave()
    res=save.init()
    if res["errno"]==0:
        save.save()