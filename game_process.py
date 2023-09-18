import os
import sys

import pygetwindow

from mhxy import *

# 所有窗口
windows = []
frames = []

def get_all_mhxy_frames() -> frames:
    """
    获取到所有的梦幻西游的窗口
    :rtype: Frame
    """
    global windows
    windows = pygetwindow.getWindowsWithTitle("梦幻西游：时空")

    for window in windows:
        frames.append(Frame(window))
    return frames

class GameProcess:
    _moveOffset = (60, 20)

    '''
    初始化为小窗口
    size为init.py中设置的窗口大小
    '''

    def __move_zhuo_mian_ban_func(self, size):
        global windows
        windows = pyautogui.getAllWindows()
        zhuomianban = (71, 963)
        i = 0
        for item in list(filter(lambda window: window.title.startswith("梦幻西游："), windows)):
            item.activate()
            print(f"当前拖拽窗口：{item}")
            if item.left < 0:
                print("notSafe")
            # 调整游戏窗口大小
            pyautogui.moveTo(item.right - resizeOffset[0], item.bottom - resizeOffset[1])
            pyautogui.dragTo(item.left + (size[0] - resizeOffset[0]), item.top + (size[1] - resizeOffset[1]),
                             duration=1)
            # 调整窗口位置
            pyautogui.moveTo(item.left + self._moveOffset[0], item.top + self._moveOffset[1])
            cooldown(1)
            pyautogui.dragTo(zhuomianban[i] + self._moveOffset[0], 0 + self._moveOffset[1], duration=1)
            i += 1
            print("处理后：", item)

    # 初始化为小窗口
    def move_zhuo_mian_ban(self):
        self.__move_zhuo_mian_ban_func(smallSize)

    # 初始化为原始窗口
    def move_zhuo_mian_ban_to_origin(self):
        windows = pyautogui.getAllWindows()
        item = list(filter(lambda x: x.title.startswith("梦幻西游"), windows))[0]
        item.activate()
        print(item)
        pyautogui.moveTo(item.right - resizeOffset[0], item.bottom - resizeOffset[1])
        pyautogui.dragTo(item.left + (originSize[0] - resizeOffset[0]), item.top + (originSize[1] - resizeOffset[1]),
                         duration=1)
        cooldown(3)
        print("处理后：", item)

    '''
    移动模拟器
    '''

    def move_mo_ni_qi(self):
        self.__move_mo_ni_qi_func(smallSize)

    '''
    移动模拟器
    '''

    def __move_mo_ni_qi_func(self, size):
        windows = pyautogui.getAllWindows()
        i = 0
        for item in list(
                filter(lambda x: x.title.startswith("MuMu模拟器12") or x.title.startswith("梦幻西游 - "), windows)):
            item.activate()
            print(item)
            if item.left < 0:
                print("notSafe")
            pyautogui.moveTo(item.right - 5, item.top + 15)
            pyautogui.dragTo(item.left + (size[0] - 5), item.top + 15,
                             duration=1)
            i += 1
            print("处理后：", item)

    '''
    关闭模拟器
    '''

    def close_mo_ni_qi(self):
        # 根据进程名杀死进程 NemuPlayer.exe QtWebEngineProcess.exe NemuHeadless.exe || mymain.exe CCMini.exe
        pro = 'taskkill /f /im %s' % 'NemuHeadless.exe'
        os.system(pro)
        pro = 'taskkill /f /im %s' % 'QtWebEngineProcess.exe'
        os.system(pro)


if __name__ == '__main__':
    type = int(0 if len(sys.argv) <= 1 else sys.argv[1])
    resize = GameProcess()
    if type == 0:
        resize.move_zhuo_mian_ban()
    else:
        resize.move_zhuo_mian_ban_to_origin()
    # 模拟器分辨率设置为：1600*1095 再调整窗口大小可使用脚本
    # resize.moveMoniqi()
