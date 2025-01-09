# @Author  : RinChord
# @File    : main_window.py
# @Software: VScode

import sys
import os
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialogButtonBox, QComboBox

# 其他窗口模块
from .port_setting import port_setting

# 后端函数
from function.change_port import is_admin, find_device_usb_path, read_com_port_number, write_com_port_value


class main_window(QMainWindow):
    def __init__(self, ui_file_path):
        super(main_window, self).__init__()
        self.load_ui(ui_file_path)

        ##############################################
        # 初始化成员变量
        ##############################################
        self.selected_device = 1
        self.vid = "0CA3"  
        self.pid = "0021"  
        self.device_paths = find_device_usb_path(self.vid, self.pid)
        ##############################################
        # 实例化 port_setting 窗口
        ##############################################
        self.port_setting_window = port_setting("Project/interface/port_setting.ui", self.device_paths, self.selected_device)
        ##############################################
        # 获取按钮并连接信号
        ##############################################
        self.findChild(QPushButton, 'pushButton_1_1').clicked.connect(self.on_button_click)
        self.findChild(QPushButton, 'reconfirm_button').clicked.connect(self.reconfirm)
        
        # 初始化底部多功能控件
        self.dialog_button = self.findChild(QDialogButtonBox, 'dialog_button')
        self.dialog_button.accepted.connect(self.close_windows)
        self.dialog_button.helpRequested.connect(self.close_windows)
        
        # 初始化下拉框控件
        self.device_selector = self.findChild(QComboBox, 'device_selector')
        self.device_selector.currentIndexChanged.connect(self.on_device_selected)
        self.refresh_device_selector()
        ##############################################
        


    ##############################################
    # 事件
    ##############################################
    
    # 窗口关闭事件
    def close_windows(self):
        self.close()

    # 测试事件
    def on_button_click(self):
        self.port_setting_window.show()
        print("按钮被点击了！")

    # 为设备选择器添加设备下拉列表
    def refresh_device_selector(self):
        # 获取设备路径的二维数组
        # 清空 device_selector 的下拉列表
        self.device_selector.clear()

        # 根据二维数组的列数，动态生成下拉列表
        for i in range(len(self.device_paths)):
            self.device_selector.addItem(f"设备 {i + 1}")

    # 获取用户选择
    def on_device_selected(self, index):
        self.update_port_setting(self.device_selector.itemText(index))

    # 再次确认事件
    def reconfirm(self):
        self.update_port_setting(self.device_selector.currentText())

    # 更新端口设置窗口的信息
    def update_port_setting(self, selected_text):

        if not selected_text :
            print("未选择设备")
            return
        self.selected_device = selected_text[3:]
        if not self.selected_device.isdigit():
            print("类型错误")
            return

        # 经过有效性检查后，更新端口设置窗口的信息
        self.port_setting_window.selected_device = self.selected_device
        self.port_setting_window.update_ports()
        print(f"选择了设备: {self.selected_device}")
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