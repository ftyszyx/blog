# coding="utf-8"
import os

from mysave.baidu import BaiDuPan
from mysave.mylanzou import Lanzou
from mysave.chentong import Chentong
import pymysql.cursors
import logging
import mysave.my_help as myhelp

TABLE_TAG="book_tags"
TABLE_TYPE="book_types"
TABLE_BOOK="books"
class Mysave(object):
    all_book_tags = {}
    all_book_types = {}
    def __init__(self):
        return

    def int(self):
        try:
            self.connect = pymysql.connect(
                host='127.0.0.1',  # 数据库地址
                port=3306,  # 数据库端口
                db='sobooks',  # 数据库名
                user='root',  # 数据库用户名
                passwd='',  # 数据库密码
                charset='utf8',  # 编码方式
                use_unicode=True)
            with self.connect.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                self.cursor=cursor
                # 初始化百度网盘
                self.cursor.execute(""" select * from {} """.format(TABLE_TAG))
                results = self.cursor.fetchall()
                for row in results:
                    self.all_book_tags[row["id"]] = row["name"]

                self.cursor.execute(""" select * from {} """.format(TABLE_TYPE))
                results = self.cursor.fetchall()
                for row in results:
                    self.all_book_types[row["id"]] = row["name"]

            self.bai_du_pan = BaiDuPan()
            self.lanzou = Lanzou()
            self.chentong=Chentong()
            result =  self.bai_du_pan.verifyCookie()
            if (result['errno'] != 0):
                logging.error("baidu link error:%s", result)
                return result
        except Exception as e:
            if self.cursor is not None and hasattr(self.cursor, "_last_executed"):
                logging.error("nysqlerr:%s", self.cursor._last_executed)
            logging.exception(e)
            return myhelp.newError("错误")
        return myhelp.newSuccess()


    def getallItem(self):
        try:
            with self.connect.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                self.cursor = cursor
                self.cursor.execute(""" select COUNT(*) from {} where saveok=0""".format(TABLE_BOOK))
                results = cursor.fetchone()
                num = int(results["COUNT(*)"])
                perpagenum = 10
                page = int(num / perpagenum + 1)
                for pageindex in range(1,page):
                    start=(pageindex-1)*perpagenum;
                    cursor.execute(""" select * from {} where saveok=0 limit {},{} """.format(TABLE_BOOK,start,perpagenum))
                    results = cursor.fetchall()
                    for item in results:
                         yield item

        except Exception as e:
            if self.cursor is not None and hasattr(self.cursor, "_last_executed"):
                logging.error("nysqlerr:%s", self.cursor._last_executed)
            logging.exception(e)

    def save(self):
        item_itr=self.getallItem()
        try:
            with self.connect.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                while True:
                    item = next(item_itr, None)
                    if item is None:
                        return
                    if self.processitem(item)==True:
                        cursor.execute(""" update {} set `saveok`=1 where `id`=%s """.format(TABLE_BOOK), item["id"])
                        self.connect.commit()
        except Exception as e:
            logging.exception(e)
            return


    def processitem(self,item):
        res=False
        try:
            baiduurl = item["baidu_url"]
            baiducode = item["baidu_code"]
            typename = self.all_book_types[item["type"]]
            chentongurl = item["chentong_url"]
            lanzou_url = item["lanzou_url"]
            if lanzou_url != "" :
                res = self.saveLanzou(os.path.join(os.curdir, typename), lanzou_url)
            if chentongurl != "" and res==False:
                if  ".lanzous.com" in chentongurl:
                    res = self.saveLanzou(os.path.join(os.curdir, typename), chentongurl)
                else:
                    res = self.saveChenTong(os.path.join(os.curdir, typename), chentongurl)
            if baiduurl != "" and res==False :
                res = self.saveBaidu('/sobooks/' + typename, baiduurl, baiducode)
        except Exception as e:
            logging.exception(e)
            return False
        return res

    def saveLanzou(self,path,url,code=""):
        res = self.lanzou.Download(path, url,code)
        if (res['errno'] == 0):
            logging.info('蓝奏保存成功:path:%s url:%s', path, url)
            return True
        else:
            logging.info('蓝奏保存失败:path:%s url:%s err:%s', path, url,res)
            return False
    def saveBaidu(self,path,url,code):
        res = self.bai_du_pan.saveShare(url,code,path)
        if (res['errno'] == 0):
            logging.info('百度保存成功:path:%s url:%s', path, url)
            return True
        else:
            logging.info('百度保存失败:path:%s url:%s err:%s', path, url,res)
            return False

    def saveChenTong(self,path,url):
        res =  self.chentong.download( path,url)
        if (res['errno'] == 0):
            logging.info('城通保存成功:path:%s url:%s', path, url)
            return True
        else:
            logging.info('城通保存失败:path:%s url:%s err:%s', path, url,res)
            return False