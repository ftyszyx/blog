import mysave
from mysave.my_request import MyRequest
class Chentong(MyRequest):
    def __init__(self):
        # 创建session并设置初始登录Cookie
        self.headers = {
            'Referer': 'https://www.lanzous.com',  # 这个必须
            'Accept-Language': 'zh-CN,zh;q=0.9',  # 提取直连必需设置这个，否则拿不到数据
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }

    def download(self,path,url):
        return

    def _parse(self,path,url):
        return