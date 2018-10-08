# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MultpagescrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobItem(scrapy.Item):
    """
    定义数据模型类，要注意打开settings中的配置
    """
    position = scrapy.Field()
    company = scrapy.Field()
    pay = scrapy.Field()
    address = scrapy.Field()
    job_term = scrapy.Field()
    job_des = scrapy.Field()




