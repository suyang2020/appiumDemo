"""
文件名：check_devices.py
创建人：苏杨
创建日期：
文件描述：定义一个log输出的格式和log输出等级的定义等等
"""
import logging
from datetime import datetime
import os
import threading


class Log:
    def __init__(self):
        self.pro_dir = os.path.dirname(os.path.abspath(__file__))
        self.pro_dir = os.path.split(self.pro_dir)[0]

        # 下面是记录log的文件创建的过程
        self.result_path = os.path.join(self.pro_dir, "result")
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)
        self.log_path = os.path.join(self.result_path, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # 创建处理器对象
        handler = logging.FileHandler(os.path.join(self.log_path, "output.log"))
        formatter = logging.Formatter('%(levelname)s  %(name)s:%(filename)s:%(lineno)s>> %(message)s')
        # 为处理器添加设置格式器对象，添加过滤器对象的方法为：handler.setFilter(filter)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger


class MyLog:
    """
    将上面的记录log的方法放到一个线程内，让它单独启用一个线程，是为了更好的写log
    """
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()
        return MyLog.log

