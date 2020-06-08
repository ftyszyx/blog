from requests_html import HTMLSession
from random import shuffle, random, uniform
import re
import json
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
        return int(valuetext)
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
        self.session = HTMLSession()
        #self.session.cookies['BDUSS'] = 'pSb3VsWW5zSm53ajlCdU9FU2RiYlVqMURYb2wwT2UySHRtN1V1bG5Da1pvd1ZkSVFBQUFBJCQAAAAAAAAAAAEAAABGhdQBZnR5c3p5eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkW3lwZFt5cM1'
        #self.session.cookies['STOKEN'] = '132f5312854e7e3f2493aca33390f2fa657d475beabb9a5e4ef5151b0ce79267'
        self.session.proxies["http"]= "http://127.0.0.1:8888"
        self.session.proxies["https"] = "https://127.0.0.1:8888"
        self.session.verify =False # fiddle抓包

        self.headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9',  # 提取直连必需设置这个，否则拿不到数据
            'Referer': 'https://www.lanzous.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }

    def captcha_recognize(self, file_token):
        """识别下载时弹出的验证码,返回下载直链
        :param file_token 文件的标识码,每次刷新会变化
        """
        if not self._captcha_handler:  # 必需提前设置验证码处理函数
            print(f"Not set captcha handler function!")
            return None

        get_img_api = 'https://vip.d0.baidupan.com/file/imagecode.php?r=' + str(random())
        img_data = self.session.get(get_img_api).content
        captcha = self._captcha_handler(img_data)  # 用户手动识别验证码
        post_code_api = 'https://vip.d0.baidupan.com/file/ajax.php'
        post_data = {'file': file_token, 'bm': captcha}
        resp = self.session.post(post_code_api, post_data)
        if not resp or resp.json()['zt'] != 1:
            print("Captcha ERROR:",captcha)
            return None
        print("Captcha PASS:", captcha)
        return resp.json()['url']

    def Download2(self,path,host,ifram):
        framurl = host + ifram.attrs["src"]
        frameres = self.session.get(framurl, headers=self.headers)
        frameres_page = frameres.content.decode("utf-8")
        frameres_page=clearComment(frameres_page)
        #print("frameres_page",frameres_page)
        postdata = getPostJson(frameres_page)
        print("postdata", postdata)
        res = self.session.post(host + "ajaxm.php", headers=self.headers, data=postdata)
        print("get json", res)
        res_json = res.json()
        print("get json:",res_json)
        download_url = res_json["dom"] + "/file/" + res_json["url"]
        print("download_url:",download_url)
        res = self.session.get(download_url, allow_redirects=False)
        res_html = res.content.decode("utf-8")
        if '网络不正常' in res_html:  # 流量异常，要求输入验证码
            file_token = re.findall(r"'file':'(.+?)'", res_html)[0]
            direct_url = self.captcha_recognize(file_token)
        else:
            direct_url = res_html.headers['Location']  # 重定向后的真直链
        #下载
        res=self.session.get(direct_url)
        dirname=os.path.dirname(path)
        if os.path.exists(dirname)==False:
            os.mkdir(dirname)
        with open(path, 'wb') as f:
            f.write(res.content)

    def Download(self,path,url):
        host=re.findall(r'.*lanzous.com\/',url)[0]
        print("get host:",host)
        res = self.session.get(url, headers=self.headers)
        ifram = res.html.find('iframe', first=True)
        if ifram is not None:
            filename=res.html.find('title', first=True).text
            filename=filename.replace("- 蓝奏云","")
            self.Download2(os.path.join(path, filename),host,ifram)
        else:
            res_html = res.content.decode("utf-8")
            res_html=clearComment(res_html)
            postdata=getPostJson(res_html)
            print("get postdata json", postdata)
            res = self.session.post(host+"filemoreajax.php", headers=self.headers, data=postdata)
            res_json = res.json()
            print("get json",res_json)
            infores = res_json['info']
            if infores is None or infores!="sucess":
                return {'errno': 1, "err": infores}
            for item in res_json["text"]:
                id=item["id"]
                res=self.session.get(host + id, headers=self.headers)
                #print(res.content.decode("utf-8"))
                ifram=res.html.find('iframe',first=True)
                filename = res.html.find('title', first=True).text
                filename = filename.replace("- 蓝奏云", "")
                if ifram==None:
                    return {'errno': 1, "err": "ifran not find"}
                print("filename",filename)
                self.Download2(os.path.join(path, filename), host, ifram)

        return {'errno': 0}
