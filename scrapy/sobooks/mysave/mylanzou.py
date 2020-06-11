from mysave.my_request import MyRequest
import re
import  os
import mysave


class Lanzou(MyRequest):
    def __init__(self):
        # 创建session并设置初始登录Cookie
        self.headers = {
            'Referer': 'https://www.lanzous.com', #这个必须
            'Accept-Language': 'zh-CN,zh;q=0.9',  # 提取直连必需设置这个，否则拿不到数据
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }
    #解析文件页
    def _prase_page(self, page,savepath,pwd=""):
        page_html = page.content.decode("utf-8")
        page_html=mysave.clearComment(page_html)
        passflag=False
        if '密码' in page_html:
            passflag = True
        if passflag==False:
            ifram = page.html.find('iframe', first=True)
            filename = re.search(r"<title>(.+?) - 蓝奏云</title>", page_html) or \
                     re.search(r'<div class="filethetext".+?>([^<>]+?)</div>', page_html) or \
                     re.search(r'<div style="font-size.+?>([^<>].+?)</div>', page_html) or \
                     re.search(r"var filename = '(.+?)';", page_html) or \
                     re.search(r'id="filenajax">(.+?)</div>', page_html) or \
                     re.search(r'<div class="b"><span>([^<>]+?)</span></div>', page_html)
            filename = filename.group(1) if filename else "未匹配到文件名"
            framurl = self._host_url + ifram.attrs["src"]
            frameres = self._get(framurl)
            page_html = frameres.content.decode("utf-8")
            page_html = mysave.clearComment(page_html)
            postdata = mysave.getPostJson(page_html)
        else:
            datastr = mysave.getDataValue(page_html)
            postdata = {
                "action": mysave.getJsValue(datastr, "action"),
                "sign": mysave.getJsValue(datastr, "sign"),
                "p": pwd
            }

        print("postdata", postdata)
        res = self._post(self._host_url + "ajaxm.php",postdata)

        print("get json", res)
        res_json = res.json()
        print("get json:",res_json)
        if passflag == True:
            filename=res_json["inf"]
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
        if direct_url=="":
            return {'errno': 1, "err": "direct_url获取失败"}
        return self._downloadFile(savepath, filename, direct_url)



    #解析
    def _prase(self,path,url,pwd=""):
        if os.path.exists(path)==False:
            os.mkdir(path)
        res = self._get(url)
        res_html = res.content.decode("utf-8")
        res_html = mysave.clearComment(res_html)
        if '密码' in res_html and len(pwd) == 0:
            return {'errno': 1, "err": "需要密码"}
        # 取文件夹名
        dirname = mysave.getJsValue(res_html, "document.title")
        if dirname!="":
            dirname = mysave.getJsValue(res_html, dirname)

        if dirname=="":
            #文件
            result=self._prase_page(res,path,pwd)
            if result["errno"] != 0:
                return result
        else:
            #文件夹
            savepath = os.path.join(path, dirname)
            if os.path.exists(savepath) == False:
                os.mkdir(savepath)
            #是文件夹
            postdata=mysave.getPostJson(res_html)
            print("get postdata json", postdata)
            if '密码' in res_html:  # 文件设置了提取码时
                postdata["pwd"] = pwd
            res = self._post(self._host_url+"filemoreajax.php", postdata)
            res_json = res.json()
            print("get json",res_json)
            infores = res_json['info']
            if infores is None or infores!="sucess":
                return {'errno': 1, "err": infores}
            for item in res_json["text"]:
                id=item["id"]
                result=self._prase(savepath, self._host_url + id, pwd)
                if result["errno"]!=0:
                    return result
        return {'errno': 0}

    def download(self, path, url, pwd=""):
        self._host_url = re.findall(r'.*lanzous.com\/', url)[0]
        print("get host:", self._host_url)
        return self._prase(path, url, pwd)