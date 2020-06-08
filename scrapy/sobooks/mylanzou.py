from requests_html import HTMLSession
from random import shuffle, random, uniform
import re
import pickle
import  os
def is_number(str):
    try:
        # 因为使用float有一个例外是'NaN'
        if str=='NaN':
            return False
        int(str)
        return True
    except ValueError:
        return False

def clearComment(text):
    find_res = re.findall(r'//[^\n]*', text)
    if len(find_res) > 0:
        for item in find_res:
            text = text.replace(item, "//")
    return text

def getPostJson(text):
    find_res = re.search(r'data \:[^{}]*(\{[^}]*\})', text)
    postdata_str = find_res.group(1)
    postdata = getDictFromJson(text, postdata_str)
    return postdata

def getJsValue(text,key):
    regex= re.compile(r"%s[\s]*=[\s]*(\'*[^;\'\}]*\'*);" % key)
    find_res = re.search(regex, text)
    if find_res is None:
        print("key not find:",key,text)
    valuetext=find_res.group(1)
    if valuetext.startswith("'")==False:
        if (is_number(valuetext)):
            return int(valuetext)
        else:
            return valuetext
    return str(valuetext.replace("'",""))


def getDictFromJson(html,json):
    data={}
    find_res = re.findall(r'\'([^,\'\}]*)\':(\'*[^\',\}]*\'*)', json)
    for item in find_res:
        key_str=item[0]
        value_str=item[1]
        if value_str.startswith("'")==False:
            if(is_number(item[1])):
                data[key_str]=int(value_str)
            else:
                data[key_str] = getJsValue(html,value_str)
        else:
            data[key_str]=value_str.replace("'","")
    return data



class Lanzou(object):
    def __init__(self):
        # 创建session并设置初始登录Cookie
        self._captcha_handler = None
        self.log=None
        self.session = HTMLSession()
        self.session.verify =False # fiddle抓包
        self._host_url=""
        self.headers = {
            'Referer': 'https://www.lanzous.com', #这个必须
            'Accept-Language': 'zh-CN,zh;q=0.9',  # 提取直连必需设置这个，否则拿不到数据
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }

    def _get(self, url, **kwargs):
        try:
            kwargs.setdefault('headers', self.headers)
            return self.session.get(url,  **kwargs)
        except Exception as e:
            self.log.error("error:%s\n stack:%s",e,repr(e))
            return None

    def _post(self, url, data, **kwargs):
        try:
            kwargs.setdefault('headers', self.headers)
            return self.session.post(url, data,  **kwargs)
        except Exception as e:
            self.log.error("error:%s\n stack:%s", e, repr(e))
            return None

    def un_serialize(self,data: bytes):
        """反序列化文件信息数据"""
        try:
            ret = pickle.loads(data)
            if not isinstance(ret, dict):
                return None
            return ret
        except Exception as e:  # 这里可能会丢奇怪的异常
            self.log.error("error:%s\n stack:%s", e, repr(e))
            return None

    #验证码识别
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
            print("Captcha ERROR:",captcha)
            return None
        print("Captcha PASS:", captcha)
        return resp.json()['url']

    def _downloadFile(self,save_path,filename,durl):
        resp = self._get(durl, stream=True)
        if not resp:
            return {'errno': 1, "err": "net err"}
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
            return {'errno': 1, "err": "net err"}
        if resp.status_code == 416:  # 已经下载完成
            return {'errno': 0}

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
        return {'errno': 0}

    #获取真实地址
    def _getFileUrl(self, url):
        frameres = self._get(url )
        frameres_page = frameres.content.decode("utf-8")
        frameres_page=clearComment(frameres_page)
        postdata = getPostJson(frameres_page)
        print("postdata", postdata)
        res = self._post(self._host_url + "ajaxm.php",postdata)
        print("get json", res)
        res_json = res.json()
        print("get json:",res_json)
        download_url = res_json["dom"] + "/file/" + res_json["url"]
        res = self._get(download_url,allow_redirects=False)
        res_html = res.content.decode("utf-8")
        print("res_html",res_html)
        if '网络不正常' in res_html:  # 流量异常，要求输入验证码
            file_token = re.findall(r"'file':'(.+?)'", res_html)[0]
            direct_url = self._captcha_recognize(file_token)
        else:
            direct_url = res.headers['Location']  # 重定向后的真直链
        print("direct_url:",direct_url)
        return direct_url

    def Download(self,path,url):
        if os.path.exists(path)==False:
            os.mkdir(path)
        self._host_url=re.findall(r'.*lanzous.com\/',url)[0]
        print("get host:",self._host_url)
        res = self._get(url)
        ifram = res.html.find('iframe', first=True)
        if ifram is not None:
            filename=res.html.find('title', first=True).text
            filename=filename.replace("- 蓝奏云","")
            framurl =  self._host_url + ifram.attrs["src"]
            durl=self._getFileUrl(framurl)
            if durl is None:
                return {'errno': 1, "err": "durl获取失败"}
            return self._downloadFile(path,filename,durl)
        else:
            #是文件夹
            res_html = res.content.decode("utf-8")
            res_html=clearComment(res_html)
            #取文件夹名
            dirname=getJsValue(res_html,"document.title")
            dirname=getJsValue(res_html, dirname)
            savepath=os.path.join(path,dirname)
            if os.path.exists(savepath)==False:
                os.mkdir(savepath)
            postdata=getPostJson(res_html)
            print("get postdata json", postdata)
            res = self._post(self._host_url+"filemoreajax.php", postdata)
            res_json = res.json()
            print("get json",res_json)
            infores = res_json['info']
            if infores is None or infores!="sucess":
                return {'errno': 1, "err": infores}
            for item in res_json["text"]:
                id=item["id"]
                res=self._get(self._host_url + id)
                ifram=res.html.find('iframe',first=True)
                filename = res.html.find('title', first=True).text
                filename = filename.replace("- 蓝奏云", "")
                if ifram==None:
                    return {'errno': 1, "err": "ifran not find"}
                print("filename",filename)
                framurl = self._host_url + ifram.attrs["src"]
                durl=self._getFileUrl(framurl)
                if durl is None:
                    return {'errno': 1, "err": "durl获取失败"}
                result=self._downloadFile(savepath,filename,durl)
                if result["errno"]!=0:
                    return result
        return {'errno': 0}
