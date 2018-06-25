# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from csanjukeSpider.settings import USER_AGENTS,PROXY_POOL_URL
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
from time import sleep

import random
import requests
import re


class CsanjukespiderSpiderMiddleware(object):
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

class CsanjukespiderDownloaderMiddleware(object):
    #logger = logging.getLogger(__name__)
    def process_request(self, request, spider):
        # self.logger.debug("Using Proxy")
        user_agent = random.choice(USER_AGENTS)
        request.headers['User-Agent'] = user_agent
        return None


class RedirectDownloaderMiddleware(object):
    def get_proxy(self):
        result = requests.get(PROXY_POOL_URL)
        if result.status_code == 200:
            proxy = result.text
            # proxies = {'https': 'https://' + proxy}
            proxies = 'https://' + proxy
            return proxies
        else:
            print("--------------------------get proxy again---------------------------")
            return self.get_proxy()

    def process_response(self, request, response, spider):
        if response.status == 302:
            print('response.status = 302')
            request.meta['proxy'] = self.get_proxy()
            return request
        else:
            return response


class SeleniumDownloaderMiddleware(object):
    def __init__(self):
        self.logger = getLogger(__name__)
        self.browser = webdriver.Chrome(service_log_path=r"watchlog.log")
        self.timeout = 60
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        self.logger.debug("SeleniumDownloading................")
        try:
            if re.compile('.*captcha.*').match(request.url):
                self.logger.debug("requestUrl is {}".format(request.url))
                self.browser.get(request.url)
                self.wait.until(
                    EC.presence_of_element_located((By.ID, "ISDCaptcha"))
                )
                self.browser.save_screenshot('page.png')
                self.logger.debug("-------------------already save png---------------")
                sleep(100)
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

