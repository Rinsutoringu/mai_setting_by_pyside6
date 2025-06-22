# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : main_window.py
# @Software: VScode

import sys
import os
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialogButtonBox, QComboBox, QTextBrowser, QLabel
from utils.port_utils import read_com_port_number, write_com_port_value, show_warning

class port_setting(QMainWindow):
    def __init__(self, ui_file_path, device_paths, selected_device: int):
        super(port_setting, self).__init__()
        
        self.device_paths = device_paths
        # 检查 device_paths 是否为 None 或空
        if not self.device_paths:
            show_warning("Initialization Error", "Device paths are invalid or empty!")
            self.label = QLabel("No Device Found", self)
            return

        # 检查 device_paths 的结构是否符合预期
        for index, path in enumerate(self.device_paths):
            if not isinstance(path, list) or len(path) < 4:
                show_warning("Initialization Error", f"Device path at index {index} is invalid: {path}")
                return
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

    def close_windows(self):
        """
        关闭窗口事件
        """
        self.close()


    def set_port_click(self,device):
        """
        设置端口的事件
        """
        i = int(self.selected_device) - 1

        port_select_box = self.findChild(QComboBox, device)
        port = "COM"+port_select_box.currentText()
        # print("为", device, "设备配置", port, "端口")
        if device == 'touch_select':
            if write_com_port_value(self.device_paths[i][0], port) == False:
                show_warning("port error", "Change port fail!")
        elif device == 'aime_select':
            if write_com_port_value(self.device_paths[i][1], port) == False:
                show_warning("port error", "Change port fail!")
        elif device == 'led_select':
            if write_com_port_value(self.device_paths[i][2], port) == False:
                show_warning("port error", "Change port fail!")
        elif device == 'command_select':
            if write_com_port_value(self.device_paths[i][3], port) == False:
                show_warning("port error", "Change port fail!")
        self.update_ports()


    def refresh_port_click(self):
        """
        新端口事件
        """
        self.update_ports()


    def update_ports(self):
        """
        获取设备端口
        """
        if self.selected_device == 1:
            show_warning("device error", "Device Not Found!")
            return
        i = int(self.selected_device) - 1
        touch_port = read_com_port_number(self.device_paths[i][0])[3:]
        if touch_port is None:
            show_warning("device error", "Cannot get touch device port!")
        aime_port = read_com_port_number(self.device_paths[i][1])[3:]
        if aime_port is None:
            show_warning("device error", "Cannot get aime device port!")
        led_port = read_com_port_number(self.device_paths[i][2])[3:]
        if led_port is None:
            show_warning("device error", "Cannot get led device port!")
        command_port = read_com_port_number(self.device_paths[i][3])[3:]
        if command_port is None:
            show_warning("device error", "Cannot get command device port!")

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
        """
        加载UI
        """
        if not os.path.exists(ui_file_path):
            print(f"文件不存在: {ui_file_path}")
            sys.exit(-1)

        print("当前工作目录:", os.getcwd())
        ui_file = QFile(ui_file_path)

        if not ui_file.open(QIODevice.ReadOnly):
            sys.exit(-1)
        loader = QUiLoader()
        self.setCentralWidget(loader.load(ui_file))

        ui_file.close()