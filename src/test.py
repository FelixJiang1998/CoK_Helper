from airtest.core.android.android import Android
from airtest.core.api import *


# # print(device.get_top_activity_name())
# # print(device.is_locked())
# # print(device.display_info)
# # print(device.unlock())
# # print(device.get_current_resolution())
# # print(device.get_render_resolution())
# # device.shell("adb shell input keyevent 26")
#
# uri = "android://127.0.0.1:5037/208602d4?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MAXTOUCH"
uri = r"android://127.0.0.1:5037/127.0.0.1:62001?cap_method=JAVACAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH"
auto_setup(__file__, logdir=True, devices=[uri], project_root="C:/CODE/Airtest")
device: Android = connect_device(uri)
print(device.display_info)
print(device.get_top_activity_name())
#
# # pos = exists(Template(r"btn_占领.png", threshold=0.9, record_pos=(0.043, -0.06), resolution=(1080, 2248)))
# # if pos:
# #     touch(pos)
# # else:
# #     raise TargetNotFoundError()
#
# # touch((70, 1703))
#
# # from CokFarm import CokFarm
# # cok = CokFarm("com.hcg.cok.uc")
# # cok.toggle_view(1)
#
# print(device.get_top_activity_name())
#
import collections
from typing import *
from collections import *


def sumPrefixScores(words: List[str]) -> List[int]:
    n = len(words)
    if n == 1: return [len(words[0])]

    ans = []
    temp = defaultdict(lambda: [])

    # for i, word in enumerate(words):
    #     cnt = 0
    #     temp[i].append(word)
    #     for j in range(len(word)):
    #         temp[i].append(word[:-j])
    #         for k in range(n):
    #             if i != k and words[k].startswith():
    #                 cnt += 1
    #     ans.append(cnt)

    # for i, word in enumerate(words):
    #     temp[i].append(word)
    #     for j in range(1, len(word)):
    #         temp[i].append(word[:-j])
    # for i in range(n):
    #     cnt = 0
    #     for j in range(n):
    #         for pre in temp[i]:
    #             if words[j].startswith(pre):
    #                 cnt += 1
    #     ans.append(cnt)
    def cntPre(pre: str, words: List[str]):
        cnt = 0
        for w in words:
            if w.startswith(pre):
                cnt += 1
        return cnt

    for i, word in enumerate(words):
        c = cntPre(word, words)
        for j in range(1, len(word)):
            c += cntPre(word[:-j], words)
        ans.append(c)
    return ans


# inpu = ["abc", "ab", "bc", "b"]
# print(sumPrefixScores(inpu))


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def reverseOddLevels(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if root is None:
        return
    res = []
    node_que = deque()
    node_que.append(root)
    # node_que = [root]
    while node_que:
        node = node_que.popleft()
        res.append(node.val)
        if node.left:
            node_que.append(root.left)
        if node.right:
            node_que.append(root.right)
    print(res)


def gen(arr, i):
    if i < len(arr):
        tn = TreeNode(val=arr[i]) if arr[i] else None
        if tn is not None:
            tn.left = gen(arr, 2 * i + 1)
            tn.right = gen(arr, 2 * i + 2)
        return tn


# inpu = [2, 3, 5, 8, 13, 21, 34]
# reverseOddLevels(gen(inpu, 0))


l = []
l.sort(reverse=True)
