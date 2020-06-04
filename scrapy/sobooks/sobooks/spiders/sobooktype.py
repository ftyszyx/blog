import  scrapy
from sobooks.items import BookTypeItem

#读取标签
class authorspider(scrapy.Spider):
    name = "sobooktype"
    start_urls = ['https://sobooks.cc/']
    def parse(self, response):
        for a in response.css('li.menu-item a'):
            item =BookTypeItem()
            item["name"]=a.css('::text').get().strip()
            self.logger.info("get booktype:%s",item)
            yield item