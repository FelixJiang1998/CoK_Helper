# # -*- encoding=utf8 -*-
# __author__ = "FelixJ"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
from airtest.core.android.android import Android
# from airtest.core.android.adb import ADB
# from CommonUtils import *
import cv2
from PIL import Image
import logging
import typing

logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)

resource = ['木', "粮", "铁", "银"]


class CokFarm(object):
    param = None
    device = None
    app_name = None

    def __init__(self, target_app_name="com.hcg.cok.uc", target_resrc="银", device_=None):
        """
           display_info - {'width': 1080, 'height': 2248, 'density': 2.75, 'orientation': 0, 'rotation': 0, 'max_x': 1079, 'max_y': 2247}

        """

        self.device: Android = device() if device_ is None else device_
        assert self.device is not None
        self.app_name = target_app_name
        self.param = self.device.display_info
        self.param["center"] = (self.param["max_x"] // 2, self.param["max_y"] // 2)
        self.target_resrc = target_resrc

    def collect_resource(self, target_march_size=6):
        """
            默认空闲状态为采集
            行动步骤：
            1. 切换到世界
            2. 检测剩余队列
        """
        logger.error("当前任务：采集")
        self.toggle_view(target_view=1)
        # 放大视图
        self.zoom_in()
        loop_cnt = 0

        is_march_list_expanded = False
        march_size = 0
        while True:
            loop_cnt += 1

            # 队列未满

            if loop_cnt > 7:
                logger.error("收集资源任务部署完成")
                break

            logger.info("开始搜索资源,当前循环数：{}".format(loop_cnt))

            self.get_cur_view()
            self.toggle_view(1)

            # 展开队列
            if not is_march_list_expanded:
                pos = exists(
                    Template(r"../images/队列识别.png", threshold=0.8, record_pos=(-0.384, -0.569),
                             resolution=(1080, 2248)))
                if pos:
                    logger.debug("展开队列显示")
                    touch(pos)

                is_march_list_expanded = True
            else:
                # 更新队列数量
                march_list = find_all(
                    Template(r"../images/队列状态_返回.png", rgb=True, threshold=0.7, record_pos=(-0.135, -0.462),
                             resolution=(1080, 2248)))
                march_size = len(march_list) if march_list else 0
                march_list = find_all(
                    Template(r"../images/队列状态_加速.png", rgb=True, threshold=0.7, record_pos=(-0.135, -0.462),
                             resolution=(1080, 2248)))
                march_size += len(march_list) if march_list else 0

            if march_size and march_size >= target_march_size:
                logger.error("当前队列数量已满:{}".format(march_size))
                break

            # 开始搜索
            touch((70, 1703))
            sleep(1)

            swipe(v1=(980, 1750), v2=(500, 1750))
            sleep(1)
            #             exists(Template(r"tpl1663827084320.png", record_pos=(-0.059, 0.564), resolution=(1080, 2248)))

            pos = exists(Template(r"../images/搜索_{}.png".format(self.target_resrc),
                                  record_pos=(-0.104, 0.526),
                                  resolution=(1080, 2248)))
            if pos:
                touch(pos)
            else:
                logger.error("搜索框匹配失败")
                continue
            # 确认搜索
            touch((600, 2090))
            sleep(1.5)

            # 点击找到的资源 - 在屏幕中心点
            touch((self.param["max_x"] // 2, self.param["max_y"] // 2))
            sleep(1)
            pos = exists(Template(r"../images/btn_占领.png", threshold=0.7, record_pos=(0.043, -0.06),
                                  resolution=(1080, 2248)))
            if pos:
                touch(pos)
            else:
                continue

            pos = exists(
                Template(r"../images/出征界面检测.png", record_pos=(-0.001, -0.903), resolution=(1080, 2248)))
            if not pos:
                logger.error("未进入出征")
                # if march_size < target_march_size:
                # 猜测没田了 todo
                # self.target_resrc = "铁" if self.target_resrc == "银" else "银"
                continue

            # 选择兵种优先级 -> 速度优先 todo 目前与分辨率绑定，待优化
            touch((120, 2100))
            touch((110, 1960))
            # 出征
            touch((900, 2100))
            march_size += 1

            logger.error("当前队列数：{}".format(march_size))
            if march_size >= target_march_size:
                break

    def collect_production(self):
        error_cnt = 0
        logger.error("收集自产开始")
        self.toggle_view(0)
        assert self.param["cur_view"] == 0
        while error_cnt < 5:
            error_cnt += 1

            if self.app_name not in self.device.get_top_activity_name():
                self.launch_app()

            pos = exists(Template(r"../images/侧边按钮_缩起.png", threshold=0.5, rgb=True, record_pos=(-0.432, 0.38),
                                  resolution=(1080, 2248)))
            if pos:
                touch(pos)
            else:
                pos = exists(
                    Template(r"../images/侧边按钮_展开.png", threshold=0.5, rgb=True, record_pos=(-0.434, 0.374),
                             resolution=(1080, 2248)))
                if pos:
                    touch(pos)
                    touch(pos)
                else:
                    logger.error("未找到按钮")

                    if error_cnt > 3:
                        stop_app(self.app_name)
                        error_cnt = 0
                    self.toggle_view(0)
                    continue
            logger.info("猜测按钮已经展开")
            swipe(v1=(80, 1350), v2=(80, 1100))
            sleep(0.5)
            # touch((75, 1550))
            touch((pos[0], pos[1] - 175))
            sleep(0.5)
            if exists(
                    Template(r"../images/领地辅助_界面检测.png", record_pos=(-0.007, -0.899), resolution=(1080, 2248))):
                logger.info("进入领地辅助")
                break

        touch((550, 2060))
        logger.info("执行中")
        sleep(15)
        self.os_return()
        self.os_return()
        logger.error("收集自产结束")

    def kill_monster(self, total=10):

        cnt = 0
        while True:
            # launching thing
            if self.app_name not in self.device.get_top_activity_name():
                self.launch_app()

            if cnt >= total:
                break
            if cnt > 10 and cnt % 10 == 0:
                self.get_energy()
            if cnt and cnt % 6 == 0:  # 每6队休息15s
                logger.error("进度{}/{}".format(cnt, total))
                sleep(15)

            self.toggle_view(1)

            # 寻找野怪
            touch((70, 1703))
            sleep(0.5)

            pos = exists(Template(r"../images/搜索_野怪.png", record_pos=(-0.411, 0.564), resolution=(1080, 2248)))
            if pos:
                touch(pos)
            else:
                continue

            touch((600, 2090))
            sleep(1)

            pos = exists(Template(r"../images/野怪_攻击.png", resolution=(1080, 2248)))
            if pos:
                touch(pos)
            else:
                # 点击找到的资源 - 在屏幕中心点
                touch((self.param["max_x"] // 2, self.param["max_y"] // 2))
                pos = exists(Template(r"../images/野怪_攻击.png", resolution=(1080, 2248)))
                if pos:
                    touch(pos)
                else:
                    continue

            # 检测出征
            pos = exists(
                Template(r"../images/出征界面检测.png", record_pos=(-0.001, -0.903), resolution=(1080, 2248)))
            if not pos:
                logger.error("未进入出征")
                continue

            # 选择兵种优先级 -> 速度优先
            touch((120, 2100))
            touch((110, 1960))
            # 出征
            touch((900, 2100))

            cnt += 1

    def get_cur_view(self):
        """先检测app装态检测当前view"""
        if self.app_name not in self.device.get_top_activity_name():
            logger.error("app已退出")
            self.launch_app()

        logger.error("检测当前view")

        if exists(Template(r"../images/mini_城内.png", threshold=0.7, rgb=True, record_pos=(-0.398, 0.935),
                           resolution=(1080, 2248))):
            logger.info("现在在城内")
            self.param["cur_view"] = 0
            return 0
        elif exists(Template(r"../images/mini_城外.png", threshold=0.7, rgb=True, record_pos=(-0.392, 0.94),
                             resolution=(1080, 2248))):
            logger.info("现在在城外")
            self.param["cur_view"] = 1
            return 1
        else:
            logger.error("检测不到所处界面")
            if self.app_name not in self.device.get_top_activity_name():
                self.launch_app()
            else:
                logger.error("Unknown error")
                # stop_app(self.app_name)
            self.param["cur_view"] = 2
            return None

    def toggle_view(self, target_view=0):
        if self.app_name not in self.device.get_top_activity_name():
            self.launch_app()
        logger.error("开始切换视图，目标为：{}".format(target_view))
        """
        切换view, 默认回主城
        """
        # if "cur_view" not in self.param:
        self.get_cur_view()
        while self.param["cur_view"] != target_view:

            if self.param["cur_view"] == 2:
                # 处于特殊界面中
                self.app_return()
                self.get_cur_view()
            else:  # target_view in [0, 1]
                touch(v=(110, 2150))
                sleep(2)
                # 更新所在视图
                self.get_cur_view()

    def launch_app(self):
        if self.app_name in self.device.get_top_activity_name():
            return

        start_app(self.app_name)
        sleep(5)
        attemp_times = 0
        while True:
            if exists(Template(r"../images/内城城堡.png", threshold=0.5, record_pos=(-0.218, -0.121),
                               resolution=(1080, 2248))):
                break
            self.os_return()
            sleep(5)
            attemp_times += 1

            if attemp_times > 2:
                if self.app_name in self.device.get_top_activity_name():
                    return
                else:
                    logger.error("启动失败")
                    self.launch_app()

    def zoom_in(self):
        pinch(
            center=(self.param["max_x"] // 2, self.param["max_y"] // 2),
            in_or_out="out"
        )

    def os_return(self):
        """系统的返回手势"""
        # swipe(v1=(0, self.param["max_y"] // 2), v2=(self.param["max_x"] // 2, self.param["max_y"] // 2))
        assert self.device is not None
        keyevent("4")
        sleep(0.5)

    def app_return(self):
        self.os_return()
        # touch((75,175)) # 点左上角
        # self.os_return()
        # pos = Template(r"特殊界面.png", record_pos=(-0.434, -0.903), resolution=(1080, 2248))
        # if pos:
        #     touch(pos)

    def run(self, is_prod=True, collect_number=6):
        wake()
        #     cok.device.unlock()
        self.launch_app()

        # 收集自产
        if is_prod:
            self.collect_production()
        # 采集
        if collect_number:
            self.collect_resource(collect_number)

        logger.error("{}任务完成".format(self.app_name))
        stop_app(self.app_name)
        home()

    def kill_griffin(self, total=3):
        if self.app_name not in self.device.get_top_activity_name():
            self.launch_app()

        i = 0
        while i < total:
            self.toggle_view(1)
            # 搜索
            touch((70, 1703))
            sleep(1)
            touch((270, 1730))
            sleep(0.5)
            touch((600, 2090))  # 确认查找button
            sleep(0.7)
            touch(self.param["center"])
            sleep(1)
            touch((520, 1575))
            sleep(0.7)

            touch((350, 1108))
            sleep(0.5)
            touch((850, 2150))
            sleep(0.7)
            keyevent("4")

            i += 1
            if i and i % 6 == 0:
                self.get_energy()
            if i and i % 3 == 0:
                logger.error("当前进度{}/{}".format(i, total))
                sleep(2 * 60)

    def get_energy(self, value=10):
        touch((80, 150))  # 头像
        sleep(0.5)
        touch((950, 1200))  # 体力
        sleep(0.5)
        touch((850, 610))  # 使用10
        sleep(0.5)
        touch((745, 1200))
        sleep(0.5)
        logger.error("补充体力100点")
        text("0")
        sleep(0.5)
        touch((750, 1350))
        sleep(0.5)
        self.app_return()
        self.app_return()


if __name__ == '__main__':
    if not cli_setup():
        xiaomi_8_uri = "android://127.0.0.1:5037/208602d4?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MAXTOUCH"
        nox_uri = "android://127.0.0.1:5037/127.0.0.1:62001?cap_method=JAVACAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH"

        logger.error("auto setup")

        auto_setup(__file__, logdir=True,
                   devices=[xiaomi_8_uri, ],
                   project_root="C:/CODE/Airtest")
        simple_report(__file__, logpath=True)
    #         connect_device(nox_uri)
    device = device()
    cok_9u = CokFarm("com.hcg.cok.uc",
                     target_resrc="铁",
                     device_=device)
    cok_cn = CokFarm("com.hcg.cok.cn1",  # 国服
                     target_resrc="银",
                     device_=device)
    logger.info(cok_9u.device.display_info)
    cok_9u.run()
    cok_cn.run()

    # cok.device.keyevent("26")
