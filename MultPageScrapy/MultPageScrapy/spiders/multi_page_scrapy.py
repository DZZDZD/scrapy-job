from urllib.parse import urljoin

import requests
from scrapy import Spider
from scrapy import Request
import lxml.html
from MultPageScrapy.items import JobItem
import random
import time
import sqlite3
from MultPageScrapy.mongo_cache import MongoCache

class JobProfile(object):
    """
    工作的详细描述，模型类，用来存储解析结果，以及进行一些简单的数据清洗
    """
    def __init__(self):
        self.job_url = ""
        self.job_saray = ""
        self.job_title = ""
        self.job_area = ""
        self.job_experience = ""


    # 这里写一个函数处理过滤信息，限制薪资范围
    def salary_limit(self):
        '40k-60k'
        if self.job_saray.find('-') > 0:
            lt1 = self.job_saray.split('-')
            if lt1[0].rstrip('k')> '10':
                if lt1[1].rstrip('k')< '30':
                    return True

    # 限制地区
    def eara_limit(self):
        if self.job_area.find('北京') > 0:
            return True
    #限制工作内容
    def job_desc_limit(self):
        if  self.job_title.find('python')>0:
            return True
def judge_next_page_exist(response):
    try:
        btn = response.xpath('//button[@class="btn btn-pager btn-pager-disable"]/text()').extract()[0]
        print(btn)
    except:
        return True
    else:
        if btn=='下一页':
            return False
        elif btn=='上一页':
            try:
                response.xpath('//button[@class="btn btn-pager btn-pager-disable"]/text()').extract()[1]
            except:
                return True
            else:
                return False
        else:
            return True

#判断 每页的数据是否下载完成，再去翻页


def page_to_download():
    conn = sqlite3.connect('job.db')
    cursor = conn.cursor()
    sql = 'select count(*) from jobs'
    a = cursor.execute(sql)
    count = a.fetchone()[0]

    print('<<<<<',count)
    return count


