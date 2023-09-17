from mhxy import *


class Hanhua:
    def hanhua(self):
        while True:
            Util.left_click(9, 2)
            Util.left_click(3.5, 11.5)
            # 第二个 14 第一个 x 9
            Util.left_click(9, 12)
            Util.left_click(11, 2)
            cooldown(4)

    def hanhuaWithText(self):
        cooldown(3)
        Util.write("哈哈哈哈哈")
        # while True:
        #     Util.leftClick(5, 2)
        #     cooldown(1)
        #     Util.write("哈哈哈哈哈")
        #     cooldown(1)
        #     Util.leftClick(13, 2)
        #     cooldown(2)


# 喊话
if __name__ == '__main__':
    Util.PAUSE = 0.2
    print("start task....")
    init(resize_to_small=True)
    Hanhua().hanhua()
