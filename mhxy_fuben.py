import os
import sys
from configparser import ConfigParser

from mhxy import *

'''
副本实现逻辑：
1.构造方法中找到游戏的窗口，读取resource中的配置信息，再定位副本图片的位置
2.调用do()方法，循环执行副本
'''


class Fuben(MhxyScript):
    # 暂时没用，请忽视
    xiashi_fix = 5.6 + 0
    _fubenIdx = 0
    fuben_position = [
        ("xiashi", 13, 15),
        ("xiashi", 7, 15),

        ("norm", 19, 15),
        ("norm", 13, 15),
        ("norm", 7, 15)
    ]
    config = {
        'lastFuben': r'resources/small/fuben_flag.png'
    }

    def __init__(self, idx=0, change_window_position=True, resize_to_small=False) -> None:
        super().__init__(idx, change_window_position, resize_to_small)
        # 读取副本资源中的ini文件
        file_path = os.path.join(os.path.abspath('.'), 'resources/fuben/fuben.ini')
        if not os.path.exists(file_path):
            raise FileNotFoundError("文件不存在")
        conn = ConfigParser()
        conn.read(file_path)
        type = int(conn.get('main', 'type'))
        if type >= 4:
            self.fuben_position = [self.fuben_position[1], self.fuben_position[2], self.fuben_position[3],
                                   self.fuben_position[4]]
        elif type == 3:
            self.fuben_position = [self.fuben_position[2], self.fuben_position[3], self.fuben_position[4]]
        elif type == 2:
            self.fuben_position = [self.fuben_position[3], self.fuben_position[4]]
        elif type == 1:
            self.fuben_position = [self.fuben_position[1], self.fuben_position[3], self.fuben_position[4]]

    def _changan(self):
        return util.locate_center_on_screen(r'resources/fuben/activity.png')

    def do(self):
        while self._do() and self._flag:
            cooldown(2)

    # 流程任务
    def _do(self):
        #  进入第一个副本为起点
        self.do_until_to_changan()

        if self._fubenIdx >= len(self.fuben_position):
            return False
        # elif self.fubenPos[self._fubenIdx][0] == "xiashi":
        #     # 已领取的侠士任务所在坐标
        #     util.leftClick(-3, self.xiashi_fix)
        #     cooldown(2.0)
        #     util.leftClick(self.fubenPos[self._fubenIdx][1], self.fubenPos[self._fubenIdx][2])
        #     self._fubenIdx += 1
        #     print("下一个副本" + str(print("下一个副本" + str())))
        else:
            cooldown(1)
            util.left_click(7.5, 1.5)
            cooldown(0.5)
            util.left_click(3, 4.5)
            cooldown(1)
            lastFuben = util.locate_center_on_screen(self.config['lastFuben'])
            i = 0
            while lastFuben is None and i in range(0, 2):
                pyautogui.moveTo(util.win_relative_x(10), util.win_relative_y(10))
                pyautogui.dragTo(util.win_relative_x(10), util.win_relative_y(4.6), duration=0.8)
                cooldown(1.5)
                lastFuben = util.locate_center_on_screen(self.config['lastFuben'])
                i += 1
            if lastFuben is not None:
                cooldown(1)
                pyautogui.leftClick(lastFuben.x + util.relative_x2_act(3), lastFuben.y + util.relative_y2_act(0.2))
                cooldown(5)
                se = util.locate_center_on_screen(r'resources/fuben/selectfuben.png')
                #  11
                pyautogui.leftClick(se.x, se.y)
                cooldown(2)
                if self.fuben_position[self._fubenIdx][0] == "xiashi":
                    util.left_click(9, 5)
                    cooldown(1)
                # 下一个副本
                util.left_click(self.fuben_position[self._fubenIdx][1], self.fuben_position[self._fubenIdx][2])
                self._fubenIdx += 1
                print("下一个副本" + str(self._fubenIdx))
        return True

    def login_in(self):
        cooldown(1)
        login_in_button = util.locate_center_on_screen(r'resources/fuben/loginin.png')
        if login_in_button is not None:
            pyautogui.leftClick(login_in_button.x, login_in_button.y)
        cooldown(5)
        util.left_click(12, 13.5)

    def click_skip(self, locate, idx, times):
        if not self._flag:
            sys.exit(0)
        reachPos = util.locate_center_on_screen(r'resources/fuben/select.png')
        if reachPos is not None:
            # 对话
            pyautogui.leftClick(reachPos.x, reachPos.y + util.relative_y2_act(1.5))
        elif util.locate_center_on_screen(r'resources/fuben/skipJuqing.png') is not None:
            # 跳过剧情动画
            util.left_click(-3, 7)
        elif util.locate_center_on_screen(r'resources/small/blood.png') is None:
            # 阅读剧情
            util.left_click(-3, 1.8)
        else:
            # 追踪任务 如果 xiashi_fix 不是在第一个任务，可能会使得 到长安点到第一个任务出现弹窗使得脚本出错，此时确认下没到达长安，可降低发生的概率
            if self.xiashi_fix < 6 or self._changan() is None:
                util.left_click(-3, 5.5)
        cooldown(1)

    def do_until_to_changan(self):
        changan_position = self._changan()
        while changan_position is None:
            # 找不到头像则正在对话点击头像位置跳过 直到找到头像位置
            do_util_find_pic([r'resources/small/enter_battle_flag.png', r'resources/fuben/activity.png'],
                             self.click_skip, warn_times=10)
            changan_position = self._changan()
            cooldown(2)


# 副本 进入第一个副本为起点 小窗口
if __name__ == '__main__':
    pyautogui.PAUSE = 0.2
    print("start task....")
    Fuben().do()
