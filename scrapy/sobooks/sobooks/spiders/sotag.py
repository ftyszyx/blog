import  scrapy
from sobooks.items import TagsItem

class authorspider(scrapy.Spider):
    name = "sotag"
    start_urls = ['https://sobooks.cc/']
    def parse(self, response):
        for taglist in response.css('div.git_tags'):
            item =TagsItem()
            item["name"]=taglist.css('a::text').get().split(' ')[0]
            self.logger.info("get item:%s",item)
            yield item