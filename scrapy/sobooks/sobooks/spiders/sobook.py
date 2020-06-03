import scrapy
from sobooks.items import BooksItem

class authorspider(scrapy.Spider):
    name = "sobook"
    start_urls = ['https://sobooks.cc/']
    def parse(self, response):
        item =BooksItem()
        yield item