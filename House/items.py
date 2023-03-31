# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    village = scrapy.Field()
    price = scrapy.Field()
    address1 = scrapy.Field()
    address2 = scrapy.Field()
    address3 = scrapy.Field()
    area = scrapy.Field()
    huxing = scrapy.Field()
    onsale = scrapy.Field()
    wuyetp = scrapy.Field()
    tags = scrapy.Field()
