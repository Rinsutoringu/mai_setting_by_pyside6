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
from utils.warning import show_warning

class port_setting(QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(port_setting, cls).__new__(cls)
        return cls._instance

    def __init__(self, ui_file_path, device_paths, selected_device: int, main_window_instance=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        super(port_setting, self).__init__()
        self._initialized = True

        self.device_paths = device_paths
        # 检查 device_paths 是否为 None 或空
        if not self.device_paths:
            show_warning("Initialization Error", "Device Not Found!")
            self.label = QLabel("No Device Found", self)
            return

        # 检查 device_paths 的结构是否符合预期
        for index, path in enumerate(self.device_paths):
            if not isinstance(path, list) or len(path) < 4:
                show_warning("Initialization Error", f"Device path at index {index} is invalid: {path}")
                return
        self.selected_device = selected_device
        self.load_ui(ui_file_path)

        # 获取main_window实例句柄
        self.main_window = main_window_instance
        self.ConnectDevice = self.main_window.getDevices()
        
        # 从main_window获取用户选择的设备
        if self.ConnectDevice == {}:
            show_warning("Initialization Error", "No connected devices found!")
            self.device = None
        else:
            self.device = self.ConnectDevice[self.main_window.getUserChooseDevice()]

        #####################################
        # 获取按钮并连接信号
        #####################################
        self.dialog_button = self.findChild(QDialogButtonBox, 'dialog_button')
        self.dialog_button.accepted.connect(self.close_windows)
        self.dialog_button.helpRequested.connect(self.close_windows)

        # 把端口存储到对象里，对象的内部方法完成端口的配置
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


    def read_port_from_select(self, device):
        """
        从选择的端口中读取端口号
        """
        port_select_box = self.findChild(QComboBox, device)
        return port_select_box.currentText()


    def set_port_click(self, port_type):
        """
        给指定设备设定端口
        """

        if self.device is None:
            show_warning("device error", "Device Not Found!")
            return
        if not self.device.check_connect():
            show_warning("device error", "Device Not Connected!")
            return
        # 获取当前选择的端口
        port = self.read_port_from_select(port_type)

        # DEBUG
        print(f"Selected port for {port_type}: {port}")
        if port is None:
            show_warning("port error", "Invalid Port Selected!")
            return
        # 为指定串口设备设置端口
        self.device.set_port(port_type, port)
        self.update_ports()

        # DEBUG
        print(f"Setting {port_type} port to: {port}")


    def refresh_port_click(self):
        """
        刷新行为
        """
        self.update_ports()


    def update_ports(self):
        """
        刷新端口
        """
        if self.device is None:
            show_warning("device error", "Device Not Found!")
            return
        self.device.get_port()

        self.findChild(QTextBrowser, 'touch_port').setText(self.device.getPort('touch'))
        self.findChild(QTextBrowser, 'aime_port').setText(self.device.getPort('aime'))
        self.findChild(QTextBrowser, 'led_port').setText(self.device.getPort('led'))
        self.findChild(QTextBrowser, 'command_port').setText(self.device.getPort('command'))

    #####################################

    def load_ui(self, ui_file_path):
        """
        加载UI
        """
        if not os.path.exists(ui_file_path):
            print(f"文件不存在: {ui_file_path}")
            sys.exit(-1)

        # print("当前工作目录:", os.getcwd())
        ui_file = QFile(ui_file_path)

        if not ui_file.open(QIODevice.ReadOnly):
            sys.exit(-1)
        loader = QUiLoader()
        self.setCentralWidget(loader.load(ui_file))

        ui_file.close()