class MultiPageSpider(Spider):
    """
    多页爬虫
    """
    name = "multi_page"
    def __init__(self):
        super(MultiPageSpider, self).__init__()
        self.list = [719, 538, 530, 765, 763, 531, 801, 653, 736, 600, 613, 635, 702, 703, 639, 599, 854, 749, 551, 622,
                     636, 654, 681, 682, 565, 664, 773]
        self.m = MongoCache()
        self.conn = sqlite3.connect('job.db')
        self.cursor = self.conn.cursor()
        self.index = 1
        self.lt=[]
        # 719郑州538上海530北京765深圳763广州#天津531成都801#杭州653#武汉736
        # 大连600#长春613#南京635#济南702#青岛703#苏州639#沈阳599#西安854
        # 长沙749#重庆551#哈尔滨622#无锡636#宁波654#福州681#厦门682#石家庄565#合肥664#惠州773
        # 全国489
    def start_requests(self):
        """
        1.引擎起始调用函数，该函数第一个需要下载的网页，通过返回Request对象实现
        此方法与start_urls属性提供的方法相同
        2. 如果先用start_urls默认解析方法是parse

        :return:
        """
        #智联招聘页面是一个ajax页面，可以先把每块的整体取出来，再写一个函数提取数据，还可以过滤要爬取信息
        # urls = ["https://sou.zhaopin.com/?pageSize=60&jl={}&kw=python&kt=3".format(i) for i in self.list]
        urls = ["https://sou.zhaopin.com/?pageSize=60&jl={}&kw=python&kt=3".format(801)]
        #Result 提供下载请求，下载成功后系统自动调用指定的callback方法向用户返回下载结果
        #meta 用于指定附加的用户元数据，可以随意指定需要的键值对，该元数据在整个request、response的生命周期都会被携带
        for url in urls:
            yield Request(url,callback=self.parse,meta={'page':'1'})
    """
    html = '<div class="listItemBox-wrapper clearfix"><!----> <div class="listItemBox clearfix"><div class="infoBox"><div class="itemBox nameBox"><div class="jobName"><a href="https://jobs.zhaopin.com/CC401810587J00085750610.htm" target="_blank"><span title="实习生应届生" class="job_title">实习生应届生</span></a> <span class="is_saleType"></span> <!----></div> <div class="commpanyName"><img alt="" src="//img03.zhaopin.cn/IHRNB/img/detailvipm.png" class="is_vipLevel"> <a href="https://company.zhaopin.com/CZ401810580.htm" target="_blank" title="北京融翔科技有限公司" class="company_title">北京融翔科技有限公司</a></div></div> <div class="itemBox descBox"><div class="jobDesc"><p class="job_saray">3K-5K</p> <ul class="job_demand"><li class="demand_item">北京-朝阳区</li> <li class="demand_item">经验不限</li> <li class="demand_item">大专</li></ul></div> <div class="commpanyDesc"><span class="info_item">民营 </span> <span class="info_item">20-99人 </span></div></div> <div class="itemBox"><div class="job_welfare"><div class="welfare_item">创业公司</div><div class="welfare_item">每年多次调薪</div><div class="welfare_item">周末双休</div><div class="welfare_item">五险一金</div><div class="welfare_item">年底双薪</div></div> <div class="commpanyStatus"><span class="recruit_status">置顶</span></div></div></div> <span class="zp-icon icon-job_checked-pile icon-job_isNotChecked" style="display: none;"></span> <div class="job_btnBox" style="display: none;"><div class="zp-jobBtn job_collect"><span class="zp-icon icon-job_collectStar"></span> <span>收藏</span></div> <div class="zp-jobBtn job_apply">申请职位</div></div></div></div>'
    """

    def parse(self, response):
        #使用css选择器，获取内容

        jobs = response.css('div.listItemBox-wrapper').extract()
        page_index = response.css('span.page-index').extract()
        for job in jobs:
            job_profile = self.parse_one_job(job)
            # print(job_profile.job_area)
            # 过滤
            # if job_profile.salary_limit():
                 #这里callback可以回调到另一个函数里解析详情页的内容
            url_str = job_profile.job_url
            # print(url_str)
            # result = requests.get(url=urljoin("https://sou.zhaopin.com", url_str))
            # if url_str not in self.m:
            #     self.m[url_str] = result
            yield Request(url=job_profile.job_url,callback=self.parse_detail,meta={'job':job_profile,'page':0})
            # print('>>>>>>>>>>>>>>',job_profile.job_title)
        """<span class="page-index">2</span>"""


        # 多页爬取，先判断有没有下一页（有的是直接有网址，有的是js）
        if judge_next_page_exist(response):
            print('我要翻页')
            # meta  携带翻页信息，随意带
            # 这里的url要不断变化，不然scrapy默认的配置识别已访问过,可以用meta 将job_profile传过去
            self.index += 1
            yield Request(url="http://www.baidu.com", callback=self.parse, meta={'page': 2}, dont_filter=True)


    def parse_one_job(self,html_str):
        """
        根据内部的html解析详情数据
        :param html_str:
        :return:
        """
        job_profile = JobProfile()
        tree = lxml.html.fromstring(html_str)
        # 这里可以过滤
        job_profile.job_title = tree.xpath('//span[@class="job_title"]/@title')[0]
        job_profile.job_url = tree.xpath('//div[@class="jobName"]/a[@href]/@href')[0]
        job_profile.job_saray = tree.xpath('//div[@class="jobDesc"]/p[@class="job_saray"]/text()')[0]
        job_profile.job_area = tree.xpath('//ul[@class="job_demand"]/li[1]/text()')[0]
        job_profile.job_experience = tree.xpath('//ul[@class="job_demand"]/li[2]/text()')[0]
        return job_profile

    def parse_detail(self,response):
        """
        用于解析工作详情信息页，将结果封装为指定的item，动刀pipelines，
        进一步存入数据库
        :param response:
        :return:
        """
        job_categories_old = ''.join(response.xpath('//ul[@class="terminal-ul clearfix"]/li[8]/strong/a/text()').extract())
        job_categories_new = ''.join(response.xpath('//h1[@class="l info-h3"]/text()').extract())



        if job_categories_old:
            # 工作详情
            job_description_base = response.xpath('//div[@class="tab-inner-cont"][1]')
            job_des = ''.join(job_description_base.xpath('string(.)').extract())

            #薪资
            pay = response.meta['job'].job_saray
            #职位
            position = response.meta['job'].job_title
            #公司
            # company = response.css('div.company > a:nth-child(1)::text').extract_first()
            company = response.css('div.fixed-inner-box div:nth-child(1) h2 a::text').extract_first()
            #工作经验与学历
            work_experience = ''.join(response.xpath('//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()').extract())
            education = ''.join(response.xpath('//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()').extract())
            job_term = work_experience + education
            #工作地点
            address = response.meta['job'].job_area

            item = JobItem()
            item['job_des'] = job_des
            item['pay'] = pay
            item['position'] = position
            item['company'] = company
            item['job_term'] = job_term
            item['address'] = address

            yield item

        else:
            # 工作详情
            job_description_base = response.xpath('//div[@class="responsibility pos-common"]/')
            job_des = ''.join(job_description_base[0].xpath('string(.)').extract())
            # 薪资
            pay = response.meta['job'].job_saray
            # 职位
            position = response.meta['job'].job_title
            # 公司
            # company = response.css('div.company > a:nth-child(1)::text').extract_first()
            company =''.join(response.xpath('//h3/a/text()').extract())
            # 工作经验与学历
            work_experience = ''.join(response.xpath('//div[@class="info-three l"]/span[2]/text()').extract())
            education = ''.join(response.xpath('//div[@class="info-three l"]/span[3]/text()').extract())
            job_term = work_experience + education
            # 工作地点
            address = response.meta['job'].job_area

            item = JobItem()
            item['job_des'] = job_des
            item['pay'] = pay
            item['position'] = position
            item['company'] = company
            item['job_term'] = job_term
            item['address'] = address

            yield item




