import datetime
import json
import logging
import threading
import time

import playsound as pl
import pyautogui
import pyperclip
from pygetwindow import PyGetWindowException, BaseWindow

from mhxy.frame import Frame

# 日志
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
# 创建一个处理器，用于写入日志文件
fileHandler = logging.FileHandler('mhxy_script.log')
fileHandler.setLevel(logging.DEBUG)
# 添加到 logger 中
logger.addHandler(fileHandler)

# 窗口左上侧位置 init后修改
frame = Frame(0, 0)

# 窗口固定大小
originSize = [1040, 807]
smallSize = (907, 707)
# 鼠标到变化态需要向做微调距离
resizeOffset = (10, 7)
frameSize = [0, 0]

frameOriginSizeCm = [28.1, 21.8]
frameSizeCm = [28.1, 21.8]


def relative_size(x, y):
    return (frameSize[0] * x / frameSizeCm[0],
            frameSize[1] * y / frameSizeCm[1])


def relative_x2_act(x_cm):
    return frameSize[0] * abs(x_cm) / frameSizeCm[0]


def relative_y2_act(yCm):
    return frameSize[1] * abs(yCm) / frameSizeCm[1]


def win_relative_x(x):
    return frame.right - relative_x2_act(x) if x < 0 else frame.left + relative_x2_act(x)


def win_relative_y(y):
    return frame.bottom - relative_y2_act(y) if y < 0 else frame.top + relative_y2_act(y)


def win_relative_xy(x, y):
    return win_relative_x(x), win_relative_y(y)


# 百分比方法不是很实用，因为窗口大小变化，ui并不是百分比变化的
def percent_x(x):
    return frameSize[0] * (abs(x) / 100)


def percent_y(y):
    return frameSize[1] * (abs(y) / 100)


def win_percent_x(x):
    return frame.right - percent_x(x) if x < 0 else frame.left + percent_x(x)


def win_percent_y(y):
    return frame.bottom - percent_y(y) if y < 0 else frame.top + percent_y(y)


def win_percent_xy(x, y):
    return win_percent_x(x), win_percent_y(y)


def battling(battling_pic=r'resources/origin/zhen_tian.png'):
    return Util.locate_on_screen(battling_pic) is not None


def not_battling(not_battling_pic):
    return Util.locate_on_screen(not_battling_pic) is not None


# 关闭任务侧边栏
def close_mission():
    Util.left_click(-7, 4.3)
    # print("关闭任务侧边栏")
    # pyautogui.hotkey('alt', 'p')


# 结束战斗后进行操作
def escape_battle_do(do,
                     not_battling_pic=None,
                     battling_pic=r'resources/small/enter_battle_flag.png',
                     battle_do_func=None):
    already_do = False
    battle_do = False
    while True:
        if (battling_pic is not None and not battling(battling_pic=battling_pic)) or \
                (not_battling_pic is not None and not_battling(not_battling_pic)):
            battle_do = False
            if not already_do:
                # 脱离战斗
                print("escape battle")
                cooldown(1.5)
                already_do = True
                do()
                cooldown(2)
            else:
                # 战斗外当已完成了动作
                cooldown(2)
        else:
            # 战斗中
            already_do = False
            if not battle_do:
                # 进入战斗
                print("enter battle")
                cooldown(3)
                battle_do = True
                # 进入战斗后做一次
                if battle_do_func is not None:
                    battle_do_func()
                cooldown(2)
            else:
                # 战斗中当已完成了动作
                cooldown(2)


def do_util_find_pic(pic, do, warn_times=None):
    def find():
        if isinstance(pic, list):
            for idx, each in enumerate(pic):
                locate = Util.locate_center_on_screen(each)
                if locate is not None:
                    return locate, idx
            return None, None
        else:
            return Util.locate_center_on_screen(pic), None

    locate, idx = find()
    # 最少执行一次
    times = 0
    while locate is None:
        do(locate, idx=idx, times=times)
        locate, idx = find()
        times += 1
        cooldown(1)
        if warn_times is not None and times > warn_times:
            alarm_clock = threading.Thread(target=pl.playsound('resources/common/music.mp3'))
            # 闹钟提醒
            alarm_clock.start()
    return locate, idx


