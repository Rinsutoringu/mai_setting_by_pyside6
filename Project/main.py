# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : main.py
# @Software: VScode

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from interface.main_window import main_window


def main():
    app = QApplication([])

    # UI文件路径
    ui_file_path = "Project\interface\main_window.ui"  # 确保使用正确的路径格式

    # 创建主窗口
    window = main_window(ui_file_path)

    # 显示窗口
    window.show()

    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
