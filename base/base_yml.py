"""
创建人：suynag
创建日期：
文件描述：处理yml文件的模块
"""
import os
import yaml
from util.log import MyLog

log = MyLog().get_log()
logger = log.get_logger()


def yaml_to_list(file_name, key):
    """
    将yml文件转为list
    :param file_name: yml文件名字，将哪一个yml文件转为list
    :param key: yml文件中的最外层键，测试用例的名字
    :return: 返回一个list
    """
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.split(project_dir)[0]
    yml_path = os.path.join(project_dir, "data")

    # 打开yml文件，将内容load到data中，此时data是一个字典

    with open(os.path.join(yml_path, file_name + ".yml"), "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        try:
            # 将测试用例名对应的values给data
            data = data[key]
        except KeyError:
            logger.error("请检查<data>文件夹中的<%s.yml>文件的key:<%s>是否正确" % (file_name, key))
        else:
            # 如果data是一个list，就直接返回
            if isinstance(data, list):
                return data
            # 否则 将data里面的键值对放到list中，将list返回
            else:
                data_list = list()
                for case_data in data.values():
                    data_list.append(case_data)
                return data_list