def wait_util_find_pic(pic):
    def do():
        cooldown(1)

    return do_util_find_pic(pic, do)


# 副本式任务
def do_norm_fuben_mission():
    def reach():
        return Util.locate_center_on_screen(r'resources/fuben/select.png')

    # 流程任务
    def do():
        reach_position = reach()
        while reach_position is None:
            def click_skip():
                Util.left_click(-1, -2)

            # 找不到头像则正在对话点击头像位置跳过 直到找到头像位置
            do_util_find_pic(r'resources/avatar.png', click_skip)
            reach_position = reach()
            cooldown(2)
        pyautogui.leftClick(reach_position.x, reach_position.y)

    escape_battle_do(do)


def cooldown(second):
    time.sleep(max(0, second))


class Util:

    @staticmethod
    def __open_cv_enable():
        __openCVEnable = True
        try:
            import cv2
        except ImportError:
            __openCVEnable = False
        return __openCVEnable

    @staticmethod
    def locate_center_on_screen(pic, confidence=0.9):
        cfd = confidence if Util.__open_cv_enable() else None
        if isinstance(pic, list):
            res = None
            for i in pic:
                if cfd is not None:
                    res = pyautogui.locateCenterOnScreen(i, region=(frame.left, frame.top, frame.right, frame.bottom),
                                                         confidence=cfd)
                else:
                    res = pyautogui.locateCenterOnScreen(i, region=(frame.left, frame.top, frame.right, frame.bottom))
                if res is not None:
                    return res
            return res
        else:
            if cfd is not None:
                return pyautogui.locateCenterOnScreen(pic, region=(frame.left, frame.top, frame.right, frame.bottom),
                                                      confidence=cfd)
            else:
                return pyautogui.locateCenterOnScreen(pic,
                                                      region=(frame.left, frame.top, frame.right, frame.bottom))

    @staticmethod
    def locate_on_screen(pic, confidence=0.9):
        cfd = confidence if Util.__open_cv_enable() else None
        if cfd is not None:
            return pyautogui.locateOnScreen(pic, region=(frame.left, frame.top, frame.right, frame.bottom),
                                            confidence=cfd)
        else:
            return pyautogui.locateOnScreen(pic, region=(frame.left, frame.top, frame.right, frame.bottom))

    @staticmethod
    def left_click(x, y):
        pyautogui.leftClick(win_relative_x(x), win_relative_y(y))

    @staticmethod
    def double_click(x, y):
        pyautogui.doubleClick(win_relative_x(x), win_relative_y(y))

    @staticmethod
    def click(x, y, clicks, buttons):
        pyautogui.click(win_relative_x(x), win_relative_y(y), clicks=clicks, button=buttons)

    @staticmethod
    def click_picture(pic):
        locate, idx = wait_util_find_pic(pic)
        pyautogui.leftClick(locate.x, locate.y)

    @staticmethod
    def write(text):
        # 不支持中文
        # pyautogui.typewrite(text)
        pyperclip.copy(text)
        # print(pyperclip.paste())
        pyautogui.hotkey('Ctrl', 'v')


def resize_to_small(windows):
    while not windows.isActive:
        cooldown(1)
    pyautogui.moveTo(windows.right - resizeOffset[0], windows.bottom - resizeOffset[1])
    pyautogui.dragTo(windows.left + (smallSize[0] - resizeOffset[0]), windows.top + (smallSize[1] - resizeOffset[1]),
                     duration=1.3)


'''
@:param resizeToSmall 是否修改窗口为小窗口
@:param changWinPos 窗口位置是否发生移动
'''


