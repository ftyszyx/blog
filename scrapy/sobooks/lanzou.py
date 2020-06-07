from requests_html import HTMLSession
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

def getJsValue(html,key):
    regex= re.compile(r"\n[^\/]*%s[\s]*=[\s]*(\'*[^;\']*\'*);" % key)
    find_res = re.search(regex, html)
    valuetext=find_res.group(1)
    if valuetext.startswith("'")==False:
        return int(valuetext)
    return str(valuetext.replace("'",""))


def getDictFromJson(html,json):
    data={}
    find_res = re.findall(r'\'([^,\']*)\':(\'*[^\']*\'*),', json)
    for item in find_res:
        key_str=item[0]
        value_str=item[1]
        if value_str.startswith("'")==False:
            if(is_number(item[1])):
                data[key_str]=int(value_str)
            else:
                data[key_str] = getJsValue(html,value_str)
        else:
            data[key_str]=str(value_str)
    return data

class Lanzou(object):
    def __init__(self):
        # 创建session并设置初始登录Cookie
        self.session = HTMLSession()
        #self.session.cookies['BDUSS'] = 'pSb3VsWW5zSm53ajlCdU9FU2RiYlVqMURYb2wwT2UySHRtN1V1bG5Da1pvd1ZkSVFBQUFBJCQAAAAAAAAAAAEAAABGhdQBZnR5c3p5eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkW3lwZFt5cM1'
        #self.session.cookies['STOKEN'] = '132f5312854e7e3f2493aca33390f2fa657d475beabb9a5e4ef5151b0ce79267'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }

    def Download2(self,path,host,ifram):
        framurl = host + ifram.attrs["src"]
        frameres = self.session.get(framurl, headers=self.headers)
        frameres_page = frameres.content.decode("utf-8")
        #print(frameres_page)
        cots=getJsValue(frameres_page,"cots")
        print("get cots",cots)
        postdata = {
            'action': 'downprocess',
            'sign': cots,
            'ves': 1
        }
        res = self.session.post(host + "ajaxm.php", headers=self.headers, data=postdata)
        #print("get json", res)
        res_json = res.json()
        print("get json:",res_json)
        download_url = res_json["dom"] + "/file/" + res_json["url"]
        print("download_url:",download_url)
        res = self.session.get(download_url)
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
            find_res=re.search(r'data \:[^{}]*(\{[^}]*\})',res_html)
            postdata_str=find_res.group(1)
            postdata=getDictFromJson(res_html,postdata_str)
            #print("get postdata", eval(postdata_str)) 处理不了字符串不带引号的情况
            #postdata = json.loads(postdata_str)  处理不掉单引号的情况
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
