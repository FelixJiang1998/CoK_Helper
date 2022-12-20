import cv2
from PIL import Image
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
import time


def crop_screenshot(img_file, pos_x, pos_y, width, height, out_file=None):
    img = Image.open(img_file)
    region = (pos_x, pos_y, pos_x + width, pos_y + height)
    crop_img = img.crop(region)
    if out_file is None:
        out_file = "tp" + str(time.time()) + ".png"
    crop_img.save(out_file)
    # print("exported:", out_file)


def get_cur_view(param):
    # 检测当前view
    if exists(Template(r"../images/mini_城内.png", record_pos=(-0.398, 0.935), resolution=(1080, 2248))):
        param["cur_view"] = 0
    elif exists(Template(r"../images/mini_城外.png", record_pos=(-0.392, 0.94), resolution=(1080, 2248))):
        param["cur_view"] = 1


def toggle_view(param, target_view=0):
    """
    切换view, 默认回主城
    """
    if param["cur_view"] != target_view:
        touch(v=(110, 2150))


def os_return():
    swipe(v1=(0, 1150), v2=(100, 1150))


