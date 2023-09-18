import random
from tkinter import ttk
import tkinter

import game_process
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


def pack_stop(x, y):
    def change_to_none():
        global _backgroundThread
        global _curScript
        if _backgroundThread is not None:
            if _curScript is not None:
                _curScript.stop()
            _backgroundThread.stop()
        _backgroundThread = None

    stop_btn = my_button(root, text='停止当前任务', width=12, command=change_to_none)
    stop_btn.place(x=x, y=y, anchor=tkinter.NW)


def button_ghost(x, y):
    def change_to_ghost():
        change_thread(Ghost(chang_window_position=_changWinPos))

    ghost_btn = my_button(root, text='捉鬼', width=12, command=change_to_ghost)
    ghost_btn.place(x=x, y=y, anchor=tkinter.NW)


def button_fuben(x, y):
    def change2Fuben():
        change_thread(Fuben(change_window_position=_changWinPos))

    fubenBtn = my_button(root, text='副本', width=12, command=change2Fuben)
    fubenBtn.place(x=x, y=y, anchor=tkinter.NW)


def button_menpai(x, y):
    def changMission():
        change_thread(Menpai(chang_window_position=_changWinPos))

    fubenBtn = my_button(root, text='门派', width=12, command=changMission)
    fubenBtn.place(x=x, y=y, anchor=tkinter.NW)


def button_haidi(x, y):
    def changMission():
        change_thread(Haidi(chang_window_position=_changWinPos))

    fubenBtn = my_button(root, text='海底', width=12, command=changMission)
    fubenBtn.place(x=x, y=y, anchor=tkinter.NW)


def button_mihunta(x, y):
    def changMission():
        change_thread(Mihunta(chang_window_position=_changWinPos))

    fubenBtn = my_button(root, text='迷魂塔', width=12, command=changMission)
    fubenBtn.place(x=x, y=y, anchor=tkinter.NW)


def button_bangpai(x, y):
    global bangpai_btn

    def change_to_bangpai():
        change_thread(Bangpai(chang_window_position=_changWinPos))

    bangpai_btn = my_button(root, text='帮派任务', width=12, command=change_to_bangpai)
    bangpai_btn.place(x=x, y=y, anchor=tkinter.NW)


def button_mine(x, y):
    def change_to_mine():
        change_thread(Mine(chang_window_position=_changWinPos))

    mine_btn = my_button(root, text='挖矿', width=12, command=change_to_mine)
    mine_btn.place(x=x, y=y, anchor=tkinter.NW)


'''
创建游戏窗口列表
'''


def table_window_list(x, y):
    global root
    # (1)创建样式
    style = tkinter.ttk.Style()
    style.configure("Treeview", rowheight=20)  # 设置行高
    style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))  # 设置表头字体
    # (2)创建 Treeview 控件，设置高度为10行
    root.tree = ttk.Treeview(root, height=10, style="Treeview")
    root.tree.place(x=x, y=y, anchor=tkinter.NW)
    # (3)定义列名
    root.tree["columns"] = ("name", "status")
    # (4)设置列的标题名称，anchor可设置对其方式：居中(center)/左对齐(w)/右对齐(e)，无anchor参数时，标题名称默认居中
    root.tree.heading("#0", text="序号", anchor="w")
    root.tree.heading("name", text="角色名称")
    root.tree.heading("status", text="状态")
    # (5)设置列宽度(像素)，无anchor参数时，列表中的数据除(#0)外其余都是默认左对齐
    root.tree.column("#0", width=50)
    root.tree.column("name", width=100, anchor="center")
    root.tree.column("status", width=90, anchor="center")
    # (6)插入默认数据
    root.tree.insert("", tkinter.END, text="1", values=("恣意asdfasdfasdfasdf", "抓鬼中"))
    root.tree.insert("", tkinter.END, text="2", values=("恣意asdfasdfasdfasdf恣意asdfasdfasdfasdf", "抓鬼中"))


