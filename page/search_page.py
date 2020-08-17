from util.read_config import ReadConfig
from base.base_action import BaseAction
from util.log import MyLog
import os

log = MyLog().get_log()
logger = log.get_logger()


class SearchPage(BaseAction):
    try:
        project_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.split(project_dir)[0]
        ini_dir = os.path.join(project_dir, "page\property.ini")
        rc = ReadConfig(ini_dir)
        current_page_title = rc.get_title("search")
        next_page_title = rc.get_title("order_list")
        # 身份证号
        eid_text = rc.get_search("eid_text")
        # 手机号
        tel_text = rc.get_search("tel_text")
        # 验证码
        verify_code_text = rc.get_search("verify_code_text")
        # 点击查询按钮
        search_button = rc.get_search("search_button")
        # 点击获取按钮
        gain_button = rc.get_search("gain_button")
    except Exception as e:
        logger.error(str(e))
        raise e

    def input_eid(self, text):
        try:
            self.input_text(self.eid_text, text)
        except Exception as e:
            logger.error("输入身份证号错误")
            raise e
        
    def input_tel(self, text):
        try:
            self.input_text(self.tel_text, text)
        except Exception as e:
            logger.error("输入手机号错误")
            raise e
        
    def input_verify_code(self, text):
        try:
            self.input_text(self.verify_code_text, text)
        except Exception as e:
            logger.error("输入验证码错误")
            raise e

    def click_search(self):
        try:
            self.click(self.search_button)
        except Exception as e:
            logger.error("点击查询按钮出错")
            raise e


