import pymysql
from dbutils.pooled_db import PooledDB


class MysqlUtil(object):

    def __init__(self):
        config = {
            'host': "127.0.0.1",
            'port': 3306,
            'database': "house_price",
            'user': "root",
            'password': "root",
            'charset': "utf8mb4",
        }
        self.pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=config['host'],
                             port=config['port'], user=config['user'],
                             passwd=config['password'], db=config['database'],
                             charset=config['charset'])

    # 获取链接
    def get_conn(self):
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur

    # 关闭数据库链接
    def close_conn(self, conn, cur):
        cur.close()
        conn.close()

    # 插入一条数据
    def insert_one(self, item):
        conn, cur = self.get_conn()
        sql = "insert into house_price.tab1(village,price,area,address1,address2,address3,huxing,onsale,wuyetp,tags) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = list()
        params.append(item['village'])
        params.append(item['price'])
        params.append(item['area'])
        params.append(item['address1'])
        params.append(item['address2'])
        params.append(item['address3'])
        params.append(item['huxing'])
        params.append(item['onsale'])
        params.append(item['wuyetp'])
        params.append(item['tags'])
        try:
            cur.execute(sql, tuple(params))
            conn.commit()
            # print('数据库插入成功')
        except BaseException as e:
            print('数据库插入错误', e)
        finally:
            self.close_conn(conn, cur)
    def close(self):
        self.pool.close()
