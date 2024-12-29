# -*- coding: utf-8 -*-

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from interface.MainWindow import MainWindow


def main():
    app = QApplication([])

    # UI文件路径
    ui_file_path = "Project\interface\mai_deploy.ui"  # 确保使用正确的路径格式

    # 创建主窗口
    window = MainWindow(ui_file_path)

    # 显示窗口
    window.show()

    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
