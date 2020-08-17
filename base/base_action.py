# coding=utf-8
"""
创建人：suyang
创建日期：
文件描述：通用模块，比如find_element,click,input等
"""

import base64
import os
import re
import allure
import imagehash
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from PIL import Image
import math
import operator
from functools import reduce
from util.log import MyLog
from selenium.common.exceptions import TimeoutException

log = MyLog().get_log()
logger = log.get_logger()


class BaseAction:
    def __init__(self, driver):
        self.driver = driver

    def click(self, loc):
        """
        功能：找到loc对应的元素，点击它
        :param loc: 类型为元组，包含两个元素，第一个元素是查找的方式比如By.XPATH，第二个元素是XPATH对应的值
        :return: 点击找到的元素
        """
        try:
            self.find_element(loc).click()
        except Exception:
            raise
        
    def click_s(self, loc, index):
        try:
            self.find_elements(loc)[index].click()
        except Exception:
            raise
    
    def tap(self, loc):
        """
        功能：找到loc对应的元素，轻敲它
        :param loc: 类型为元组，包含两个元素，第一个元素是查找的方式比如By.XPATH，第二个元素是XPATH对应的值
        :return: 点击找到的元素
        """
        tc = TouchAction(self.driver)
        x_value = loc[0]
        y_value = loc[1]
        try:
            tc.tap(x=x_value, y=y_value).perform()
        except Exception as e:
            logger.error(str(e))
            raise

    def input_text(self, loc, text):
        """
         功能：找到loc对应的元素，输入text文字
        :param loc: 类型为元组，包含两个元素，第一个元素是查找的方式比如By.XPATH，第二个元素是XPATH对应的值
        :param text: 要输入的字符串
        :return: 给找到的元素输入text值
        """
        try:
            self.find_element(loc).send_keys(text)
        except Exception:
            raise

    def find_element(self, loc, timeout=20.0, time=0.5):
        """
        查找元素
        :param loc: 类型为元组，包含两个元素，第一个元素是查找的方式比如By.XPATH，第二个元素是XPATH对应的值
        :return: 返回一个元素
        """
        by = loc[0]
        value = loc[1]

        if by == By.XPATH:
            value = self.make_xpath_feature(value)
        elif by == MobileBy.IMAGE:
            with open(value, 'rb') as i_file:
                b64_data = base64.b64encode(i_file.read()).decode('UTF-8')
                value = b64_data
        try:
            ele = WebDriverWait(self.driver, timeout, time).until(lambda x: x.find_element(by, value))
            # logger.info(value)
        except TimeoutError:
            logger.error("没有找到元素：%s，或者寻找超时" % value)
            raise
        else:
            return ele

    def find_elements(self, loc):
        """
        查找元素
        :param loc: 类型为元组，包含两个元素，第一个元素是查找的方式比如By.XPATH，第二个元素是XPATH对应的值
        :return: 返回元素列表
        """
        by = loc[0]
        value = loc[1]
        if by == "By.XPATH":
            value = self.make_xpath_feature(value)
        try:
            eles = WebDriverWait(self.driver, 10, 1).until(lambda x: x.find_elements(by, value))
        except Exception as e:
            logger.error("寻找元素超时%s" % str(e))
            raise
        else:
            return eles

    def make_xpath_unit_feature(self, loc):
        """
        拼接xpath中间的部分
        """
        args = loc.split(",")
        # xpath查找的属性名
        key_index = 0
        # 属性值
        value_index = 1
        # 是按照什么方式查找，0表示使用contains方法，1表示使用精确查找
        option_index = 2

        print(loc)

        try:
            args[value_index] = args[value_index].lstrip()
        except IndexError:
            logger.error("请检查xpath的值是否正确,应该类似这样写：'text,xxxx'")
        else:
            feature_middle = ""
            if len(args) == 2:
                feature_middle = "contains(@" + args[key_index] + ",'" + args[value_index] + "')" + " and "
            elif len(args) == 3:
                if args[option_index] == "1":
                    feature_middle = "@" + args[key_index] + "='" + args[value_index] + "'" + " and "
                elif args[option_index] == "0":
                    feature_middle = "contains(@" + args[key_index] + ",'" + args[value_index] + "')" + " and "
            return feature_middle

    def make_xpath_feature(self, loc):
        """
        参数loc的值为'@xxx,xxx'，表示要使用contains方法的xpath，
        loc的值为'@xxx,xxx,1'：表示使用精确查找
        loc的值为'@xxx,xxx,0'，表示要使用contains方法的xpath，
        """
        feature_start = "//*["
        feature_end = "]"
        feature = ""

        if isinstance(loc, str):
            feature = self.make_xpath_unit_feature(loc)
        else:
            for i in loc:
                feature += self.make_xpath_unit_feature(i)
        try:
            feature = feature.rstrip(" and ")
        except AttributeError:
            logger.error("请检查feature的返回值")
        else:
            result = feature_start + feature + feature_end
            return result

    def screenshot(self, file_name):
        """
        截图的方法
        :param file_name: 截图的名字
        """
        try:
            # 定义要创建的目录
            mkpath = "..\\screen"
            # 调用函数
            self.mkdir(mkpath)
            self.driver.get_screenshot_as_file("./screen/" + file_name + ".png")
        except Exception as e:
            logger.error(str(e))
            raise

    def put_screen_to_report(self, screenshot_name, step_describe):
        """
        截图并且将截图结果放到报告中
        :param screenshot_name: 截图的名字
        :param step_describe: 截图的描述
        """
        try:
            # 截图
            self.screenshot(screenshot_name)
            step_describe = step_describe + ':' + screenshot_name
            # 将截图上传到报告中
            allure.attach.file(r"./screen/%s.png" % screenshot_name, step_describe,
                               attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(str(e))
            raise
        
    def find_toast(self, message, screen_name="", is_screenshot=True, timeout=10.0, time=0.5):
        """
        获取toast的内容并返回
        :param message: 预期要获取到的toast部分提示信息
        :param screen_name:保存截图的名字
        :param is_screenshot:是否截图
        :param timeout:WebDriverWait寻找toast的超时时间
        :param time:每隔多长时间寻找toast一次
        :return: 返回找到的toast提示信息
        """
        message = "text," + message
        try:
            element = self.find_element((By.XPATH, message), timeout, time)
            if is_screenshot:
                self.screenshot(screen_name)
        except Exception:
            logger.error("没有找到这句提示信息:%s" % message[5:])
            return False
        else:
            return element.text

    def is_toast_exist(self, message, screen_name="", is_screenshot=False, timeout=10.0, time=0.1):
        """
        根据message查找toast是否存在
        :param message: toast的部分或者全部提示内容
        :param screen_name:保存截图的名字
        :param is_screenshot:是否截图
        :param timeout:WebDriverWait寻找toast的超时时间
        :param time:每隔多长时间寻找toast一次
        :return: 如果message存在，返回True，否则返回False
        """
        try:
            self.find_toast(message, screen_name, is_screenshot, timeout, time)
        except Exception:
            return False
        else:
            return True
            
    def press_keycode(self, keycode):
        """
        重写press_keycode，整合keyevent(keycode)
        :param keycode: 需要按的键，对应的keycode
        :return: 无
        """
        if "automationName" not in self.driver.desired_capabilities.keys():
            self.driver.keyevent(keycode)
        elif self.driver.desired_capabilities["automationName"] == "Uiautomator2":
            self.driver.press_keycode(keycode)

    def get_control_text(self, attr):
        """
        根据控件的某些属性，找到该控件，返回该控件的text
        :param attr: 控件属性
        :return: 返回控件attr的text
        """
        try:
            text = self.find_element(attr).text
        except Exception:
            logger.error("%s:元素没找到,请重新尝试" % attr[1])
        else:
            return text

    def scroll_find_element(self, loc, loc_a, loc_b, mode=0, time=3000):
        """
        寻找元素，没找到就向上滑动，继续找，找到为止
        :param loc:要寻找的元素
        :param loc_a:从哪个点或者元素滑
        :param loc_b:滑动到哪个点
        :param mode:滑动想要使用的方法，mode为0使用drag方法，mode为1使用scroll方法，mode为2使用swipe方法
        :param time:swipe方法用到的滑动时间，时间越长，滑动时的惯性越小。
        :return:
        """
        while True:
            try:
                self.find_element(loc, 5.0, 1.0)
            except Exception:
                # 滑动前，记录当前页面的页面信息
                page = self.driver.page_source
                # 向下翻页
                # 这里还要注意，翻完页之后，上一页的最下面的元素还应该在页面上，以免丢失元素
                if mode == 0:
                    ele_a = self.find_element(loc_a)
                    ele_b = self.find_element(loc_b)
                    # 从哪个元素拖拽到哪个元素，没有惯性
                    self.driver.drag_and_drop(ele_a, ele_b)
                elif mode == 1:
                    ele_a = self.find_element(loc_a)
                    ele_b = self.find_element(loc_b)
                    # 从哪个元素滑动到哪个元素，有惯性
                    self.driver.scroll(ele_a, ele_b)
                else:
                    ele_a_x = loc_a[0]
                    ele_a_y = loc_a[1]
                    ele_b_x = loc_b[0]
                    ele_b_y = loc_b[1]
                    # 从哪个点滑动到哪个点，time越长，惯性越小
                    self.driver.swipe(ele_a_x, ele_a_y, ele_b_x, ele_b_y, time)
                # 滑动后比较页面信息和滑动前的如果一样，就是滑动到底部了，退出滑动
                page_down = self.driver.page_source
                if page == page_down:
                    return False
            else:
                return True

    def swipe_screen(self, time=3000):
        """
        从手机的屏幕从下往上滑，一直到底部，退出
        :param time:swipe的时间
        :return:
        """
        # 向下翻页
        # 这里还要注意，翻完页之后，上一页的最下面的元素还应该在页面上，以免丢失元素
        window_width = self.driver.get_window_size()["width"]
        window_height = self.driver.get_window_size()["height"]
        start_x = window_width * 0.5
        start_y = window_height * 3 / 4
        end_x = start_x
        end_y = window_height * 0.25
        if end_y >= window_height:
            return 0
        self.driver.swipe(start_x, start_y, end_x, end_y, time)

    def swipe_screen_to_find(self, loc, time=3000):
        """
        从手机的屏幕从下往上滑，找到所需要元素就返回，没找到，一直找到底部，就直接退出
        :param loc:需要寻找的元素特征
        :param time:swipe的时间
        :return:
        """
        while True:
            try:
                ele = self.find_element(loc, 4.0, 1.0)
            except TypeError:
                logger.error("error")
            except TimeoutException:
                # 滑动前，记录当前页面的页面信息
                page = self.driver.page_source
                # 向下翻页
                # 这里还要注意，翻完页之后，上一页的最下面的元素还应该在页面上，以免丢失元素
                window_width = self.driver.get_window_size()["width"]
                window_height = self.driver.get_window_size()["height"]
                start_x = window_width * 0.5
                start_y = window_height * 3 / 4
                end_x = start_x
                end_y = window_height * 0.25
                # 滑动
                self.driver.swipe(start_x, start_y, end_x, end_y, time)
                # 滑动后比较页面信息和滑动前的如果一样，就是滑动到底部了，退出滑动
                page_down = self.driver.page_source
                if page == page_down:
                    break
            else:
                return ele

    def click_button_times(self, loc, time=0):
        if time == 0:
            while True:
                try:
                    self.find_element(loc, 10.0).click()
                except Exception:
                    break
        else:
            for i in range(time):
                try:
                    self.find_element(loc, 10.0).click()
                except Exception as e:
                    logger.error("找不到该元素：%s" % str(e))
                    break

    def compare_pic(self, pic1, pic2):
        """
        对比两张图片是否一样
        :param pic1: 图片1的路径
        :param pic2: 图片2的路径
        :return: 返回对比结果，结果越小，图越相似
        """
        image1 = Image.open(pic1)
        image2 = Image.open(pic2)

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a-b)**2, histogram1, histogram2)))/len(histogram1))
        print(differ)

        return differ

    def compare_img(self, img1, img2):
        """
        对比两张图片是否完全一样,一样返回true
        :param img1: 图片1的路径
        :param img2: 图片2的路径
        :return: 返回对比结果
        """
        image1 = Image.open(img1)
        image2 = Image.open(img2)

        h1 = str(imagehash.dhash(image1))
        h2 = str(imagehash.dhash(image2))
        image1.verify(image2)

        if h1 == h2:
            return True
        else:
            return False

    @staticmethod
    def get_img_size(self, img):
        image = Image.open(img)
        return image.size

    @staticmethod
    def str_to_tuple(self, str, sep=", "):
        """
        将字符串转为元组
        :param str: 需要转换为元组的字符串
        :param sep: 分隔符，默认以逗号+空格分隔
        :return: 返回元组
        """
        tuple(str.split(sep))

    @staticmethod
    def get_app_package(apk_path):
        """
        获取APP的包名
        :param apk_path: apk的路径
        :return: 返回apk对应的包名
        """
        try:
            app_package_adb = list(os.popen('aapt dump badging ' + apk_path).readlines())
            app_package = re.findall(r'\'com\w*.*?\'', app_package_adb[0])[0]
        except Exception as e:
            logger.error(str(e))
        else:
            return eval(app_package)

    @staticmethod
    def get_devices_id():
        """
        读取设备的id
        :return: 返回设备id
        """
        try:
            read_deviceId = list(os.popen('adb devices').readlines())
            device_id = read_deviceId[1].split('\t')[0]
        except Exception as e:
            logger.error(str(e))
        else:
            return device_id

    @staticmethod
    def get_devices_version():
        # os.popen('adb root')
        try:
            device_android_version = list(os.popen('adb shell getprop ro.build.version.release').readlines())
            device_version = device_android_version[0].split('\r\n')[0]
        except IndexError:
            logger.error("手机没有连接上,请检查,可以使用adb devices命令")
            # exit()
        else:
            return device_version

    def mkdir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断路径是否存在
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False


if __name__ == "__main__":
    BaseAction("").put_screen_to_report("s", "d")
