# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from House.MysqlUtil import MysqlUtil


class HousePipeline:

    # 开启爬虫时连接数据库
    def open_spider(self, spider):
        self.pool = MysqlUtil()

    def process_item(self, item, spider):
        # print(self.pool)
        # print(item)
        self.pool.insert_one(item)
        return item

    def close_spider(self, spider):
        self.pool.close()
        pass
