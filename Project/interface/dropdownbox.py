# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : dropdownbox.py
# @Software: VScode

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton
from PySide6.QtCore import Qt

class DropdownBoxDemo(QMainWindow):
    def __init__(self):
        super(DropdownBoxDemo, self).__init__()

        self.setWindowTitle("Dynamic Dropdown Box Demo")
        self.setGeometry(100, 100, 300, 200)

        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout(self.central_widget)

        # 创建下拉列表
        self.combo_box = QComboBox()
        self.layout.addWidget(self.combo_box)

        # 创建刷新按钮
        self.refresh_button = QPushButton("Refresh")
        self.layout.addWidget(self.refresh_button)

        # 连接按钮点击事件到刷新方法
        self.refresh_button.clicked.connect(self.refresh_data)

        # 初始化下拉列表数据
        self.refresh_data()

    def refresh_data(self):
        # 模拟从指定来源获取数据
        data = self.get_data_from_source()

        # 清空下拉列表
        self.combo_box.clear()

        # 添加新数据到下拉列表
        self.combo_box.addItems(data)

    def get_data_from_source(self):
        # 模拟从指定来源获取数据
        # 你可以在这里实现从 API 或其他来源获取数据的逻辑
        return ["Option 1", "Option 2", "Option 3", "test123"]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropdownBoxDemo()
    window.show()
    sys.exit(app.exec())