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
    lastitem=None
    default_savepath="G:\\book"
    def __init__(self):
        return

    def init(self):
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
                logging.info("all_book_tags:%s",self.all_book_tags)

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


    def getallItem(self,tag=None):

        if tag is not None:
            self.cursor.execute(""" select COUNT(*) from {} where saveok=0 and tags like '%{}%' """.format(TABLE_BOOK,tag))
        else:
            self.cursor.execute(
                """ select COUNT(*) from {} where saveok=0 """.format(TABLE_BOOK))
        results = self.cursor.fetchone()
        num = int(results["COUNT(*)"])
        if tag is not None:
            logging.info("总数量:%s tag:%s",num,self.all_book_tags[tag])
        else:
            logging.info("总数量:%s ", num)
        perpagenum = 10
        page = int(num / perpagenum + 1)
        for pageindex in range(1,page):
            start=(pageindex-1)*perpagenum
            if tag is not None:
                self.cursor.execute(""" select * from {} where saveok=0 and tags like '%{}%' limit {},{} """.format(TABLE_BOOK,tag,start,perpagenum))
            else:
                self.cursor.execute(
                    """ select * from {} where saveok=0  limit {},{} """.format(TABLE_BOOK,start, perpagenum))
            results = self.cursor.fetchall()
            for item in results:
                 yield item

    def save(self,tag=None):
        item_itr=self.getallItem(tag)
        try:
            with self.connect.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                self.cursor = cursor
                while True:
                    self.lastitem = next(item_itr, None)
                    if self.lastitem  is None:
                        return
                    if self.processitem(self.lastitem )==True:
                        cursor.execute(""" update {} set `saveok`=1 where `id`=%s """.format(TABLE_BOOK), self.lastitem ["id"])
                        self.connect.commit()
        except Exception as e:
            if self.cursor is not None and hasattr(self.cursor, "_last_executed"):
                logging.error("last sql:%s", self.cursor._last_executed)
            if self.lastitem is not None:
                self.lastitem["intro_text"]=""
                logging.info("self.lastitem：%s",self.lastitem )
            logging.exception(e)
            return


    def processitem(self,item):
        res=False
        baiduurl = item["baidu_url"]
        baiducode = item["baidu_code"]
        typename = self.all_book_types[item["type"]]
        chentongurl = item["chentong_url"]
        lanzou_url = item["lanzou_url"]
        bookname=item["title"]
        if lanzou_url != "" :
            res = self.saveLanzou(os.path.join(self.default_savepath, typename), lanzou_url,bookname,"")
        if chentongurl != "" and res==False:
            if  ".lanzous.com" in chentongurl:
                res = self.saveLanzou(os.path.join(self.default_savepath, typename), chentongurl,bookname,"")
            else:
                res = self.saveChenTong(os.path.join(self.default_savepath, typename), chentongurl,bookname)
        if baiduurl != "" and res==False :
            res = self.saveBaidu('/sobooks/' + typename, baiduurl,bookname, baiducode)
        return res

    def saveLanzou(self,path,url,bookname,code):
        res = self.lanzou.download(path, url,code)
        if (res['errno'] == 0):
            logging.info('蓝奏保存成功:path:%s bookname:%s url:%s', path,bookname, url)
            return True
        else:
            logging.info('蓝奏保存失败:path:%s url:%s bookname:%s err:%s', path, bookname,url,res)
            return False
    def saveBaidu(self,path,url,bookname,code):
        res = self.bai_du_pan.saveShare(url,code,path)
        if (res['errno'] == 0):
            logging.info('百度保存成功:path:%s bookname:%s url:%s', path,bookname, url)
            return True
        else:
            logging.info('百度保存失败:path:%s bookname:%s url:%s err:%s', path, bookname,url,res)
            return False

    def saveChenTong(self,path,url,bookname):
        res =  self.chentong.download( path,url)
        if (res['errno'] == 0):
            logging.info('城通保存成功:path:%s bookname:%s url:%s', path, bookname,url)
            return True
        else:
            logging.info('城通保存失败:path:%s bookname:%s url:%s err:%s', path,bookname, url,res)
            return False