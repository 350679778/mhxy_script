import pyautogui
import pyperclip
from mhxy import *


def __open_cv_enable():
    __openCVEnable = True
    try:
        import cv2
    except ImportError:
        __openCVEnable = False
    return __openCVEnable

def locate_center_on_screen(frame, pic, confidence=0.9):
    cfd = confidence if __open_cv_enable() else None
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

def locate_on_screen(frame, pic, confidence=0.9):
    cfd = confidence if __open_cv_enable() else None
    if cfd is not None:
        return pyautogui.locateOnScreen(pic, region=(frame.left, frame.top, frame.right, frame.bottom),
                                        confidence=cfd)
    else:
        return pyautogui.locateOnScreen(pic, region=(frame.left, frame.top, frame.right, frame.bottom))

def left_click(x, y):
    pyautogui.leftClick(win_relative_x(x), win_relative_y(y))

def double_click(x, y):
    pyautogui.doubleClick(win_relative_x(x), win_relative_y(y))

def click(x, y, clicks, buttons):
    pyautogui.click(win_relative_x(x), win_relative_y(y), clicks=clicks, button=buttons)

def click_picture(pic):
    locate, idx = wait_util_find_pic(pic)
    pyautogui.leftClick(locate.x, locate.y)

def write(text):
    # 不支持中文
    # pyautogui.typewrite(text)
    pyperclip.copy(text)
    # print(pyperclip.paste())
    pyautogui.hotkey('Ctrl', 'v')

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