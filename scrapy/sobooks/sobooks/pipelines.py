# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymysql.cursors
class SobooksPipeline(object):
    def process_item(self, item, spider):
        return item


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
        if (spider.name == "sobooks" or spider.name=="sotag"or spider.name=="sobooktype"):
            with self.connect.cursor() as cursor:
                cursor.execute(""" select * from book_tags """)
                results=cursor.fetchall()
                for row in results:
                    self.all_book_tags[row[1]]=row[0]
                self.connect.commit()
                spider.logger.info("get all_book_types:%s",self.all_book_tags)

            with self.connect.cursor() as cursor:
                cursor.execute(""" select * from book_types """)
                results=cursor.fetchall()
                for row in results:
                    self.all_book_types[row[1]]=row[0]
                self.connect.commit()
                spider.logger.info("get alltags:%s", self.all_book_types)

    #获取tag
    def getbooktag(self,tags):
        arr=tags.split(' ')
        tagids=[]
        for tagname in arr:
            tagids.append(self.all_book_tags[tagname])
        return ",".join(tagids)

    def get_book_types(self,book_type):
        if book_type in self.all_book_types:
            return self.all_book_types[book_type]
        raise scrapy.exceptions.CloseSpider(reason='book_type {} not exit'.format(book_type))

    def process_item(self, item, spider):
        spider.logger.info("%s process_item:%s", spider.name,item)
        if(spider.name=="sobooks"):
            with self.connect.cursor() as cursor:
                cursor.execute(
                    """insert into books (title, desc, author, type, img, baidu_url, baidu_code,isbn,tags,lanzou_url,chentong_url)
                    value (%s, %s,%s, %s,%s, %s,%s, %s,%s)""",
                    (item['title'], item['desc'], item['author'], self.get_book_types(item['type']), item['img'],
                     item['baidu_url'],item['baidu_code'],item['isbn'],self.getbooktag(item["tag"],item['lanzou_url'],item['chentong_url'])))
                # 提交sql语句
                self.connect.commit()
        elif(spider.name=="sotag"):
            tagname=item['name']
            if tagname in self.all_book_tags:
                spider.logger.info("tag exit:%s",tagname)
            else:
                with self.connect.cursor() as cursor:
                    cursor.execute("""insert into book_tags (name) value (%s) """,(tagname))
                    # 提交sql语句
                    self.connect.commit()
        elif (spider.name == "sobooktype"):
            typename = item['name']
            if typename in self.all_book_types:
                spider.logger.info("type exit:%s", typename)
            else:
                with self.connect.cursor() as cursor:
                    cursor.execute("""insert into book_types (name) value (%s) """, (typename))
                    # 提交sql语句
                    self.connect.commit()
        return  item