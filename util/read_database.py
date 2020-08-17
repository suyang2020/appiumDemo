#encoding=utf-8
"""
读取数据库的方法
"""

import pymysql
from util.read_config import ReadConfig
from util.log import MyLog


class MyDB(object):
    def __init__(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        local_read_config = ReadConfig()
        host = local_read_config.get_db("host")
        username = local_read_config.get_db("username")
        password = local_read_config.get_db("password")
        port = local_read_config.get_db("port")
        database = local_read_config.get_db("database")
        self.config = {
            'host': str(host),
            'user': username,
            'password': password,
            'port': int(port),
            'db': database
        }

        self.db = None
        self.cursor = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        """每一次实例化的时候，都返回同一个instance对象"""
        if not hasattr(cls, "_instance"):
            cls._instance = super(MyDB, cls).__new__(cls)
        return cls._instance

    def connect_db(self):
        try:
            self.db = pymysql.connect(**self.config)
            self.cursor = self.db.cursor()
            self.logger.info("连接数据库成功")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    def execute_sql(self, sql, params=None):
        self.connect_db()
        self.cursor.execute(sql, params)
        self.db.commit()
        return self.cursor

    def get_all(self, cur):
        value = cur.fetchall()
        return value

    def close_db(self):
        self.db.close()
        self.logger.info("关闭数据库")






