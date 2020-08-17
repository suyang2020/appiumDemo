"""
读取配置文件的各种方法
"""
import codecs
import configparser
import os
from selenium.webdriver.common.by import By
from util.log import MyLog


log = MyLog().get_log()
logger = log.get_logger()


def dir_log(test):
    """
    捕获异常的装饰器方法
    :param test:需要增加异常捕获的方法名
    :return:
    """
    def log(*args, **kwargs):
        try:
            res = test(*args, **kwargs)
            return res
        except Exception:
            raise
    return log


class ReadConfig:
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.split(project_dir)[0]

    def __init__(self, config_path="config.ini"):
        # 需要读取的配置文件路径
        self.config_path = os.path.join(self.project_dir, config_path)

        try:
            with open(self.config_path, encoding="UTF-8") as fd:
                data = fd.read()
                # 判断data是否带BOM，如果带就删除
                if data[:3] == codecs.BOM_UTF8:
                    data = data[3:]
                    # 使用codecs.open打开文件，写入的时候更不容易出现编码问题，open方法只能写入str
                    with codecs.open(self.config_path, "w", encoding="UTF-8") as file:
                        file.write(data)
        except FileNotFoundError as e:
            logger.error(str(e))
        # 将配置文件分割成一块一块的字典形式
        self.cfp = configparser.ConfigParser()
        self.cfp.read(self.config_path, encoding="UTF-8")

    @dir_log
    def get_db(self, name):
        value = self.cfp.get("DATABASE", name)
        return value

    @dir_log
    def get_test(self, name):
        value = self.cfp.get("TEST", name)
        return value

    @dir_log
    def get_title(self, name):
        value = self.cfp.get("TITLE", name)
        return value

    @dir_log
    def get_tel(self, name):
        value = self.cfp.get("TEL", name)
        return value

    @dir_log
    def trs(self, str):
        # res = []
        res = str.split(", ", 1)
        by = res[0]
        value = res[1]

        if by == "By.XPATH":
            res[0] = By.XPATH
        elif by == "By.ID":
            res[0] = By.ID
        elif by == "By.CLASS_NAME":
            res[0] = By.CLASS_NAME
        elif by == "By.NAME":
            res[0] = By.NAME

        if value[0] == '"' or value[0] == "'":
            res[1] = eval(value)
        return tuple(res)

    @dir_log
    def get_index(self, name):
        value = self.cfp.get("INDEX", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_area(self, name):
        value = self.cfp.get("AREA", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_verify(self, name):
        value = self.cfp.get("VERIFY", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_address(self, name):
        value = self.cfp.get("ADDRESS", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_confirm(self, name):
        value = self.cfp.get("CONFIRM", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_service(self, name):
        value = self.cfp.get("SERVICE", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_upload(self, name):
        value = self.cfp.get("UPLOAD", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_order(self, name):
        value = self.cfp.get("ORDER", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_search(self, name):
        value = self.cfp.get("SEARCH", name)
        value = self.trs(value)
        return value

    @dir_log
    def get_list(self, name):
        value = self.cfp.get("LIST", name)
        value = self.trs(value)
        return value
