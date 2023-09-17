from mhxy import *

# 使用搜索截胡商品
class Shopping3:
    _approached = False
    _startTime = None

    def __init__(self) -> None:
        init()
        now = datetime.datetime.now()
        self._startTime = datetime.datetime(now.year, now.month, now.day, 0, 40)
        self._time = self._startTime + datetime.timedelta(hours=1, minutes=2)
        super().__init__()

    def _refresh(self):
        cooldown(0.2)
        Util.left_click(5, 7)
        cooldown(0.2)
        Util.left_click(23, 18.5)

    def _buy(self):
        print("购买商品")
        cooldown(0.1)
        buyTab = (frame.right - relative_x2_act(5), frame.bottom - relative_y2_act(3))
        pyautogui.leftClick(buyTab[0], buyTab[1])
        cooldown(0.1)
        # confirmTab = (frame.py.left + relativeX2Act(13.5), frame.py.top + relativeY2Act(8.5))
        confirmTab = (frame.left + relative_x2_act(8), frame.top + relative_y2_act(14))
        pyautogui.leftClick(confirmTab[0], confirmTab[1])

    def _timeApproach(self):
        now = datetime.datetime.now()
        # 三分钟开始刷新页面
        sj1 = now - datetime.timedelta(minutes=2)
        sj2 = now + datetime.timedelta(minutes=1)
        # 三分钟内
        if sj1 < self._time and sj2 > self._time:
            self._approached=True
            return True
        return False

    def close(self):
        cooldown(2)
        Util.left_click(-2.5, 3.5)
        cooldown(2)

    class _End(Exception):
        pass

    def shopping3(self):
        while True:
            while self._timeApproach():
                # 找三次是否有商品
                itemPic = r'resources/shop/item_3.png'
                point = Util.locate_center_on_screen(itemPic)
                # 两次都没有刷新列表
                if point is None:
                    self._refresh()
                else:
                    # 如果有则购买
                    pyautogui.leftClick(point.x, point.y)
                    self._buy()
                    break
                cooldown(1.5)
            if self._approached:
                break
            cooldown(60)

# 不关注、靠搜索抢
if __name__ == '__main__':
    pyautogui.PAUSE = 0.2
    # pyautogui.PAUSE = 2
    print("start task....")
    Shopping3().shopping3()
