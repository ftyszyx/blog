

import os

libs = {"wget", "requests_html","pickle","pymysql","scrapy"}

try:
    for lib in libs:
        os.system("pip install " + lib)
    print("successful")
except:
    print("failed somehow")