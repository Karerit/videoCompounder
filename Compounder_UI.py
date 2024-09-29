import logging
import sys
import time
import tkinter
from tkinter import *
from ttkbootstrap import *
import videoCompound
import extra_message_panel

class MainWindows(Tk):
    def __init__(self):
        super().__init__()
        self.title("简易视频编辑软件")  # 给界面添加一个标题
        self.geometry("544x344+400+200")  # 定义界面尺寸
        # self.resizable(0, 0)  # 定义界面窗口大小不可改变

        self.iconbitmap('123.ico')

        self.TotalLog = 'default'
        self.video_dispose = videoCompound.video_dispose()

        # 调用常用变量
        self.setup_main_gui()

        # 创建日志handler
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def SetPath(self, source_path):
        self.sourcepath = source_path

    def setup_main_gui(self):
        # 给界面设置一个主题
        #self.style = Style(theme="flatly")
        # 创建一个界面标题
        self.label_title = Label(self, text="简易视频编辑软件", font="微软雅黑 20 bold")
        self.label_title.place(relwidth=1, relheight=0.18, relx=0, rely=0)
        # 创建左侧按钮显示区域
        self.Pane_left = PanedWindow(self)
        self.Pane_left.place(relwidth=0.15, relheight=0.82, relx=0, rely=0.18)
        # 创建界面01控制按钮
        self.button_frame01 = Button(self.Pane_left, text="视频合成", command=self.create_frame01)
        self.button_frame01.place(relwidth=1, relheight=0.08, relx=0, rely=0.2)

    def setup_frame01(self):
        self.frame01 = Frame(self, relief="groove")
        self.frame01.place(relwidth=0.84, relheight=0.82, relx=0.16, rely=0.18)
        self.title = Label(self, text='视频合成界面', font="微软雅黑 12 bold")
        self.title.place(relwidth=1, relheight=0.18, relx=0, rely=0)

        self.dispose_log = PanedWindow(self.frame01, orient=VERTICAL)

        self.label01 = Label(self.frame01, text='源视频完整路径')
        self.label01.grid(row=0, column=0)

        self.sourcepath = Entry(self.frame01)
        self.sourcepath.grid(row=0, column=1)

        self.label02 = Label(self.frame01, text='输出视频目标路径')
        self.label02.grid(row=1, column=0)

        self.localpath = Entry(self.frame01)
        self.localpath.grid(row=1, column=1)

        # print(self.sourcepath)  # 现在 self.sourcepath 将是 Entry 组件的实例

        self.button = Button(self.frame01, text='开始合成', command=self.video_dispose_caller)
        self.button.grid(row=1, column=2, pady=10)

    def video_dispose_caller(self):
        self.logFrame = Frame(self, relief="groove")
        self.logFrame.place(relwidth=0.84, relheight=0.52, relx=0.16, rely=0.48)
        self.message = Text(self.logFrame, state='disabled', font="微软雅黑 12 bold")
        self.message.pack()

        self.scollbar_v  = Scrollbar(self.logFrame)
        self.scollbar_v.pack(side=RIGHT, fill=Y)
        self.scollbar_h = Scrollbar(self.logFrame, orient=HORIZONTAL)
        self.scollbar_h.pack(side=BOTTOM, fill=X)

        # 配置日志
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 创建一个TkinterLogHandler并添加到logger
        tk_handler = extra_message_panel.TkinterLogHandler(self.message)
        tk_handler.setFormatter(formatter)
        logger.addHandler(tk_handler)

        time.sleep(3)
        self.video_dispose.video_compound(self.sourcepath.get(), self.localpath.get())

    def create_frame01(self):
        try:
            self.frame01.destroy()
        except:
            pass
        finally:
            self.setup_frame01()


if __name__ == "__main__":
    windows = MainWindows()
    windows.mainloop()

