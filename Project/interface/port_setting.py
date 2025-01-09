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
from function.change_port import is_admin, find_device_usb_path, read_com_port_number, write_com_port_value

class port_setting(QMainWindow):
    def __init__(self, ui_file_path, device_paths, selected_device: int):
        super(port_setting, self).__init__()
        
        self.device_paths = device_paths
        self.selected_device = selected_device
        self.load_ui(ui_file_path)

        #####################################
        # 获取按钮并连接信号
        #####################################
        self.dialog_button = self.findChild(QDialogButtonBox, 'dialog_button')
        self.dialog_button.accepted.connect(self.close_windows)
        self.dialog_button.helpRequested.connect(self.close_windows)

        self.findChild(QPushButton, 'touch_set').clicked.connect(lambda: self.set_port_click('touch_select'))
        self.findChild(QPushButton, 'aime_set').clicked.connect(lambda: self.set_port_click('aime_select'))
        self.findChild(QPushButton, 'led_set').clicked.connect(lambda: self.set_port_click('led_select'))
        self.findChild(QPushButton, 'command_set').clicked.connect(lambda: self.set_port_click('command_select'))
        
        self.findChild(QPushButton, 'Refresh').clicked.connect(self.refresh_port_click)
        #####################################
        # 界面逻辑
        #####################################
        self.update_ports()
        #####################################

    #####################################
    #在这里写点击事件
    #####################################

    # 关闭窗口事件
    def close_windows(self):
        self.close()

    # 设置端口的事件
    def set_port_click(self,device):
        i = int(self.selected_device) - 1

        port_select_box = self.findChild(QComboBox, device)
        port = "COM"+port_select_box.currentText()
        print("为", device, "设备配置", port, "端口")
        if device == 'touch_select':
            write_com_port_value(self.device_paths[i][0], port)
        elif device == 'aime_select':
            write_com_port_value(self.device_paths[i][1], port)
        elif device == 'led_select':
            write_com_port_value(self.device_paths[i][2], port)
        elif device == 'command_select':
            write_com_port_value(self.device_paths[i][3], port)
        self.update_ports()

    # 刷新端口事件
    def refresh_port_click(self):
        self.update_ports(self)


    # 获取设备端口
    def update_ports(self):
        i = int(self.selected_device) - 1
        touch_port = read_com_port_number(self.device_paths[i][0])[3:]
        aime_port = read_com_port_number(self.device_paths[i][1])[3:]
        led_port = read_com_port_number(self.device_paths[i][2])[3:]
        command_port = read_com_port_number(self.device_paths[i][3])[3:]

        touch_port_box = self.findChild(QTextBrowser, 'touch_port')
        aime_port_box = self.findChild(QTextBrowser, 'aime_port')
        led_port_box = self.findChild(QTextBrowser, 'led_port')
        command_port_box = self.findChild(QTextBrowser, 'command_port')

        touch_port_box.setText(touch_port)
        aime_port_box.setText(aime_port)
        led_port_box.setText(led_port)
        command_port_box.setText(command_port)

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


        
