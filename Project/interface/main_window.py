# @Author  : RinChord
# @File    : main_window.py
# @Software: VScode

import sys
import os
import ctypes
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialogButtonBox, QComboBox

# 其他窗口模块
from .port_setting import port_setting

# 后端函数
from function.change_port import find_device_usb_path, show_warning, find_device_reg_path


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
        if self.device_paths is None:
            show_warning("error", "No device found!")
            # sys.exit(-1)
        ##############################################
        # 初始化子窗口
        ##############################################
        self.port_setting_window = port_setting("Project/interface/port_setting.ui", self.device_paths, self.selected_device)
        ##############################################
        # 初始化按钮
        ##############################################
        self.port_setting = self.findChild(QPushButton, 'port_setting')
        self.reconfirm_button = self.findChild(QPushButton, 'reconfirm_button')
        self.admin_button = self.findChild(QPushButton, 'admin_button')
        self.dialog_button = self.findChild(QDialogButtonBox, 'dialog_button')
        self.device_selector = self.findChild(QComboBox, 'device_selector')
        ##############################################
        # 事件绑定
        ##############################################
        self.port_setting.clicked.connect(self.open_port_setting)
        self.reconfirm_button.clicked.connect(self.reconfirm)
        self.admin_button.clicked.connect(self.request_admin_privileges)
        self.dialog_button.accepted.connect(self.close_windows)
        self.dialog_button.helpRequested.connect(self.close_windows)
        self.device_selector.currentIndexChanged.connect(self.on_device_selected)
        self.refresh_device_selector()
        self.is_admin()
        ##############################################
    
    ##############################################
    # 事件
    ##############################################
    
    def close_windows(self):
        """
        关闭窗口
        """
        self.close()

    def open_port_setting(self):
        """
        打开端口设置窗口
        """
        self.port_setting_window.show()

    def refresh_device_selector(self):
        """
        为设备选择器添加设备下拉列表
        获取设备路径的二维数组
        清空 device_selector 的下拉列表
        """
        self.device_selector.clear()

        # 根据二维数组的列数，动态生成下拉列表
        for i in range(len(self.device_paths)):
            self.device_selector.addItem(f"设备 {i + 1}")

    def on_device_selected(self, index):
        """
        获取用户选择
        """
        self.update_port_setting(self.device_selector.itemText(index))

    def reconfirm(self):
        """
        再次确认事件
        """
        self.update_port_setting(self.device_selector.currentText())

    def update_port_setting(self, selected_text):
        """
        更新端口设置窗口的信息
        :param selected_text: 选择的设备的文本
        """
        if not selected_text :

            return
        self.selected_device = selected_text[3:]
        if not self.selected_device.isdigit():
            show_warning("error", "The selected device is illegal!")
            return

        # 经过有效性检查后，更新端口设置窗口的信息
        self.port_setting_window.selected_device = self.selected_device
        self.port_setting_window.update_ports()

    def is_admin(self):
        """
        验证当前用户是否是管理员
        :return: 不是返回False, 是返回True
        """
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            return False
        self.admin_button.setText("Admin Active !")
        self.admin_button.setStyleSheet("color: rgb(0, 128, 0)")
        return True
            
    def request_admin_privileges(self):
        """
        请求管理员权限
        """
        if self.is_admin() == True:
            show_warning("Hey!", "Escalated already!")
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 0)
            self.close()

    ##############################################

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