# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : main_window.py
# @Software: VScode

import sys
import os
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialogButtonBox, QComboBox, QTextBrowser, QLabel, QGraphicsView
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray
from PySide6.QtWidgets import QGraphicsScene
from utils.warning import show_warning
from utils.string_utils import extract_device_number
from utils.svghandle import svgHandle

class mai_button(QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(mai_button, cls).__new__(cls)
        return cls._instance

    # 构造函数
    def __init__(self, ui_file_path, device_paths, selected_device: int, main_window_instance=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        super(mai_button, self).__init__()
        self._initialized = True

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

        # 获取main_window实例句柄
        self.main_window = main_window_instance
        self.ConnectDevice = self.main_window.getDevices()
        
        # 从main_window获取用户选择的设备
        if self.ConnectDevice == {}:
            show_warning("Initialization Error", "No connected devices found!")
            self.device = None
        else:
            device_number = extract_device_number(self.main_window.getUserChooseDevice())
            self.device = self.ConnectDevice[device_number-1]

        self.handler = svgHandle("resources//drawing.svg")
          # 示例调用，显示 E8 标签的绿色 SVG
        #####################################
        # 获取按钮并连接信号
        #####################################
        self.dialog_button = self.findChild(QDialogButtonBox, 'buttonBox')
        self.screen_view = self.findChild(QGraphicsView, 'screenView')
        self.testbutton = self.findChild(QPushButton, 'test123')
        if self.testbutton is None:
            show_warning("Initialization Error", "Test button not found!")

        # TODO 
        self.dialog_button.accepted.connect(self.close)
        self.dialog_button.rejected.connect(self.close)
        self.dialog_button.helpRequested.connect(self.close)
        self.testbutton.clicked.connect(lambda: self.show_svg_on_screenview("E8", "#00ff00"))

        #####################################
        # 界面逻辑
        #####################################
        

        #####################################


    #####################################
    # 工具函数
    #####################################
    def show_svg_on_screenview(self, label_name, color):
        # 用 svgHandle 修改 SVG
        new_svg = self.handler.changeSvgColor(label_name, color)

        # 创建 QSvgRenderer
        renderer = QSvgRenderer(QByteArray(new_svg.encode("utf-8")))

        # 创建 QGraphicsSvgItem 并设置 renderer
        svg_item = QGraphicsSvgItem()
        svg_item.setSharedRenderer(renderer)

        # 创建场景并添加 item
        scene = QGraphicsScene()
        scene.addItem(svg_item)
        self.screen_view.setScene(scene)
        self.screen_view.show()
    #####################################

    #####################################
    #在这里写点击事件
    #####################################

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