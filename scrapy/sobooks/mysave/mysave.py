# coding="utf-8"
import os

from mysave.baidu import BaiDuPan
from mysave.mylanzou import Lanzou
import pymysql.cursors
import logging

TABLE_TAG="book_tags"
TABLE_TYPE="book_types"
TABLE_BOOK="books"
class Mysave(object):
    all_book_tags = {}
    all_book_types = {}
    def __init__(self):
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
            self.lanzou.log = logging
            result =  self.bai_du_pan.verifyCookie()
            if (result['errno'] != 0):
                logging.error("baidu link error:%s", result)
                return
        except Exception as e:
            if self.cursor is not None and hasattr(self.cursor, "_last_executed"):
                logging.error("nysqlerr:%s", self.cursor._last_executed)
            logging.error("error:%s\n stack:%s", e, repr(e))

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
            logging.error("error:%s\n stack:%s", e, repr(e))

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
            logging.error("error:%s\n stack:%s", e, repr(e))
            return


    def processitem(self,item):
        try:
            baiduurl = item["baidu_url"]
            baiducode = item["baidu_code"]
            typename = self.all_book_types[item["type"]]
            bookname = item["title"]
            chentongurl = item["chentong_url"]
            lanzou_url = item["lanzou_url"]
            if baiduurl!="":
                res =   self.saveBaidu('/sobooks/' + typename,baiduurl,baiducode)
            if lanzou_url != "" and res==False:
                res = self.saveLanzou(os.path.join(os.curdir, typename), lanzou_url)
            if chentongurl != "" and (".lanzous.com" in chentongurl) and res==False:
                res = self.saveLanzou(os.path.join(os.curdir, typename), chentongurl)
        except Exception as e:
            logging.error("error:%s\n stack:%s", e, repr(e))
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