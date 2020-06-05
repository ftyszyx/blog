# coding="utf-8"

import sys
sys.path.append('/home/meetup/Desktop/BaiDuPan')
from BaiDuPan import BaiDuPan
from DbOperate import DbOperate
import time

def startSave():
	db_operate = DbOperate()
	unsave_list = db_operate.getUnSave()
	bai_du_pan = BaiDuPan()
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '开始执行保存至百度网盘')
	for hifini in unsave_list:
		try:
			result = bai_du_pan.saveShare(hifini.pan_url, hifini.pan_pwd, '/hifini.com/%s' % hifini.type)
		except Exception as e:
			result = {'errno': -1}
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '其他保存异常（ID：', hifini.id, '）: ', e)
		if(result['errno'] == 0):
			db_operate.update(hifini.id, 1, 1)
			if(result['errno'] > 0):
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '百度网盘分享链接有问题（ID：', id, '）: ', e)
		else:
			db_operate.update(hifini.id, 0, 0)
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '全部执行完成！')


if __name__ == '__main__':
	startSave()