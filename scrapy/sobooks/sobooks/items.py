# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SobooksItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    img = scrapy.Field()
    type_title=scrapy.Field()
    author=scrapy.Field()
    desc=scrapy.Field()
    baidu_url=scrapy.Field()
    baidu_code=scrapy.Field()



    pass
