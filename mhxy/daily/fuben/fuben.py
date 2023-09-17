import pyautogui

from mhxy import MhxyScript

DAILY_MISSION = "普通副本"
WEEKLY_MISSION = "侠士副本"


class Fuben(MhxyScript):

    def getTabName(self):
        pass

    # 4.打开任务按钮，查找对应的副本
    # 5.循环进入副本
    # 5.1 自动点击右上角对话
    # 5.2 对话快进
    # 5.3 进入战斗
    # 5.4 战斗结束，重复以上步骤
    # 5.5 副本结束，点击返回长安城
    # 5.6 进入下一个副本
    def do(self):
        # 1.找到选择副本按钮，并点击
        pyautogui.locateCenterOnScreen()
        # 2.判断是否需要切换tab

        # 判断是否有已完成按钮

        # 找到未完成的副本按钮，并点击


class DailyFuben(Fuben):

    def getTabName(self):
        return DAILY_MISSION


class WeeklyFuben(Fuben):

    def getTabName(self):
        return WEEKLY_MISSION
