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
    xiaomi_8_uri =  "android://127.0.0.1:5037/208602d4?cap_method=&&ori_method=MINICAPORI&&touch_method=MAXTOUCH"
    uri =           "android://127.0.0.1:5037/127.0.0.1:62001?cap_method=&&ori_method=MINICAPORI&&touch_method=MINITOUCH"
    auto_setup(__file__, logdir=False, devices=[uri], project_root="C:/CODE/Airtest")

device: Android = connect_device(xiaomi_8_uri)
logger.info(device.display_info)

cok_gp = CokFarm("com.hcg.cok.cn1",
                 # target_resrc="铁",
                 device_=device)

# for _ in range(10):
#     cok_gp.kill_monster(1)
#     sleep(40)
# cok_gp.kill_griffin(30)
while True:
    # sleep(1.5 * 60 * 60)
    try:
        cok_gp.kill_monster(500)
    except Exception as e:
        logger.error(e)



touch(Template(r"tpl1689630190685.png", record_pos=(-0.433, 0.537), resolution=(1080, 2248)))
