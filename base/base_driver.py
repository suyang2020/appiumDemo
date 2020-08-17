# coding=utf-8
"""
创建人：suyang
创建日期：
文件描述：连接手机的模块
"""
import os

import urllib3
from appium import webdriver
import selenium
from util.read_config import ReadConfig
from base.base_action import BaseAction
from util.check_devices import is_devices_link
from util.check_devices import install_apk
from util.check_devices import check_local_file
from util.check_devices import is_apk_installed
from util.log import MyLog

log = MyLog().get_log()
logger = log.get_logger()


def base_driver():
    """连接手机，获取driver"""

    rc = ReadConfig()
    port = rc.get_tel("port")
    # 系统版本号
    device_version = BaseAction.get_devices_version()
    # APP安装包的名字
    apk_name = rc.get_tel("apkName")
    apk_path = os.path.join(ReadConfig.project_dir, "files\\apk\\" + apk_name)
    app_package = BaseAction.get_app_package(apk_path)
    # app_package = rc.get_tel("appPackage")
    # 读取设备 id
    read_device_id = BaseAction.get_devices_id()
    app_activity = rc.get_tel("appActivity")
    no_reset = rc.get_tel("noReset")
    full_reset = rc.get_tel("fullReset")
    if no_reset == "true" or "True" or "TRUE":
        no_reset = True
        full_reset = False
    else:
        no_reset = False
        full_reset = True

    server = r'http://localhost:' + port + r'/wd/hub'  # Appium Server, 端口默认为4723

    if is_devices_link():
        # if not is_apk_installed(apk_path):
        #     if check_local_file(apk_path):
        #         logger.info("开始安装APP：%s" % apk_name)
        #         install_apk(apk_path)
        #         logger.info("APP安装完成")
        desired_capabilities = {
            'platformName': 'Android',
            'deviceName': read_device_id,
            'platformVersion': device_version,
            'appPackage': app_package,
            'appActivity': app_activity,
            'noReset': no_reset,
            'fullReset': full_reset,
            # 解决中文乱码问题
            'unicodeKeyboard': True,
            'resetKeyBoard': True,
            # 下面两个是appium不重新安装
            'skipServerInstallation': True,
            'skipDeviceInitialization': True
        }
        try:
            driver = webdriver.Remote(server, desired_capabilities)  # 连接手机和APP
        except urllib3.exceptions.MaxRetryError:
            logger.error("请检查appium是否启动 or config文件中的appium的端口是否正确")
            exit()
        except selenium.common.exceptions.WebDriverException:
            logger.error("请检查driver的参数，比如APP包名，启动名等")
            exit()
        else:
            return driver
    else:
        exit()


