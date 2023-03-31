import scrapy
from math import ceil
import re
from House.items import HouseItem


class OnepageSpider(scrapy.Spider):
    name = "OnePage"
    allowed_domains = ["cq.58.com"]
    start_urls = ["https://cq.58.com/xinfang/"]

    def parse(self, response):
        total = response.xpath('//*[@id="container"]/div[2]/div/div[1]/div[2]/span/text()').get()
        total = re.findall(r"\d+\.?\d*", total)[0]
        total = int(total)
        pages = ceil(total / 60)
        print(total, pages)
        for i in range(1, pages+1):
            url = "https://cq.58.com/xinfang/loupan/all/p{}/".format(i)
            # print(url)
            yield scrapy.Request(url, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        elements = response.xpath('//*[@id="container"]/div[2]/div/div[2]/div')
        for e in elements:
            item = HouseItem()
            # 小区名
            village = e.xpath('./div/a[1]/span/text()').get().strip()
            item['village'] = village
            # 价格
            price = e.xpath('./a[2]/p/span/text()').get()
            item['price'] = price
            # 地址
            address = e.xpath('./div/a[2]/span/text()').get().strip()
            address = address.split('\xa0')
            address1 = address[1]
            address2 = address[2]
            address3 = address[4]
            item['address1'] = address1
            item['address2'] = address2
            item['address3'] = address3

            # 建筑面积
            huxing = e.xpath('./div/a[3]/span')
            try:
                area = huxing[-1].xpath('text()').get()
                del (huxing[-1])
                area = re.findall(r"\d+\.?\d*", area)
                area = '/'.join(area)
                item['area'] = area
            except Exception as e:
                item['area'] = ''
                print('建筑面积为空', e)
            # 房屋标签
            str = ""
            for h in huxing:
                str += h.xpath('text()').get().strip()
                str += "/"
            item['huxing'] = str

            onsale = e.xpath('./div/a[4]/div/i[1]/text()').get().strip()
            item['onsale'] = onsale

            try:
                wuyetp = e.xpath('./div/a[4]/div/i[2]/text()').get().strip()
                item['wuyetp'] = wuyetp
            except Exception as e:
                item['wuyetp'] = ''
                print('物业类型为空', e)

            tags = e.xpath('./div/a[4]/div/span')
            tag = ""
            for t in tags:
                tag += t.xpath('./text()').get().strip()
                tag += "/"
            item['tags'] = tag
            yield item
