"""
文件名：run.py
创建人：suyang
创建日期：
文件描述：运行case的入口，在caselist.txt中输入想要运行的case名称，运行run.py或者双击run.bat
"""

# encoding=utf-8
import os
import pytest
from util.log import MyLog
from util.read_config import ReadConfig


class RunAll:
    def __init__(self):
        self.rc = ReadConfig()
        self.pro_dir = self.rc.project_dir
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

        self.report_xml_path = os.path.join(self.log.log_path, 'report\\xml')

        self.case_list_file = os.path.join(self.pro_dir, "caselist.txt")
        self.case_list = []

    def set_case_list(self):
        """将caselist.txt中的case名存到一个list，不包含以#开头的"""
        try:
            fb = open(self.case_list_file)
        except Exception as e:
            self.logger.error(str(e))
        else:
            for value in fb.readlines():
                data = str(value) + '.py'
                if data != '' and not data.startswith("#"):
                    data = './scripts/' + data
                    self.case_list.append(data.replace('\n', ''))
            fb.close()
        # return self.case_list

    def run(self):
        logger = self.logger
        rerun = self.rc.get_test("reruns")

        try:
            self.set_case_list()
            print(self.case_list)
            if self.case_list is not None:
                # logger.info("************start appium server**************")
                # try:
                #     os.system("start startAppiumServer.bat")
                # except Exception:
                #     logger.error("启动appium服务失败")
                # time.sleep(15)
                logger.info("************test start**************")
                pytest_list = ['-s', '-q']

                xml_dir = '--alluredir=' + self.report_xml_path
                reruns = '-reruns=' + rerun
                pytest_list.append(xml_dir)
                pytest_list.append(reruns)

                for case in self.case_list:
                    pytest_list.append(case)

                pytest.main(pytest_list)
            else:
                logger.info("Have no case to test")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("****************test end**********************")
            # os.system("start stopAppiumServer.bat")


if __name__ == '__main__':
    test = RunAll()
    test.run()




