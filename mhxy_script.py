import tkinter

from game_process import *
from mhxy_bangpai2 import *
from mhxy_fuben import *
from mhxy_ghost import *
from mhxy_haidi import *
from mhxy_menpai import *
from mhxy_mihunta import *
from mhxy_mine import *

_backgroundThread = None
_curScript = None
_changWinPos = True


class MyThread(threading.Thread):
    def __init__(self, target, daemon=True):
        super(MyThread, self).__init__(target=target, daemon=daemon)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()


def my_button(root, text, width, command):
    return tkinter.Button(root, text=text, width=width, bg='white', activebackground='grey', activeforeground='black',
                          font=('微软雅黑', 8),
                          command=command)


def change_thread(target):
    global _backgroundThread
    global _curScript
    if _backgroundThread is not None:
        # python只能通过标志符结束进程，部分程序没有设计结束标志。所以暂时放着不实现了。手动关闭窗口或者鼠标移动到边缘关闭吧
        if _curScript is not None:
            _curScript.stop()
        _backgroundThread.stop()
    _backgroundThread = MyThread(target=target.do, daemon=True)
    _backgroundThread.start()
    _curScript = target


def pack_stop():
    global bangpai_btn

    def change2None():
        global _backgroundThread
        global _curScript
        if _backgroundThread is not None:
            if _curScript is not None:
                _curScript.stop()
            _backgroundThread.stop()
        _backgroundThread = None

    bangpai_btn = my_button(root, text='停止当前任务', width=12, command=change2None)
    bangpai_btn.pack(side=tkinter.BOTTOM, expand=tkinter.NO)


def pack_ghost():
    def change_to_ghost():
        change_thread(Ghost(chang_window_position=_changWinPos))

    ghost_btn = my_button(root, text='捉鬼', width=8, command=change_to_ghost)
    ghost_btn.place(x=40, y=60, anchor=tkinter.NW)


def pack_fuben():
    def change2Fuben():
        change_thread(Fuben(change_window_position=_changWinPos))

    fubenBtn = my_button(root, text='副本', width=8, command=change2Fuben)
    fubenBtn.place(x=130, y=60, anchor=tkinter.NW)


def pack_menpai():
    def changMission():
        change_thread(Menpai(chang_window_position=_changWinPos))

    fubenBtn = my_button(root, text='门派', width=8, command=changMission)
    fubenBtn.place(x=40, y=100, anchor=tkinter.NW)


def pack_haidi():
    def changMission():
        change_thread(Haidi(chang_window_position=_changWinPos))

    fubenBtn = my_button(root, text='海底', width=8, command=changMission)
    fubenBtn.place(x=130, y=100, anchor=tkinter.NW)


def pack_mihunta():
    def changMission():
        change_thread(Mihunta(chang_window_position=_changWinPos))

    fubenBtn = my_button(root, text='迷魂塔', width=8, command=changMission)
    fubenBtn.place(x=40, y=140, anchor=tkinter.NW)


def pack_bangpai():
    global bangpai_btn

    def change_to_bangpai():
        change_thread(Bangpai(chang_window_position=_changWinPos))

    bangpai_btn = my_button(root, text='帮派任务', width=8, command=change_to_bangpai)
    bangpai_btn.place(x=130, y=140, anchor=tkinter.NW)


def pack_mine():
    def change_to_mine():
        change_thread(Mine(chang_window_position=_changWinPos))

    mine_btn = my_button(root, text='挖矿', width=8, command=change_to_mine)
    mine_btn.place(x=90, y=230, anchor=tkinter.NW)


# 界面程序 此部分封装了参数没有大量写死的程序 opencv 死活打包不进去
# pyinstaller --onefile --noconsole mhxy_script.py
# pyinstaller --onefile mhxy_script.py
if __name__ == '__main__':
    root = tkinter.Tk()
    # 标题
    root.title("梦幻手游脚本")
    # 图形界面的x,y轴长度
    x = int((root.winfo_screenwidth() - root.winfo_reqwidth()) / 2)
    y = int((root.winfo_screenheight() - root.winfo_reqheight()) / 2)
    # 设置窗口的大小和位置
    root.geometry("260x430+{}+{}".format(x, y))
    gameProcess = GameProcess()

    # 初始化为小窗口
    smallWinBtn = my_button(root, text='初始化为小窗口', width=12, command=gameProcess.move_zhuo_mian_ban)
    smallWinBtn.place(x=80, y=10, anchor=tkinter.NW)
    # 抓鬼
    pack_ghost()
    # 副本
    pack_fuben()
    # 门派
    pack_menpai()
    # 海底
    pack_haidi()
    # 迷魂塔
    pack_mihunta()
    # 帮派任务
    pack_bangpai()
    # 挖矿
    pack_mine()
    # 初始化为原始窗口
    originWinBtn = my_button(root, text='初始化为原始窗口', width=12, command=gameProcess.move_zhuo_mian_ban_to_origin)
    originWinBtn.place(x=80, y=180, anchor=tkinter.NW)
    # 说明
    t = tkinter.Text(root, width=32, height=10)
    t.insert(tkinter.END, "说明\n"
                          "1 如果出现后台运行的程序无法关闭情况，请通过关闭本窗口程序关闭正在运行的脚本。\n"
                          "2 程序不受控可以通过将鼠标快速移动到右上角强制终止。\n"
                          "3 对应功能程序配置文件和说明放在resources下相应文件夹内")
    t.place(x=10, y=270, anchor=tkinter.NW)
    # 停止当前任务
    pack_stop()
    root.mainloop()
