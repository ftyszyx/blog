1、新建一个工程
scrapy startproject myproject

2、生成spider
scrapy genspider mydomain mydomain.com

3、运行spider
scrapy crawl myspiders

3、帮助
scrapy -h


scrapy shell 'http://quotes.toscrape.com/page/1/'
response.css('title')
response.css('title::text').getall()