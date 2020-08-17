"""
文件名：check_devices.py
创建人：suyang
创建日期：
文件描述：检查手机设备是否正确连接
"""

import glob
import os
from base.base_action import BaseAction
from util.log import MyLog


# 定义全局变量
devices_list_finally = []
chose_file_num = []
log = MyLog().get_log()
logger = log.get_logger()


def is_devices_link():
    """
    检查是否有设备连接PC,有则返回True
    :return:
    """
    devices_list_start = []
    devices_cmd = os.popen('adb devices').readlines()
    devices_list_start_count = len(devices_cmd)
    devices_list_start_count = devices_list_start_count - 2
    if devices_list_start_count >= 1:
        print('find devices linked')
        for devices_num in range(devices_list_start_count):
            devices_list_start.append(devices_cmd[devices_num + 1])
            device_list_pers = devices_list_start[devices_num].index('\t')
            devices_list_finally.append(devices_list_start[devices_num][:device_list_pers])
            print('devices list :' + '%d  ' % (devices_num + 1) + '%s' % devices_list_finally[devices_num])
        return True
    else:
        print('Can not find devices link...pls check device link...')
        logger.error("无法连接到手机，试试重新插拔手机")
        return False


def is_apk_installed(apk_path):
    """
    判断手机是否安装了待测试APP，安装则返回True
    :return:
    """
    app_package = BaseAction.get_app_package(apk_path)
    app_package = 'package:' + app_package + '\n'
    all_packages = list(os.popen("adb shell pm list package"))
    if app_package in all_packages:
        return True
    else:
        return False


# 检查本地文件是否存在
def check_local_file(apk_path):
    file_list = glob.glob(apk_path)
    file_index = len(file_list)
    if file_index != 0:
        if file_index == 1:
            return True
    else:
        logger.error("无法安装APP，请检查apk文件路径是否正确")
        exit()


# 安装应用
def install_apk(apk_path):
    for install_apk_to_devices_index in range(len(devices_list_finally)):
        os.system('adb -s' + ' ' + devices_list_finally[install_apk_to_devices_index] + ' ' + 'install' + ' ' + apk_path)






