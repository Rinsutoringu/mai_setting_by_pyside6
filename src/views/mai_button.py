# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : mai_button.py
# @Software: VScode

import sys
import os
from PySide6.QtCore import QFile, QIODevice, Qt, QTimer, QByteArray
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QMainWindow, QPushButton, QDialogButtonBox, QLabel, 
                               QWidget, QVBoxLayout, QHBoxLayout)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import QSvgRenderer
from utils.warning import show_warning
from utils.string_utils import extract_device_number
from utils.svghandle import svgHandle

class mai_button(QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(mai_button, cls).__new__(cls)
        return cls._instance

    def __init__(self, ui_file_path, device_paths, selected_device: int, main_window_instance=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        super(mai_button, self).__init__()
        self._initialized = True
        
        # 初始化变量
        self.svg_widget = None
        self.svg_loaded = False
        
        self.load_ui(ui_file_path)

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

        try:
            self.handler = svgHandle("resources//drawing.svg")
        except Exception as e:
            print(f"SVG handler初始化失败: {e}")
            self.handler = None

        #####################################
        # 获取按钮并连接信号
        #####################################
        self.dialog_button = self.findChild(QDialogButtonBox, 'buttonBox')
        if self.dialog_button is None:
            show_warning("Initialization Error", "Dialog button not found!")
            
        self.svg_container = self.findChild(QWidget, 'buttonview')
        self.bgweight = self.findChild(QWidget, 'bgweight')

        if self.svg_container is None:
            show_warning("Initialization Error", "SVG container not found!")
            
        self.testbutton_1 = self.findChild(QPushButton, 'test123')
        self.testbutton_2 = self.findChild(QPushButton, 'test123_2')
        self.testbutton_3 = self.findChild(QPushButton, 'test123_3')
        self.testbutton_4 = self.findChild(QPushButton, 'test123_4')
        self.testbutton_5 = self.findChild(QPushButton, 'test123_5')

        # 连接信号
        self.dialog_button.accepted.connect(self.close_windows)
        self.dialog_button.helpRequested.connect(self.close_windows)
        self.testbutton_1.clicked.connect(self.test_button_1_clicked)
        self.testbutton_2.clicked.connect(self.test_button_2_clicked)
        self.testbutton_3.clicked.connect(self.test_button_3_clicked)
        self.testbutton_4.clicked.connect(self.test_button_4_clicked)
        self.testbutton_5.clicked.connect(self.test_button_5_clicked)

        #####################################
        # 界面逻辑 - 初始化SVG容器
        #####################################
        self.setup_svg_container()
        
        # 延迟加载SVG，避免阻塞界面
        QTimer.singleShot(200, self.initialize_svg)
        #####################################

    def close_windows(self):
        """
        关闭窗口事件
        """
        self.close()

    def setup_svg_container(self):
        """设置SVG容器"""
        if not self.svg_container:
            return
            
        # 为SVG容器设置布局
        if not self.svg_container.layout():
            layout = QVBoxLayout(self.svg_container)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setAlignment(Qt.AlignCenter)
        
        # 给每个控件设置唯一的objectName，然后用ID选择器
        self.svg_container.setObjectName("svg_container")
        self.svg_container.setStyleSheet("""
            #svg_container {
            }
        """)
        
        if self.bgweight:
            self.bgweight.setObjectName("bgweight")
            self.bgweight.setStyleSheet("""
                #bgweight {
                    image: url(resources/buttonBG.png);
                }
            """)
            
    def initialize_svg(self):
        """初始化SVG显示"""
        if self.svg_loaded or not self.svg_container:
            return
            
        print("开始初始化SVG")
        try:
            self.load_svg_from_file()
            self.svg_loaded = True
            
        except Exception as e:
            print(f"初始化SVG失败: {e}")
            self.svg_loaded = True

    def load_svg_from_file(self):
        """从文件加载SVG"""
        print("尝试从文件加载SVG")
        
        # 构建可能的SVG文件路径
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        svg_paths = [
            "resources/drawing.svg",
            os.path.join(base_dir, "resources", "drawing.svg"),
            os.path.join(os.getcwd(), "resources", "drawing.svg"),
        ]
        
        for svg_path in svg_paths:
            svg_path = os.path.normpath(svg_path)
            print(f"检查路径: {svg_path}")
            
            if os.path.exists(svg_path):
                print(f"找到SVG文件: {svg_path}")
                try:
                    # 验证SVG文件
                    renderer = QSvgRenderer(svg_path)
                    if renderer.isValid():
                        self.create_svg_widget_from_file(svg_path)
                        return True
                    else:
                        print("SVG文件格式无效")
                        
                except Exception as e:
                    print(f"加载文件SVG出错: {e}")
                    continue
                    
        print("未找到可用的SVG文件")
        self.show_error_message(f"未找到可用的SVG文件")
        return False

    def create_svg_widget_from_file(self, svg_path):
        """从文件创建SVG widget"""
        try:
            # 清理旧的widget
            self.clear_svg_container()
            
            # 创建SVG widget
            self.svg_widget = QSvgWidget(svg_path)
            self.setup_svg_widget()
            
            print(f"从文件创建SVG widget成功: {svg_path}")
            
        except Exception as e:
            print(f"从文件创建SVG widget失败: {e}")
            raise

    def setup_svg_widget(self):
        """设置SVG widget的通用属性"""
        if not self.svg_widget or not self.svg_container:
            return
            
        # 设置SVG widget属性
        # self.svg_widget.setMinimumSize(200, 150)
        # self.svg_widget.setMaximumSize(600, 450)
        
        # 添加到布局
        layout = self.svg_container.layout()
        if layout:
            layout.addWidget(self.svg_widget)
        
        print("SVG widget设置完成")

    def clear_svg_container(self):
        """清理SVG容器"""
        if not self.svg_container:
            return
            
        layout = self.svg_container.layout()
        if layout:
            # 清理布局中的所有widget
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        
        # 清理SVG widget引用
        if self.svg_widget:
            self.svg_widget.deleteLater()
            self.svg_widget = None

    def show_error_message(self, message):
        """显示错误消息"""
        try:
            self.clear_svg_container()
            
            # 创建错误标签
            error_label = QLabel(f"❌ {message}\n\n点击测试按钮重试")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("""
                QLabel {
                    background-color: #ffebee;
                    border: 2px solid #f44336;
                    border-radius: 8px;
                    color: #d32f2f;
                    font-size: 14px;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                }
            """)
            error_label.setMinimumSize(200, 100)
            
            # 添加到布局
            layout = self.svg_container.layout()
            if layout:
                layout.addWidget(error_label)
            
            print(f"显示错误消息: {message}")
            
        except Exception as e:
            print(f"显示错误消息失败: {e}")

    #####################################
    # 工具函数
    #####################################
    def show_svg_on_screenview(self, label_name, color):
        """在屏幕视图上显示SVG（重构后的方法）"""
        print(f"显示SVG - 标签: {label_name}, 颜色: {color}")
        
        try:
            # 如果有handler，使用它来生成定制化的SVG
            if self.handler:
                # 使用handler修改SVG颜色
                modified_svg = self.handler.changeSvgColor(label_name, color)
                if modified_svg:
                    # TODO 展示新的SVG，此时SVG应该在内存里
                    self.display_custom_svg(modified_svg)
                    print(f"使用handler显示SVG成功 - 标签: {label_name}, 颜色: {color}")
                    return
                else:
                    print("handler返回的SVG为空，使用备用方案")
            
        except Exception as e:
            print(f"显示SVG出错: {e}")
            self.show_error_message(f"显示SVG失败: {str(e)}")

    def test_button_1_clicked(self):
        """测试按钮点击事件"""
        self.show_svg_on_screenview("A1", "#4CAF50")

    def test_button_2_clicked(self):
        """测试按钮点击事件"""
        self.show_svg_on_screenview("B1", "#2196F3")

    def test_button_3_clicked(self):
        """测试按钮点击事件"""
        self.show_svg_on_screenview("C1", "#FF9800")

    def test_button_4_clicked(self):
        """测试按钮点击事件"""
        self.show_svg_on_screenview("D1", "#9C27B0")

    def test_button_5_clicked(self):
        """测试按钮点击事件"""
        self.show_svg_on_screenview("E1", "#F44336")

    def display_custom_svg(self, svg_content):
        """显示自定义SVG内容"""
        try:
            print(f"准备显示SVG，内容长度: {len(svg_content)}")
            
            # 清理旧的widget
            self.clear_svg_container()
            
            # 创建SVG widget并加载内容
            self.svg_widget = QSvgWidget()
            
            # 将字符串转换为字节数组
            svg_bytes = QByteArray(svg_content.encode('utf-8'))
            
            # 先验证SVG内容是否有效
            renderer = QSvgRenderer()
            if not renderer.load(svg_bytes):
                print("SVG内容无效，无法被渲染器解析")
                print(f"SVG内容前100字符: {svg_content[:100]}")
                raise Exception("SVG内容格式无效")
            
            # 加载SVG内容到widget
            if self.svg_widget.load(svg_bytes):
                self.setup_svg_widget()
                print("自定义SVG显示成功")
            else:
                print("SVG widget加载失败")
                # 尝试使用渲染器方式
                self.svg_widget.renderer().load(svg_bytes)
                if self.svg_widget.renderer().isValid():
                    self.setup_svg_widget()
                    print("使用渲染器方式显示SVG成功")
                else:
                    raise Exception("SVG内容无法被widget加载")
                    
        except Exception as e:
            print(f"显示自定义SVG失败: {e}")
            # 如果失败，显示错误消息
            self.show_error_message(f"SVG显示失败: {str(e)}")

    # 添加一个修复的SVG验证方法
    def validate_and_fix_svg(self, svg_content):
        """验证并尝试修复SVG内容"""
        try:
            # 基本验证
            if not svg_content or not isinstance(svg_content, str):
                raise Exception("SVG内容为空或类型错误")
            
            # 检查基本结构
            if '<?xml' not in svg_content:
                svg_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_content
            
            if '<svg' not in svg_content:

                raise Exception("SVG内容缺少svg标签")
                
                
            if '</svg>' not in svg_content:
                svg_content += '</svg>'
            
            # 尝试用渲染器验证
            renderer = QSvgRenderer()
            svg_bytes = QByteArray(svg_content.encode('utf-8'))
            
            if renderer.load(svg_bytes):
                print("SVG验证成功")
                return svg_content
            else:
                print("SVG验证失败")
                return None
                
        except Exception as e:
            print(f"SVG验证过程出错: {e}")
            self.show_error_message(f"SVG验证过程出错: {e}")
            return None
        
    def show_error_message(self, message):
        try:
            self.clear_svg_container()
            
            # 创建错误标签
            error_label = QLabel(f"❌ {message}\n\n点击测试按钮重试")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("""
                QLabel {
                    background-color: #ffebee;
                    border: 2px solid #f44336;
                    border-radius: 8px;
                    color: #d32f2f;
                    font-size: 14px;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                }
            """)
            error_label.setMinimumSize(200, 100)
            
            # 添加到布局
            layout = self.svg_container.layout()
            if layout:
                layout.addWidget(error_label)
            
            print(f"显示错误消息: {message}")

        except Exception as e:
            print(f"显示错误消息失败: {e}")
            

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