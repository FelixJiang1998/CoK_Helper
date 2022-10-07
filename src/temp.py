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

device: Android = connect_device(uri)
logger.info(device.display_info)

cok_gp = CokFarm("com.hcg.cok.gp",
                 # target_resrc="铁",
                 device_=device)

cok_gp.kill_monster(20)
# cok_gp.kill_griffin(20)
