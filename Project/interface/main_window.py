# @Author  : RinChord
# @File    : main_window.py
# @Software: VScode

import sys
import os
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialogButtonBox

from interface.port_setting import port_setting

class main_window(QMainWindow):
    def __init__(self, ui_file_path):
        super(main_window, self).__init__()

        # 加载UI文件
        self.load_ui(ui_file_path)
        # 获取按钮并连接信号
        self.findChild(QPushButton, 'pushButton_1_1').clicked.connect(self.on_button_click)


        self.dialog_button = self.findChild(QDialogButtonBox, 'dialog_button')
        self.dialog_button.accepted.connect(self.close_windows)
        self.dialog_button.helpRequested.connect(self.close_windows)

        # 实例化 port_setting 窗口
        self.port_setting_window = port_setting("Project/interface/port_setting.ui")



##############################################
    def on_button_click(self):
        self.port_setting_window.show()
        print("按钮被点击了！")

    def close_windows(self):
        self.close()
    
##############################################

    def load_ui(self, ui_file_path):
        if not os.path.exists(ui_file_path):
            print(f"文件不存在: {ui_file_path}")
            sys.exit(-1)

        print("当前工作目录:", os.getcwd())

        # 创建UI文件对象
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.ReadOnly):
            print("无法打开UI文件")
            sys.exit(-1)

        # 创建UI加载器
        loader = QUiLoader()

        # 加载UI文件并实例化为窗口对象
        self.setCentralWidget(loader.load(ui_file))

        # 关闭UI文件
        ui_file.close()