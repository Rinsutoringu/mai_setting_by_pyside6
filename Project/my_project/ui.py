# -*- coding: utf-8 -*-
# @Time    : 2023/9/25 22:03
# @Author  : MinChess
# @File    : main.py
# @Software: PyCharm

import sys
import os
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self, ui_file_path):
        super(MainWindow, self).__init__()

        # 加载UI文件
        self.load_ui(ui_file_path)
        # 获取按钮并连接信号
        self.findChild(QPushButton, 'pushButton_1_1').clicked.connect(self.on_button_click)



    #在这里写点击事件

    def on_button_click(self):
        print("按钮被点击了！")


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


        
def main():
    app = QApplication([])

    # UI文件路径
    ui_file_path = "ui\project\mai_deploy.ui"  # 确保使用正确的路径格式

    # 创建主窗口
    window = MainWindow(ui_file_path)

    # 显示窗口
    window.show()

    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
