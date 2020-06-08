import scrapy
from sobooks.items import BooksItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import json
#返回403：https://assets.hcaptcha.com/captcha/v1/32b4a85/hcaptcha.min.js
#https://hcaptcha.com/getcaptcha
#set cookie:__cfduid=dec7479479b26e5d6cee874a0e98622081591265743; expires=Sat, 04-Jul-20 10:15:43 GMT; path=/; domain=.hcaptcha.com; HttpOnly; SameSite=Lax; Secure

#读取book
class authorspider(scrapy.Spider):
    name = "sobook"
    #start_urls = ['https://sobooks.cc/']
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }
    }
    def start_requests(self):
        urls=['https://sobooks.cc/xiaoshuowenxue',
              'https://sobooks.cc/lishizhuanji',
              'https://sobooks.cc/renwensheke',
              'https://sobooks.cc/lizhichenggong',
              'https://sobooks.cc/jingjiguanli',
              'https://sobooks.cc/xuexijiaoyu',
              'https://sobooks.cc/shenghuoshishang',
              'https://sobooks.cc/yingwenyuanban',
        ]
        #cookie={'cookie':'__cfduid=decf3f7387e8f965b3b3374b97c3597e81591265730; UM_distinctid=1727ed4f41233-0e5192d707c6b1-f7d1d38-2a3000-1727ed4f413395; __gads=ID=ac9c45f7f76d4c0c:T=1591265784:S=ALNI_MblTn46PW05HdaEw7TOYp9aSjd2Bg; cf_clearance=e6f01f37b3db605188f632dc65926f5fa63515cb-1591326191-0-250; CNZZDATA1259444303=212689518-1591264504-https%253A%252F%252Fsobooks.cc%252F%7C1591325024'}
        #cookie={'cookie':'__cfduid=d4247258b9b4f26cd1ad523106d6523291591275840;UM_distinctid=1727f6c79291-0ac3afb2b8e3c4-1333063-1fa400-1727f6c792a9a1;__gads=ID=dc9a625409077556:T=1591275841:S=ALNI_MbyldsOebciY-QMySFfsXwxuO70oQ;cf_clearance=5e9edfeeb5cc2bbdb75135eb0826a97858ed7a1e-1591507663-0-250;CNZZDATA1259444303=1995023598-1591274531-%7C1591507619'}
        cookie={
            '__cfduid': 'd4247258b9b4f26cd1ad523106d6523291591275840',
            'UM_distinctid': '1727f6c79291-0ac3afb2b8e3c4-1333063-1fa400-1727f6c792a9a1',
            'cf_clearance': '5e9edfeeb5cc2bbdb75135eb0826a97858ed7a1e-1591507663-0-250',
            'CNZZDATA1259444303': '1995023598-1591274531-%7C1591507619',
            '__gads': 'ID=dc9a625409077556:T=1591275841:S=ALNI_MbyldsOebciY-QMySFfsXwxuO70oQ'
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_type,meta={"max_retry_times":3},errback=self.errback_httpbin,cookies=cookie)
        #yield scrapy.Request(url=url, callback=self.parse_type, meta={"max_retry_times": 3},errback=self.errback_httpbin, cookies=cookie)


    def parse(self, response):
        for a in response.css('li.menu-item a'):
            booktype=a.css('::text').get()
            yield response.follow(a, callback=self.parse_type,meta={"booktype":booktype})


    def parse_type(self,response):
        booktype=response.css('li.current-menu-item a::text').get()
        for booka in response.css('div.card-item div a'):
            pageurl=booka.css('::attr(href)').get()
            if pageurl is not None:
                self.logger.info("get item:%s",pageurl)
                yield response.follow(pageurl, callback=self.parse_page, meta={"booktype": booktype})
        pageinfo=response.css('div.pagination ul')

        next_page = pageinfo.css('li.next-page a::attr(href)').get()
        if next_page is not None:
            self.logger.info("get nextpage:%s", next_page)
            yield response.follow(next_page, callback=self.parse_type, meta={"booktype": booktype})

    def parse_page(self,response):
        booitem = BooksItem()
        booktype = response.meta.get('booktype')
        bookinfo=response.css('div.book-info')

        booitem["img"] = bookinfo.css('div.bookpic img::attr(src)').get()
        if booitem["img"]==None:
            self.logger.error("img not find")

        allli=bookinfo.css('li')
        tagArr = []
        for li in allli:
            title=li.css('strong::text').get().strip(':：')
            textarr=li.css('::text')
            if title=="标签":
                for tag in li.css('a'):
                    tagArr.append(tag.css('::text').get().strip())
                booitem["tag"] = ",".join(tagArr)
            elif title=="作者":
                booitem["author"] = textarr[1].get().strip()
            elif title=="书名":
                booitem["title"] = textarr[1].get().strip()
            elif title=="ISBN":
                booitem["isbn"] = textarr[1].get().strip()

        booitem["type"] = booktype
        booitem["src"] = response.url
        booitem["desc"]=response.css('article.article-content').extract()[0]
        #获取下载地址
        formtag=response.css('div.e-secret form')
        if len(formtag)>0:
            formurl=formtag.css('::attr(action)').get().strip()
            formdata = 'e_secret_key=666'
            self.logger.info("post to:%s", formurl)
            yield scrapy.Request(
                formurl,
                body=formdata,
                method="POST",
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                callback=self.pasrse_download,
                meta=booitem
            )
        else:
            yield self.pasrse_download(response)


    def pasrse_download(self,response):
        booitem = response.meta
        downloadtable=response.css('table.dltable a')
        if len(downloadtable)>0:
            #是表格形式
            for downa in downloadtable:
                title=downa.css('::text').get().strip()
                linkurl=downa.css('::attr(href)').get().strip()
                if title.startswith("百度"):
                    booitem["baidu_url"] = linkurl
                elif title.startswith("城通"):
                    booitem["chentong_url"] = linkurl
                elif title.startswith("蓝奏"):
                    booitem["lanzou_url"] = linkurl
            if  booitem["baidu_url"] is not None:
                booitem["baidu_code"] =response.css('div.e-secret b::text').get().split('：')[1].strip()
            yield booitem
            return
        else:
            box=response.css('div.e-secret b')
            alla=box.css('a')
            alltext=box.css('::text')
            trueindex=0
            for index,texttag in enumerate(alltext):
                title=texttag.get().strip()
                linkurl=""
                if trueindex<len(alla):
                    linkurl = alla[trueindex].css('::attr(href)').get().strip()
                if title.startswith("百度"):
                    booitem["baidu_url"] = linkurl
                    trueindex+=1
                elif title.startswith("城通"):
                    booitem["chentong_url"] = linkurl
                    trueindex += 1
                elif title.startswith("蓝奏"):
                    booitem["lanzou_url"] = linkurl
                    trueindex += 1
                elif title.startswith("提取码"):
                    booitem["baidu_code"] = title.split('：')[1].strip()

            yield booitem


    #错误处理
    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