def button_resize_to_small(x, y):
    smallWinBtn = my_button(root, text='初始化为小窗口', width=12, command=gameProcess.move_zhuo_mian_ban)
    smallWinBtn.place(x=x, y=y, anchor=tkinter.NW)


def button_resize_to_origin_window(x, y):
    originWinBtn = my_button(root, text='初始化为原始窗口', width=12, command=gameProcess.move_zhuo_mian_ban_to_origin)
    originWinBtn.place(x=x, y=y, anchor=tkinter.NW)


def text_area(x, y):
    t = tkinter.Text(root, width=34, height=10)
    t.insert(tkinter.END, "说明\n"
                          "1 如果出现后台运行的程序无法关闭情况，请通过关闭本窗口程序关闭正在运行的脚本。\n"
                          "2 程序不受控可以通过将鼠标快速移动到右上角强制终止。\n"
                          "3 对应功能程序配置文件和说明放在resources下相应文件夹内")
    t.place(x=x, y=y, anchor=tkinter.NW)


'''
创建ui界面
'''


def create_ui_panel():
    global root, x, y, gameProcess
    root = tkinter.Tk()
    # 标题
    root.title("梦幻手游脚本")
    # 图形界面的x,y轴长度
    x = int((root.winfo_screenwidth() - root.winfo_reqwidth()) / 2)
    y = int((root.winfo_screenheight() - root.winfo_reqheight()) / 2)
    # 设置窗口的大小和位置
    root.geometry("660x430+{}+{}".format(x, y))
    gameProcess = GameProcess()
    # 按钮基础x坐标位置
    button_origin_x = 300
    # 每个按钮x轴间距
    button_x_step = 120
    # 按钮基础y坐标位置
    button_origin_y = 10
    # 每个按钮y轴间距
    button_y_step = 40
    # 创建一个梦幻窗口的管理列表
    table_window_list(10, 10)
    # 初始化为小窗口
    button_resize_to_small(button_origin_x, button_origin_y)
    # 初始化为原始窗口
    button_resize_to_origin_window(button_origin_x + button_x_step, button_origin_y)
    # 抓鬼
    button_ghost(button_origin_x, button_origin_y + button_y_step)
    # 副本
    button_fuben(button_origin_x + button_x_step, button_origin_y + button_y_step)
    # 门派
    button_menpai(button_origin_x, button_origin_y + button_y_step * 2)
    # 海底
    button_haidi(button_origin_x + button_x_step, button_origin_y + button_y_step * 2)
    # 迷魂塔
    button_mihunta(button_origin_x, button_origin_y + button_y_step * 3)
    # 帮派任务
    button_bangpai(button_origin_x + button_x_step, button_origin_y + button_y_step * 3)
    # 挖矿
    button_mine(button_origin_x, button_origin_y + button_y_step * 4)
    # 说明
    text_area(10, 240)
    # 停止当前任务
    pack_stop(80, 380)
    # 进入消息循环，调用这个函数之后，图形界面才会显示出来
    root.mainloop()


# 界面程序 此部分封装了参数没有大量写死的程序 opencv 死活打包不进去
# pyinstaller --onefile --noconsole mhxy_script.py
# pyinstaller --onefile mhxy_script.py
if __name__ == '__main__':
    # 扫描已经开启的游戏窗口
    frames = game_process.get_all_mhxy_frames()

    avatar_position_percent_x = 0.95
    avatar_position_percent_y = 0.1


    # 获取窗口中的人物的名称
    for frame in frames:
        frame.window.activate()
        # 2k分辨率默认是1040*807
        print(f"窗口大小：{frame.window}")
        avatar_position_x = frame.left + (frame.right - frame.left) * avatar_position_percent_x + random.randint(-10, 10)
        avatar_position_y = frame.top + (frame.bottom - frame.top) * avatar_position_percent_y + random.randint(-10, 10)
        pyautogui.moveTo(avatar_position_x, avatar_position_y)
        pyautogui.click()
        print(f"窗口大小：{frame.window}")
    # 创建ui面板
    # create_ui_panel()