# -*- encoding=utf8 -*-
__author__ = "FelixJ"

import logging
import sys

sys.path.append("./src/")
sys.path.append("./images/")
from CokFarm import *

logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)

if not cli_setup():
    # uri = "android://127.0.0.1:5037/127.0.0.1:62001?cap_method=&&ori_method=MINICAPORI&&touch_method=MINITOUCH"
    uri = "android://127.0.0.1:5037/208602d4?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MAXTOUCH"

    auto_setup(__file__, logdir=False, devices=[uri,], project_root="C:/CODE/Airtest")

# script content
print("start...")
device: Android = connect_device(uri)

logger.info(device.display_info)

cok_9u = CokFarm("com.hcg.cok.uc",
                #  target_resrc="铁",
                 device_=device)
cok_gp = CokFarm("com.hcg.cok.cn1",
                 # target_resrc="铁",
                 device_=device)
cnt = 0 
while True:
    try:
        cnt += 1
        # cok_9u.kill_monster(5),
        # sleep(60)
        logger.info("第{}次执行开始".format(cnt))
        cok_9u.run()
        
        # # sleep(60)
        # cok_gp.run(is_prod=False, collect_number=5)
        # cok_gp.run(collect_number=4)
        cok_gp.run()
        

        # stop the app for stability after 5 times
        if cnt % 5 == 0: 
            stop_app(cok_9u.app_name)
            # cok_gp.run()
            stop_app(cok_gp.app_name)
        logger.info("第{}次执行结束".format(cnt))
    except Exception as e:
        logger.error(e)
    finally:

        sleep(30 * 60)

# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)
# print(cok_gp.device.
# get_top_activity_name())