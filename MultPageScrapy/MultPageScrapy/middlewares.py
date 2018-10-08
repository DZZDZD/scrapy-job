# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from scrapy.http import HtmlResponse


class MultpagescrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MultpagescrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware(object):
    """
    selenuim  中间件，用来模拟浏览器下载，注意打开settings中的配置
    """
    def __init__(self):
        self.options = Options()
        self.options.add_argument('-headless')
        self.browser = webdriver.Firefox(executable_path="D:\geckodriver-v0.21.0-win64\geckodriver.exe",
                                         firefox_options=self.options)
    def process_request(self,request,spider):
        """
        中间件被激活的时候自动调用，
        spider.name可以区分不同的爬虫
        :param request:
        :param spider:
        :return:
        """
        if spider.name == 'multi_page':
            #判断是翻页的操作，执行seleuim
            if int(request.meta['page']) == 1:

                self.browser.get(request.url)
                # time.sleep(3)
                return HtmlResponse(
                    url=self.browser.current_url,
                    body=self.browser.page_source,
                    encoding='utf-8',
                    request=request
                )
            if int(request.meta['page']) == 2:
                # 现将页面反倒最下面，因为有的页面不下拉不加载，取不到翻页的按钮

                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(2)
                page = self.browser.find_element_by_css_selector('button.btn:nth-child(8)')
                page.click()
                time.sleep(3)
                return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source,
                                    request=request, encoding="utf-8")
            # else:
            #     html_content = requests.get(request.url).content
            #     return HtmlResponse(url=request.url,body=html_content,
            #                     request=request,encoding="utf-8")

import random
PROXIES = ['']

class ProxyMiddleware(object):
    """
    设置Proxy
    """
    def process_request(self,request,spider):
        ip = random.choice(PROXIES)
        request.meta['proxy'] = ip







