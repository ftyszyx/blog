# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    type=scrapy.Field()
    img = scrapy.Field()
    author=scrapy.Field()
    desc=scrapy.Field()
    baidu_url=scrapy.Field()
    baidu_code=scrapy.Field()
    isbn=scrapy.Field()
    tag=scrapy.Field()
    pass


class TagsItem(scrapy.Item):
    name=scrapy.Field()
    pass

#使用item
#product = SobooksItem(title='Desktop PC', type_title=1000)
#product['name']
#product2 = product.copy()
#product2 = product.deepcopy()