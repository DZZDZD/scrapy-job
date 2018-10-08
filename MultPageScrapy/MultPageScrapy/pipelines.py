# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import pymysql
from MultPageScrapy.items import JobItem
class MultpagescrapyPipeline(object):
    """
    处理spider解析过的结果，可以存入数据库或文件，打开配置
    """

    def __init__(self):
        self.conn = sqlite3.connect('job.db')
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        """
        对item做操作，
        :param item:
        :param spider:
        :return:
        """
        if isinstance(item, JobItem):

            pay = item['pay']
            position = item['position']
            address = item['address']
            company = item['company']
            job_term = item['job_term']
            job_des = item['job_des']


            sql_insert = """insert into aaa values(?,?,?,?,?,?)"""
            param = (pay,position,company,job_term,job_des,address)
            self.cursor.execute(sql_insert,param)

            # self.cursor.execute("insert into jobs values('%s','%s','%s','%s','%s','%s')" %(pay,position,company,job_term,job_des,address))

            self.conn.commit()
            return item
