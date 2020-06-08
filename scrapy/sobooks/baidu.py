# coding="utf-8"

from requests_html import HTMLSession
import re
import json
import time

class BaiDuPan(object):
    def __init__(self):
        # 创建session并设置初始登录Cookie
        self.session = HTMLSession()
        self.session.cookies['BDUSS'] = 'pSb3VsWW5zSm53ajlCdU9FU2RiYlVqMURYb2wwT2UySHRtN1V1bG5Da1pvd1ZkSVFBQUFBJCQAAAAAAAAAAAEAAABGhdQBZnR5c3p5eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkW3lwZFt5cM1'
        self.session.cookies['STOKEN'] = '132f5312854e7e3f2493aca33390f2fa657d475beabb9a5e4ef5151b0ce79267'

        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }

    '''
    验证Cookie是否已登录
    返回值errno代表的意思：
    0 有效的Cookie；1 init方法中未配置登录Cookie；2 无效的Cookie
    '''

    def verifyCookie(self):
        if (self.session.cookies['BDUSS'] == '' or self.session.cookies['STOKEN'] == ''):
            return {'errno': 1, 'err_msg': '请在init方法中配置百度网盘登录Cookie'}
        else:
            response = self.session.get('https://pan.baidu.com/disk/home?', headers=self.headers)
            html=response.content.decode("utf-8")
            username_re=re.findall(r'username\":\"([^\"]+)\"', html)
            user_name = username_re[0]
            if user_name is not None:
                return {'errno': 0, 'err_msg': '有效的Cookie，用户名：%s' % user_name}
            else:
                return {'errno': 2, 'err_msg': '无效的Cookie！'}


    '''
    验证加密分享
    返回值errno代表的意思：
    0 加密分享验证通过；1 验证码获取失败；2 提取码不正确；3 加密分享验证失败；4 重试几次后，验证码依旧不正确；
    '''

    def verifyShare(self, surl, bdstoken, pwd, referer):
        '''
        构造密码验证的URL：https://pan.baidu.com/share/verify?
        surl=62yUYonIFdKGdAaueOkyaQ  从重定向后的URL中获取
        &t=1572356417593  时间戳
        &channel=chunlei  固定值
        &web=1  固定值
        &app_id=250528  固定值
        &bdstoken=742aa0d6886423a5503bbc67afdb2a7d  从重定向后的页面中可以找到，有时候会为空，经过验证，不要此字段也可以
        &logid=MTU0ODU4MzUxMTgwNjAuNDg5NDkyMzg5NzAyMzY1MQ==  不知道什么作用，暂时为空或者固定值都可以
        &clienttype=0  固定值
        '''
        t = str(int(time.time()) * 1000)
        url = 'https://pan.baidu.com/share/verify?surl=%s&t=%s&channel=chunlei&web=1&app_id=250528&bdstoken=%s\
				&logid=MTU0ODU4MzUxMTgwNjAuNDg5NDkyMzg5NzAyMzY1MQ==&clienttype=0' % (surl, t, bdstoken)
        form_data = {
            'pwd': pwd,
            'vcode': '',
            'vcode_str': '',
        }
        headers = self.headers
        headers['referer'] = referer
        verify_res = self.session.post(url, headers=headers, data=form_data)
        verify_json = verify_res.json()
        errcode=verify_json['errno']
        if (errcode == 0):
            return {'errno': 0}
        else:
            return {'errno': errcode, 'err': verify_json}


    '''
    返回值errno代表的意思：
    0 转存成功；1 无效的分享链接；2 分享文件已被删除；
    3 分享文件已被取消；4 分享内容侵权，无法访问；5 找不到文件；6 分享文件已过期
    7 获取提取码失败；8 获取加密cookie失败； 9 转存失败；
    '''

    def saveShare(self, url, pwd=None, path='/'):
        share_res = self.session.get(url, headers=self.headers)
        share_page = share_res.content.decode("utf-8")
        if ('error/404.html' in share_res.url):
            return {"errno": 1, "err":"无效的分享链接"}
        if ('你来晚了，分享的文件已经被删除了，下次要早点哟' in share_page):
            return {"errno": 2, "err": "分享文件已被删除"}
        if ('你来晚了，分享的文件已经被取消了，下次要早点哟' in share_page):
            return {"errno": 3, "err": "分享文件已被取消"}
        if ('此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问' in share_page):
            return {"errno": 4, "err": "分享内容侵权，无法访问"}
        if ('链接错误没找到文件，请打开正确的分享链接' in share_page):
            return {"errno": 5, "err": "链接错误没找到文件"}
        if ('啊哦，来晚了，该分享文件已过期' in share_page):
            return {"errno": 6, "err": "分享文件已过期"}

        # 提取码校验的请求中有此参数
        bdstoken = re.findall(r'bdstoken\":\"(.+?)\"', share_page)
        if bdstoken is None or len(bdstoken)==0:
            return {"errno": 6, "err": "未知原因"}
        bdstoken = bdstoken[0]
        # 如果加密分享，需要验证提取码，带上验证通过的Cookie再请求分享链接，即可获取分享文件
        if ('init' in share_res.url):
            surl = re.findall(r'surl=(.+?)$', share_res.url)[0]
            referer = share_res.url
            verify_result = self.verifyShare(surl, bdstoken, pwd, referer)
            if (verify_result['errno'] != 0):
                return {"errno": verify_result['errno'], "err": verify_result }
            else:
                # 加密分享验证通过后，使用全局session刷新页面（全局session中带有解密的Cookie）
                share_res = self.session.get(url, headers=self.headers)
                share_page = share_res.content.decode("utf-8")
        share_data = json.loads(re.search("yunData.setData\(({.*})\)", share_page).group(1))
        bdstoken = share_data['bdstoken']
        shareid = share_data['shareid']
        _from = share_data['uk']
        '''
        构造转存的URL，除了logid不知道有什么用，但是经过验证，固定值没问题，其他变化的值均可在验证通过的页面获取到
        '''
        save_url = 'https://pan.baidu.com/share/transfer?shareid=%s&from=%s&ondup=newcopy&async=1&channel=chunlei&web=1&app_id=250528&bdstoken=%s\
					&logid=MTU3MjM1NjQzMzgyMTAuMjUwNzU2MTY4MTc0NzQ0MQ==&clienttype=0' % (shareid, _from, bdstoken)
        file_list = share_data['file_list']['list']
        form_data = {
            # 这个参数一定要注意，不能使用['fs_id', 'fs_id']，谨记！
            'fsidlist': '[' + ','.join([str(item['fs_id']) for item in file_list]) + ']',
            'path': path,
        }
        headers = self.headers
        headers['Origin'] = 'https://pan.baidu.com'
        headers['referer'] = url
        '''
        用带登录Cookie的全局session请求转存
        如果有同名文件，保存的时候会自动重命名：类似xxx(1)
        暂时不支持超过文件数量的文件保存
        '''
        save_res = self.session.post(save_url, headers=headers, data=form_data)
        save_json = save_res.json()
        errno=save_json['errno']
        if errno==0:
            return {'errno': errno}
        else:
            return {'errno': errno,"err":save_json}
