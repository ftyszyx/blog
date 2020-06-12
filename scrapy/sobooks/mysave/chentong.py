import mysave.my_help as myhelp
import re
import random
import os
import json
from mysave.my_request import MyRequest
#城通下文件有限制，每次只能下一个
class Chentong(MyRequest):
    def __init__(self):
        super(Chentong, self).__init__()
        # 创建session并设置初始登录Cookie
        self.headers = {
            "Accept": "application/json,text/javascript,*/*;q=0.01",
            'Accept-Language': 'zh-CN,zh;q=0.9',  # 提取直连必需设置这个，否则拿不到数据
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }

    def download(self,path,url):
        if os.path.exists(path)==False:
            os.mkdir(path)

        if "dir" in url:
            #文件夹
            res=self._get(url)
            url=res.url

            re_res = re.search(r'/([^/]*$)', url)
            query = re_res.group(1)
            re_res = re.findall(r'^https://[^/]*', url)
            self.orgin = re_res[0]

            res_html = res.content.decode("utf-8")

            re_res = re.search(r'src=\"([^"]*/js/other\.js[^"]*)\"', res_html)
            js_url = re_res.group(1)
            js_html=self._get(js_url).content.decode("utf-8")

            self._host_url=myhelp.getJsValue(js_html,"api_server").replace('"',"")
            headers = {**self.headers, 'Referer': url,"Origin":self.orgin}
            dirjson=self._get(self._host_url+"/getdir.php?d=" + query + "&folder_id=" + "&passcode=""&r=" +str(random.random()) + "&ref=",headers=headers)
            dirjson=dirjson.content.decode("utf-8-sig")
            dirjson=json.loads(dirjson)
            dirname=dirjson["folder_name"]
            savepath=os.path.join(path,dirname)
            if os.path.exists(savepath)==False:
                os.mkdir(savepath)
            filelist_json=self._get(self._host_url+dirjson["url"])
            filelist_json = filelist_json.content.decode("utf-8-sig")
            filelist_json = json.loads(filelist_json)
            for item in filelist_json["aaData"]:
                itemhtml=item[1]
                re_res = re.search(r'href=\"([^"]*)', itemhtml)
                item_url = re_res.group(1)
                #re_res = re.search(r'<a[^<>]*>([^<>]*)</a>', itemhtml)
                #item_name = re_res.group(1)
                result=self._parse_file(savepath,self.orgin+item_url)
                if result["errno"]!=0:
                    return result
            return myhelp.newSuccess()
        else:
            #文件
            return self._parse_file(path,url)

    def _parse_file(self,path,url):

        res = self._get(url)

        url=res.url
        re_res = re.findall(r'^https://[^/]*', url)
        self.orgin = re_res[0]
        re_res = re.search(r'/([^/]*$)', url)
        query = re_res.group(1)

        res_html = res.content.decode("utf-8")
        re_res = re.search(r'src=\"([^"]*/js/other\.js[^"]*)\"', res_html)
        js_url = re_res.group(1)
        js_html = self._get(js_url).content.decode("utf-8")
        self._host_url = myhelp.getJsValue(js_html, "api_server").replace('"',"")
        headers = {**self.headers, 'Referer': url, "Origin": self.orgin}
        filejson = self._get(self._host_url + "/getfile.php?f=" + query +  "&passcode=""&r=" +str(random.random()) + "&ref=",headers=headers)
        filejson = filejson.content.decode("utf-8-sig")
        filejson = json.loads(filejson)
        if filejson["code"]!=200:
            return myhelp.newError("json错误",filejson)
        filename = filejson["file_name"]
        file_chk=filejson["file_chk"]
        file_id = filejson["file_id"]
        userid = filejson["userid"]
        foldid=0
        headers = {**self.headers, 'Referer': url, "Origin": self.orgin}
        downjson=self._get(self._host_url + "/get_file_url.php?uid=" + str(userid) + "&fid=" + str(file_id) + "&folder_id=" +str(foldid)+
                  "&file_chk=" + str(file_chk) + "&mb=0&app=0&acheck=1&verifycode=&rd="+ str(random.random()),headers=headers)
        downjson = downjson.content.decode("utf-8-sig")
        downjson = json.loads(downjson)
        if downjson["code"]==200:
            return self._downloadFile(path, filename, downjson["downurl"])
        else:
            return myhelp.newError("返回错误",downjson)


