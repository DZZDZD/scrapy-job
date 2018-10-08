import requests
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import lxml.html

options = Options()
# options.add_argument('-headless')
browser = webdriver.Firefox(executable_path="D:\geckodriver-v0.21.0-win64\geckodriver.exe",
                                 firefox_options=options)




html = browser.get('http://www.jyeoo.com/')
data = browser.find_element_by_xpath('/html/body/div[6]/div/ul/li[1]/div[2]/ul/li[7]/a[1]')
data.click()
html1 = browser.get(browser.current_url)
