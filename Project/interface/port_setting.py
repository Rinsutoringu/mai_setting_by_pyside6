# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : main_window.py
# @Software: VScode

import sys
import os
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialogButtonBox, QComboBox, QTextBrowser
# from Project.function.setport import setport

class port_setting(QMainWindow):
    def __init__(self, ui_file_path):
        super(port_setting, self).__init__()

        # 加载UI文件
        self.load_ui(ui_file_path)

        #####################################
        # 获取按钮并连接信号
        self.dialog_button = self.findChild(QDialogButtonBox, 'dialog_button')
        self.dialog_button.accepted.connect(self.close_windows)
        self.dialog_button.helpRequested.connect(self.close_windows)

        self.findChild(QComboBox, 'touch_select').currentIndexChanged.connect(self.on_button_click)

        self.findChild(QPushButton, 'touch_set').clicked.connect(lambda: self.set_port_click('touch_select'))
        self.findChild(QPushButton, 'aime_set').clicked.connect(lambda: self.set_port_click('aime_select'))
        self.findChild(QPushButton, 'led_set').clicked.connect(lambda: self.set_port_click('led_select'))
        self.findChild(QPushButton, 'command_set').clicked.connect(lambda: self.set_port_click('command_select'))
        
        self.findChild(QPushButton, 'Refresh').clicked.connect(self.refresh_port_click)

        self.findChild(QTextBrowser, 'touch_port').setText("1")

        #####################################



    #####################################
    #在这里写点击事件

    # 下拉框选择触发事件
    # def touch_select(self):
    #     print("选择了")
    #     a = self.findChild(QComboBox, 'touch_select').currentText()
    #     print("当前文本为：", a)

    # 关闭窗口事件
    def close_windows(self):
        self.close()

    # 测试用事件
    def on_button_click(self):
        print("按钮被点击了！")

    # 设置端口事件
    def set_port_click(self,device):
        select_box = self.findChild(QComboBox, device)
        port = select_box.currentText()
        # setport(device, port)
        self.refresh_port_click()

    # 刷新端口事件
    def refresh_port_click(self):
        print("刷新端口")
        # port = getport()
        # self.findChild(QTextBrowser, 'touch_port').setText(port[0])
        # self.findChild(QTextBrowser, 'aime_port').setText(port[1])
        # self.findChild(QTextBrowser, 'led_port').setText(port[2])
        # self.findChild(QTextBrowser, 'command_port').setText(port[3])

    #####################################

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


        
