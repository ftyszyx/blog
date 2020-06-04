import scrapy
from sobooks.items import BooksItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import json
#读取book
class authorspider(scrapy.Spider):
    name = "sobook"
    start_urls = ['https://sobooks.cc/']

    def parse(self, response):
        for a in response.css('li.menu-item a'):
            booktype=a.css('::text').get()
            yield response.follow(a, callback=self.parse_type,meta={"booktype":booktype})


    def parse_type(self,response):
        booktype = response.meta.get('booktype')
        for booka in response.css('div.card-item a'):
            yield response.follow(booka, callback=self.parse_page, meta={"booktype": booktype})
        pageinfo=response.css('div.pagination ul')

        next_page = pageinfo.css('li.next-page a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_page, meta={"booktype": booktype})

    def parse_page(self,response):
        booitem = BooksItem()
        booktype = response.meta.get('booktype')
        bookinfo=response.css('div.book-info')
        booitem["type"] = booktype
        booitem["img"] = bookinfo.css('div.bookpic img::attr(src)').get().strip()
        booitem["title"]=bookinfo.css('ul li:nth-child(1)::text').get().strip()
        booitem["isbn"] = bookinfo.css('ul li:nth-last-child(1)::text').get().strip()
        booitem["desc"]=response.css('div.article-content p:nth-child(2)::text').get().strip()
        tagArr = []
        for tag in bookinfo.css('ul li:nth-child(4) a'):
            tagArr.append(tag.css('::text').get().strip())
        booitem["tag"] = ",".join(tagArr)

        formtag=response.css('div.e-secret')
        formurl=formtag.css('form::attr(action)').get().strip()
        formdata = {'e_secret_key': '666'}
        yield scrapy.Request(
            formurl,
            body=json.dumps(formdata),
            method="POST",
            headers={'Content-Type': 'application/json'},
            callback=self.pasrse_download,
            meta=booitem
        )


    def pasrse_download(self,response):
        booitem = response.meta
        box=response.css('div.e-secret b')
        boxtext=box.css('::text').get().strip()
        booitem["baidu_code"]=boxtext
        booitem["baidu_url"] = box.css('a:nth-last-child(1)::attr(href)').get()
        booitem["lanzou_url"] = box.css('a:nth-last-child(2)::attr(href)').get()
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