def init(idx=0, resize_to_small=False, chang_window_position=True):
    global frameSizeCm
    global frame

    def get_frame_size(idx) -> BaseWindow:
        window = None
        while window is None or window.left < 0:
            windows_list = pyautogui.getWindowsWithTitle('梦幻西游：时空')
            windows_list = list(filter(lambda x: x.left > 0, windows_list))
            windows_list.sort(key=lambda x: x.left)

            moniqiWin = list(filter(
                lambda x: x.left > 0 and (x.title.startswith("MuMu模拟器12") or x.title.startswith("梦幻西游 - ")),
                pyautogui.getAllWindows()))
            moniqiWin.sort(key=lambda x: x.left)
            for each in moniqiWin:
                windows_list.append(each)

            if len(windows_list) > 0:
                window = windows_list[idx]
            cooldown(0.5)
        if window is not None:
            frameSize[0] = window.width
            frameSize[1] = window.height
        return window

    # 如果你是使用notepad++中添加命令运行则需要修改下工作目录，比如
    # os.chdir("D:\workspace\pyproject\mhxy_script")
    # pyautogui.PAUSE = 1  # 调用在执行动作后暂停的秒数，只能在执行一些pyautogui动作后才能使用，建议用time.sleep
    pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常

    # location1 = Util.locateOnScreen(r'resources/mine_head.png')
    windows = get_frame_size(idx)
    print("窗口大小:", frameSize)
    print("窗口大小CM:", frameSizeCm)
    if resize_to_small:
        resize_to_small(windows)
        windows = get_frame_size(idx)
        print("调整后窗口大小:", frameSize)
    if resize_to_small or frameSize[0] == smallSize[0]:
        frameSizeCm = [frameOriginSizeCm[0] * (smallSize[0] / originSize[0]),
                       frameOriginSizeCm[1] * (smallSize[1] / originSize[1])]
        print("调整后窗口大小CM:", frameSizeCm)
    else:
        frameSizeCm = frameOriginSizeCm
    try:
        windows.activate()
    except PyGetWindowException:
        pass
    if frame.left == 0 or chang_window_position:
        frame.left = windows.left
        frame.top = windows.top
        frame.right = frame.left + frameSize[0]
        frame.bottom = frame.top + frameSize[1]
        print("窗口四角位置:", frame)


def parse_request(request):
    raw_list = request.split("\r\n")
    # GET /search?sourceid=chrome&ie=UTF-8&q=ergterst HTTP/1.1
    fst = raw_list[0].split(' ')
    request = {"method": fst[0], "url": fst[1]}
    for index in range(1, len(raw_list)):
        item = raw_list[index].split(":")
        if len(item) == 2:
            request.update({item[0].lstrip(' '): item[1].lstrip(' ')})
    return request


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class PicNode(object):

    def __init__(self, elem, completeFunc=None):
        if completeFunc is None:
            self.completeFunc = self.complete
        else:
            self.completeFunc = completeFunc
        self.elem = elem
        # [PicNode]
        self.next = None

    def complete(self, locate, chaseWin):
        pyautogui.leftClick(locate.x, locate.y)
        cooldown(0.5)
        # 叶子节点需要关闭对话
        Util.left_click(chaseWin[0], chaseWin[1])

    def setNext(self, nxt):
        self.next = nxt
        # 防止卡了的情况，自己下一个包含自己
        self.next.append(self)

    def __str__(self) -> str:
        return str(self.elem)


class MhxyScriptInterrupt(Exception):
    pass


class MhxyScript:
    # 程序运行标志
    _flag = True

    def __init__(self, idx=0, chang_window_position=True, resize_to_small=False) -> None:
        init(idx=idx, resize_to_small=resize_to_small, chang_window_position=chang_window_position)

    def interrupt_work(self):
        raise MhxyScriptInterrupt()

    def stop(self):
        self._flag = False

    def do(self):
        pass
