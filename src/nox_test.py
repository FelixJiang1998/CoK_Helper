# -*- encoding=utf8 -*-
__author__ = "FelixJ"

# import logging
import sys

sys.path.append("./src/")
sys.path.append("./images/")
from CokFarm import *

logger = logging.getLogger("airtest")
logger.setLevel(logging.INFO)

if not cli_setup():
    uri = "android://127.0.0.1:5037/127.0.0.1:62001?cap_method=&&ori_method=MINICAPORI&&touch_method=MINITOUCH"
    auto_setup(__file__, logdir=False, devices=[uri], project_root="C:/CODE/Airtest")

# script content
print("start...")
device: Android = connect_device(uri)
logger.info(device.display_info)

cok_9u = CokFarm("com.hcg.cok.uc", device_=device)
cok_gp = CokFarm("com.hcg.cok.gp",
                 # target_resrc="铁",
                 device_=device)

while True:
    # sleep(1.5 * 60 * 60)
    try:
        # cok_9u.kill_monster(5)
        sleep(60)
        cok_9u.run()
        # cok_gp.kill_monster(10)
        sleep(60)
        # cok_gp.run(is_prod=False, collect_number=5)
        cok_gp.run()
    finally:
        sleep(30 * 60)

# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)
# print(cok_gp.device.get_top_activity_name())