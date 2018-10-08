from scrapy import Spider

import lxml.html
from scrapy import Request,FormRequest
#日志
import logging

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
def parse_form(html):
    """
    找到所有form表单提交关键字
    :param html:
    :return:
    """
    tree = lxml.html.fromstring(html)

    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')

    return data



class CookiesSpider(Spider):
    name = 'CookieSpider'


    def start_requests(self):
        return [Request('',
                        headers = headers,callback=self.login)]

    def login(self,response):
        #解析所有的form表字段
        post_data = parse_form(response.text)
        post_data['email'] = '2478407903@qq.com'
        post_data['password'] = 'prologue123'


        #提交表单，登录使用，相当于post一个url请求
        return [FormRequest('http://example.webscraping.com/places/default/user/login',
                            formdata=post_data,headers=headers,callback=self.after_login)]
    def after_login(self,response):
        # 登录成功以后 第一次下载的种子页
        # make_requests_from_url 将控制权交给scrapy，并且带着登录信息
        # 默认从parse开始
        return self.make_requests_from_url('http://example.webscraping.com')

    def parse(self,response):
        logging.debug('*' * 40)
        logging.debug('response text %s' %response.text)
        logging.debug('response headers: %s' %response.headers)
        # logging.debug('response cookies；%s' %response.cookies)


