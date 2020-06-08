# coding="utf-8"

from baidu import BaiDuPan
from mylanzou import Lanzou
import pymysql.cursors
from lanzou2.api import LanZouCloud
import  os
TABLE_TAG="book_tags"
TABLE_TYPE="book_types"
TABLE_BOOK="books"
import logging
logfile = open("save.log", encoding="utf-8", mode="a")#防止中文乱码
logging.basicConfig(level=logging.INFO,stream=logfile,format='%(asctime)s - %(levelname)s - %(message)s')

def testLanzou():
	lanzou=Lanzou()
	lanzou.log=logging

	#lanzou.Download(os.path.join(os.curdir,"test"),"https://sobooks.lanzous.com/iHOaHdcmsyj")
	#print(lanzou.Download(os.path.join(os.curdir, "test"), "https://sobooks.lanzous.com/b03mtamna"))
	print(lanzou.Download(os.path.join(os.curdir, "test"), "https://ob1.lanzous.com/icilhdg","109131"))

	#lzy = LanZouCloud()
	#lzy.down_file_by_url("https://sobooks.lanzous.com/b03mtamna","",os.path.join(os.curdir, "test"))
	#lzy.down_dir_by_url("https://sobooks.lanzous.com/b03mtamna", "", os.path.join(os.curdir, "test"))

def startSave():

	all_book_tags = {}
	all_book_types = {}
	try:
		connect = pymysql.connect(
			host='127.0.0.1',  # 数据库地址
			port=3306,  # 数据库端口
			db='sobooks',  # 数据库名
			user='root',  # 数据库用户名
			passwd='',  # 数据库密码
			charset='utf8',  # 编码方式
			use_unicode=True)

		with connect.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
			#初始化百度网盘
			bai_du_pan = BaiDuPan()
			lanzou = Lanzou()
			lanzou.log = logging
			result = bai_du_pan.verifyCookie()

			if (result['errno'] != 0):
				logging.error("baidu link error:%s", result)
				return

			cursor.execute(""" select * from {} """.format(TABLE_TAG))
			results = cursor.fetchall()
			for row in results:
				all_book_tags[row["id"]] = row["name"]

			cursor.execute(""" select * from {} """.format(TABLE_TYPE))
			results = cursor.fetchall()
			for row in results:
				all_book_types[row["id"]] = row["name"]

			cursor.execute(""" select COUNT(*) from {} where saveok=0""".format(TABLE_BOOK))
			results = cursor.fetchone()
			num=int(results["COUNT(*)"])
			perpagenum=10
			page=int(num/perpagenum+1)

			for pageindex in range(1,page):
				start=(pageindex-1)*perpagenum;
				cursor.execute(""" select * from {} where saveok=0 limit {},{} """.format(TABLE_BOOK,start,perpagenum))
				results = cursor.fetchall()
				for item in results:
					baiduurl=item["baidu_url"]
					baiducode = item["baidu_code"]
					typename=all_book_types[item["type"]]
					bookname=item["title"]
					chentongurl = item["chentong_url"]
					lanzou_url = item["lanzou_url"]


					result = bai_du_pan.saveShare(baiduurl, baiducode, '/sobooks/'+typename)
					if (result['errno'] == 0):
						logging.info('保存成功:typename:%s bookname:%s', typename,bookname)
						cursor.execute(""" update {} set `saveok`=1 where `id`=%s """.format(TABLE_BOOK),item["id"])
						connect.commit()
					else:
						logging.error('百度保存失败:typename:%s bookname:%s url:%s code:%s err:%s', typename, bookname,baiduurl,baiducode,result)
						if lanzou_url != "":
							lanzou.Download(os.path.join(os.curdir, typename), lanzou_url)
						elif chentongurl!="" and (".lanzous.com" in chentongurl):
							lanzou.Download(os.path.join(os.curdir, typename), chentongurl)




	except Exception as e:
		if cursor is not None and hasattr(cursor,"_last_executed"):
			logging.error("nysqlerr:%s", cursor._last_executed)
		logging.error("error:%s\n stack:%s",e,repr(e))
	logging.info('全部执行完成！')


if __name__ == '__main__':
	testLanzou()
	#startSave()