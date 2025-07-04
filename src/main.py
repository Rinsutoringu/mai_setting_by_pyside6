# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : main.py
# @Software: VScode

import sys
from PySide6.QtWidgets import QApplication
from views.main_window import main_window


def main():
    app = QApplication([])

    # UI文件路径
    main_window_path = "src/ui/main_window.ui"  # 确保使用正确的路径格式

    # 实例化主界面
    window = main_window(main_window_path)

    # 显示窗口
    window.show()

    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
