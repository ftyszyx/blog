# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymysql.cursors
from sobooks.items import TagsItem
class SobooksPipeline(object):
    def process_item(self, item, spider):
        return item

TABLE_TAG="book_tags"
TABLE_TYPE="book_types"
TABLE_BOOK="books"

class MysqlPipline(object):
    all_book_tags={}
    all_book_types={}
    def open_spider(self,spider):
        # 连接数据库
        sqlsetting=spider.settings.get("MYSQL_SETTING")
        spider.logger.info("%s connect mysql:%s",spider.name,sqlsetting)
        self.connect = pymysql.connect(
            host=sqlsetting["host"],  # 数据库地址
            port=sqlsetting["port"],  # 数据库端口
            db=sqlsetting["db"],  # 数据库名
            user=sqlsetting["user"],  # 数据库用户名
            passwd=sqlsetting["passwd"],  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)

        if(self.connect==None):
            spider.logger.error("connect mysql err")
        # 通过cursor执行增删查改
        if (spider.name == "sobook" or spider.name=="sotag"or spider.name=="sobooktype"):
            with self.connect.cursor() as cursor:
                cursor.execute(""" select * from {} """.format(TABLE_TAG))
                results=cursor.fetchall()
                for row in results:
                    self.all_book_tags[row[1]]=row[0]
                self.connect.commit()
                spider.logger.info("get all_book_types:%s",self.all_book_tags)

            with self.connect.cursor() as cursor:
                cursor.execute(""" select * from {} """.format(TABLE_TYPE))
                results=cursor.fetchall()
                for row in results:
                    self.all_book_types[row[1]]=row[0]
                self.connect.commit()
                spider.logger.info("get alltags:%s", self.all_book_types)


    def addOneType(self,item):
        typename = item['name']
        with self.connect.cursor() as cursor:
            cursor.execute("""insert into {} (name) value (%s) """.format(TABLE_TYPE), (typename))
            # 提交sql语句
            self.connect.commit()

    def addOneTag(self, item):
        tagname = item['name']
        with self.connect.cursor() as cursor:
            cursor.execute("""insert into {} (name) value (%s) """.format(TABLE_TAG), (tagname))
            # 提交sql语句
            self.connect.commit()


    def geturl(self,url):
        if url.startswith("https://sobooks.cc/go.html?url="):
            return url.replace("https://sobooks.cc/go.html?url=","").strip()
        return url

    def addOneBook(self,item):
        baiduurl = self.geturl(item.get('baidu_url', ''))
        baidu_code = item.get('baidu_code', '')
        isbn = item.get('isbn', '')
        lanzou_url = self.geturl(item.get('lanzou_url', ''))
        chentong_url = self.geturl(item.get('chentong_url', ''))
        tagstr = self.getbooktag(item["tag"])
        typestr = self.get_book_types(item["type"])
        imgstr=item.get("img","")
        desc = item.get('desc', '')
        title=item.get('title','')
        author = item.get('author', '')
        try:
            with self.connect.cursor() as cursor:
                cursor.execute("""select * from {} where `title`=%s and `author`=%s """.format(TABLE_BOOK), (title,author))
                # 提交sql语句
                results = cursor.fetchone()
                if results is None:
                    cursor.execute(
                        """insert into {} (title, intro_text, author, type, img, baidu_url, baidu_code,isbn,tags,lanzou_url,chentong_url)
                        value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(TABLE_BOOK),
                        (title, desc,author, typestr, imgstr, baiduurl, baidu_code, isbn, tagstr,
                         lanzou_url, chentong_url))
                else:
                    print('book exit')
                # 提交sql语句
                self.connect.commit()
                #scrapy.Item.get()
        except Exception as e:
            print("nysqlerr:",cursor._last_executed)
            raise scrapy.exceptions.CloseSpider(reason='sqlerr')

    #获取tag
    def getbooktag(self,tags):
        arr=tags.split(',')
        tagids=[]
        for tagname in arr:
            if tagname in self.all_book_tags:
                tagids.append(self.all_book_tags[tagname])
            else:
                tagitem=TagsItem()
                tagitem["name"]=tagname
                self.addOneTag(tagitem)
                with self.connect.cursor() as cursor:
                    cursor.execute("""select * from {} where `name`=%s""".format(TABLE_TAG), (tagname))
                    # 提交sql语句
                    results = cursor.fetchone()
                    tagid=results[0]
                    tagids.append(tagid)
                    self.all_book_tags[tagname] =tagid
                    self.connect.commit()
        return ",".join([str(a) for a in tagids])

    def get_book_types(self,book_type):
        if book_type in self.all_book_types:
            return self.all_book_types[book_type]
        raise scrapy.exceptions.CloseSpider(reason='book_type {} not exit'.format(book_type))

    def process_item(self, item, spider):
        spider.logger.info("%s process_item:%s", spider.name,item)
        if(spider.name=="sobook"):
            self.addOneBook(item)
        elif(spider.name=="sotag"):
            tagname=item['name']
            if tagname in self.all_book_tags:
                spider.logger.info("tag exit:%s",tagname)
            else:
                self.addOneTag(item)
        elif (spider.name == "sobooktype"):
            typename = item['name']
            if typename in self.all_book_types:
                spider.logger.info("type exit:%s", typename)
            else:
                self.addOneType(item)
        return  item