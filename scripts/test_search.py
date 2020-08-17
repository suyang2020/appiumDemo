import os, sys
sys.path.append(os.getcwd())
import allure
import pytest
import time
from base.base_driver import base_driver
from page.search_page import SearchPage
from base.base_yml import yaml_to_list
from util.log import MyLog


log = MyLog().get_log()
logger = log.get_logger()


# 将yaml里面的数据以列表形式返回
def param(test_name):
    """
    获得'search_data'这个文件中的key键对应的值
    :param key: yml文件中的一个最外层键
    :return: 返回key对应的值
    """ 
    yaml_file_name = "search_data"
    return yaml_to_list(yaml_file_name, test_name)


class TestSearch:

    def setup_class(self):
        self.driver = base_driver()
        self.search_page = SearchPage(self.driver)
        logger.info("----------开始测试:查询页面----------")
        # 点击首页的卡片查询按钮
        allure.attach("", "点击首页的卡片查询按钮")
        self.search_page.click_search_button()

    def teardown_class(self):
        logger.info("----------结束测试:查询页面----------")
        self.driver.quit()

    @allure.title("!test_search")
    @pytest.mark.parametrize("args", param("test_search"))
    def test_search(self, args):
        """
        测试查询页面
        """
        logger.info("测试参数：%s" % args)
        try:
            code = args['code']
            message = args['message']
            screen_name = args["screen_name"]
            eid = args["eid"]
            tel = args['tel']

            # 输入身份证号
            allure.attach("", "输入身份证号")
            self.search_page.input_eid(eid)
            # 输入电话
            allure.attach("", "输入电话")
            self.search_page.input_tel(tel)
            # 输入验证码
            allure.attach("", "输入验证码")
            self.search_page.input_verify_code(code)
            # 点击查询
            allure.attach("", "点击查询")
            self.search_page.click_search()
            if message == "success":
                time.sleep(2)
                assert self.search_page.next_page_title in self.search_page.get_page_title()
                self.search_page.back_last_page()
            else:
                allure.attach("", "检查提示信息是否正确")
                toast_message = self.search_page.find_toast(message, screen_name)
                time.sleep(3)

                if not toast_message:
                    allure.attach("", "没有找到这句提示信息：%s" % message)
                    self.search_page.back_last_page()
                    assert 0
                else:
                    allure.attach.file(r"./screen/%s.png" % screen_name, '检查输入错误的截图：%s' % screen_name,
                                       attachment_type=allure.attachment_type.PNG)
                    assert message == toast_message
                    assert self.search_page.current_page_title in self.search_page.get_page_title()
                    allure.attach("", "成功找到这句提示信息：%s" % message)
        except Exception as e:
            logger.error(str(e))
            raise












