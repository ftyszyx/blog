from requests_html import HTMLSession
from random import shuffle, random, uniform
import pickle
import  os
import mysave.my_help as myhelp
import logging
import wget

class MyRequest():
    def __init__(self):
        # 创建session并设置初始登录Cookie
        self._captcha_handler = None
        self.session = HTMLSession()
        #self.session.packages.urllib3.disable_warnings()  # 屏蔽掉warnming
        self.session.verify = False  # fiddle抓包
        self._host_url = ""
        self.headers = {
            'Referer': 'https://www.lanzous.com',  # 这个必须
            'Accept-Language': 'zh-CN,zh;q=0.9',  # 提取直连必需设置这个，否则拿不到数据
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }

    # 请求
    def _get(self, url, **kwargs):
        kwargs.setdefault('headers', self.headers)
        return self.session.get(url, **kwargs)

    # post
    def _post(self, url, data, **kwargs):
        kwargs.setdefault('headers', self.headers)
        return self.session.post(url, data, **kwargs)


    def un_serialize(self, data: bytes):
        """反序列化文件信息数据"""
        ret = pickle.loads(data)
        if not isinstance(ret, dict):
            return None
        return ret

        # 验证码识别
    def _captcha_recognize(self, file_token):
        """识别下载时弹出的验证码,返回下载直链
        :param file_token 文件的标识码,每次刷新会变化
        """
        if not self._captcha_handler:  # 必需提前设置验证码处理函数
            print(f"Not set captcha handler function!")
            return None

        get_img_api = 'https://vip.d0.baidupan.com/file/imagecode.php?r=' + str(random())
        img_data = self._get(get_img_api).content
        captcha = self._captcha_handler(img_data)  # 用户手动识别验证码
        post_code_api = 'https://vip.d0.baidupan.com/file/ajax.php'
        post_data = {'file': file_token, 'bm': captcha}
        resp = self._post(post_code_api, post_data)
        if not resp or resp.json()['zt'] != 1:
            print("Captcha ERROR:", captcha)
            return None
        print("Captcha PASS:", captcha)
        return resp.json()['url']

    # 下载文件
    def _downloadFile(self, save_path, filename, durl):
        filepath=os.path.join(save_path,filename)
        logging.info("filepath:%s url:%s", filepath, durl)
        if os.path.exists(filepath):
            os.remove(filepath)
        res=wget.download(durl,filepath)
        print("downlode ok:%s",res)
        return myhelp.newSuccess()
        resp = self._get(durl, stream=True)
        if not resp:
            return myhelp.newError("net err")


        total_size = int(resp.headers['Content-Length'])

        file_path = save_path + os.sep + filename
        if os.path.exists(file_path):
            now_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
        else:
            now_size = 0
        chunk_size = 4096
        last_512_bytes = b''  # 用于识别文件是否携带真实文件名信息
        headers = {**self.headers, 'Range': 'bytes=%d-' % now_size}
        resp = self._get(durl, stream=True, headers=headers)

        if resp is None:  # 网络异常
            return myhelp.newError("net err")
        if resp.status_code == 416:  # 已经下载完成
            return myhelp.newSuccess()

        with open(file_path, "ab") as f:
            for chunk in resp.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    now_size += len(chunk)
                    if total_size - now_size < 512:
                        last_512_bytes += chunk
        # 尝试解析文件报尾
        file_info = self.un_serialize(last_512_bytes[-512:])
        if file_info is not None and 'padding' in file_info:  # 大文件的记录文件也可以反序列化出 name,但是没有 padding
            real_name = file_info['name']
            new_file_path = save_path + os.sep + real_name
            if os.path.exists(new_file_path):
                os.remove(new_file_path)  # 存在同名文件则删除
            os.rename(file_path, new_file_path)
            with open(new_file_path, 'rb+') as f:
                f.seek(-512, 2)  # 截断最后 512 字节数据
                f.truncate()
        return myhelp.newSuccess()