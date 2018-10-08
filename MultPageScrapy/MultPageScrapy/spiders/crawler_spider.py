# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urljoin,urlparse

class CrawlerSpiderSpider(CrawlSpider):
    name = 'crawler_spider'
    # allowed_domains = ['webscrap.com']
    start_urls = ['http://www.runoob.com/ajax/ajax-tutorial.html']

    rules = (
        Rule(LinkExtractor(allow=r'(/ajax)'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # paths = urlparse(response.url).path
        # url_name = paths[len(paths) - 1]
        # file_name = 'dowmload/' + url_name +'.html'
        # with open(file_name,'wb')as f:
        #     f.write(response.body)
        print(response.url)
