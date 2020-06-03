import  scrapy
from sobooks.items import TagsItem

#读取标签
class authorspider(scrapy.Spider):
    name = "sotag"
    start_urls = ['https://sobooks.cc/']
    def parse(self, response):
        for tag in response.css('div.git_tags a') :
            item =TagsItem()
            item["name"]=tag.css('::text').get().split(' ')[0].strip()
            self.logger.info("get item:%s",item)
            yield item