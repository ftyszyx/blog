# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
class SobooksPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipline(object):
    alltags={}
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
        if (spider.name == "sobooks" or spider.name=="sotag"):
            with self.connect.cursor() as cursor:
                cursor.execute("""
                select * from tags
                """)
                results=cursor.fetchall()
                for row in results:
                    self.alltags[row[1]]=row[0]
                self.connect.commit()
                spider.logger.info("get alltags",self.alltags)

    def getbooktag(self,tags):
        arr=tags.split(' ')
        tagids=[]
        for tagname in arr:
            tagids.append(self.alltags[tagname])
        return ",".join(tagids)

    def process_item(self, item, spider):
        spider.logger.info("%s process_item:%s", spider.name,item)
        if(spider.name=="sobooks"):
            with self.connect.cursor() as cursor:
                cursor.execute(
                    """insert into books (title, desc, author, type, img, baidu_url, baidu_code,isbn,tags)
                    value (%s, %s,%s, %s,%s, %s,%s, %s,%s)""",
                    (item['title'], item['desc'], item['author'], item['type'], item['img'],
                     item['baidu_url'],item['baidu_code'],item['isbn'],self.getbooktag(item["tag"])))
                # 提交sql语句
                self.connect.commit()
        elif(spider.name=="sotag"):
            tagname=item['name']
            if tagname in self.alltags:
                spider.logger.info("tag exit:%s",tagname)
            else:
                with self.connect.cursor() as cursor:
                    cursor.execute("""insert into tags (name) value (%s) """,(tagname))
                    # 提交sql语句
                    self.connect.commit()
        return  item