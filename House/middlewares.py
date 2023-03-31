# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class HouseSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class HouseDownloaderMiddleware:
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
        spider.logger.info("Spider opened: %s" % spider.name)

class SelenimuDownloaderMiddleware:
    def process_request(self, request, spider):
        if 'https://cq.58.com/robots.txt' == request.url:
            return None
        options = webdriver.ChromeOptions()

        # PROXIES = [
        #     'http://113.231.17.227:4252',
        #     'http://122.246.91.79:4213',
        #     'http://114.99.7.202:4226',
        # ]
        # PROXY = random.choice(PROXIES)
        # print('--proxy-server={}'.format(PROXY))
        # options.add_argument('--proxy-server={}'.format(PROXY))

        options.add_experimental_option('excludeSwitches', ['enable-logging']) # 关闭DevTools listening on ws://127.0.0.1的打印
        # options.add_argument('--headless')  # 开启无界面模式
        # options.add_argument('--disable-gpu')  # 禁用gpu
        options.add_argument('disable-cache')  # 禁用缓存
        options.add_argument('log-level=2')  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
        options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
        options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
        options.add_argument('--incognito')  # 隐身模式（无痕模式）
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        driver = webdriver.Chrome(options=options)

        driver.get(request.url)
        time.sleep(5)
        try:
            b = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/input')
            content = b.get_attribute('value').strip()
            print(content)
            b.click()
            time.sleep(1)
            if content == "点击按钮进行登录":
                name = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[3]/div[2]/div[1]/input')
                password = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[3]/div[2]/div[4]/input')
                name.send_keys("19936042493")
                time.sleep(1)
                password.send_keys("yangkun131160")
                time.sleep(1)
                driver.find_element(By.XPATH, '/html/body/div[6]/div/div[3]/div[2]/div[5]/button').click()
        except NoSuchElementException:
            # print("Element not found")
            pass
        time.sleep(5)
        body = driver.page_source
        driver.close()
        return HtmlResponse(request.url, body=body, encoding='utf-8')