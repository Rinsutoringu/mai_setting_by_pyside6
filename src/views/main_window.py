# @Author  : RinChord
# @File    : main_window.py
# @Software: VScode

import sys
import os
import ctypes
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialogButtonBox, QComboBox, QCheckBox, QTextBrowser, QLineEdit

# 导入设备模型
from models.device_model import Device
from models.command_model import CommandData

# 其他窗口模块
from .port_setting import port_setting
from .mai_button import mai_button


# 工具函数
from utils.port_utils import find_device_usb_path
from utils.warning import show_warning



class main_window(QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(main_window, cls).__new__(cls)
        return cls._instance

    def __init__(self, ui_file_path):
        if hasattr(self, '_initialized') and self._initialized:
            return
        super(main_window, self).__init__()
        self._initialized = True
        self.load_ui(ui_file_path)

        ##############################################
        # 初始化成员变量
        ##############################################
        self.vid = "0CA3"  
        self.pid = "0021"  

        self.device_paths = find_device_usb_path(self.vid, self.pid)
        if self.device_paths is None:
            show_warning("error", "No device found!")
        # devices 是一个字典，键为设备索引，值为 Device 实例
        self.devices = {}

        # 先初始化 selected_device，假设默认选第一个设备
        self.selected_device = 0

        self.userChooseDevice = 0

        self.command_data = CommandData(command_id=0, command_params=[], command_size=0)
        self.serial_buffer = b''
        self.sendcmd = b'\x53\xff\x00'  # 默认发送的命令
        self.checkflag = False

        ##############################################
        # 初始化按钮
        ##############################################
        self.port_setting       = self.findChild(QPushButton, 'port_setting')
        self.mai_button         = self.findChild(QPushButton, 'Sensitivity')
        self.reconfirm_button   = self.findChild(QPushButton, 'reconfirm_button')
        self.admin_button       = self.findChild(QPushButton, 'admin_button')
        self.dialog_button      = self.findChild(QDialogButtonBox, 'dialog_button')
        self.device_selector    = self.findChild(QComboBox, 'device_selector')

        self.checkadmin         = self.findChild(QCheckBox, 'checkadmin')
        self.checkdevice        = self.findChild(QCheckBox, 'checkdevice')
        self.checklink          = self.findChild(QCheckBox, 'checklink')
        self.checkhandshake     = self.findChild(QCheckBox, 'checkhandshake')

        self.miniterminal       = self.findChild(QTextBrowser, 'textBrowser')
        self.send_cmd           = self.findChild(QPushButton, 'sendcmdbutton')
        self.input_cmd          = self.findChild(QLineEdit, 'inputcmdbox')

        ##############################################
        # 事件绑定
        ##############################################
        self.port_setting.clicked.connect(self.open_port_setting)
        self.mai_button.clicked.connect(self.open_mai_button)

        self.reconfirm_button.clicked.connect(self.on_device_selected)
        self.admin_button.clicked.connect(self.request_admin_privileges)
        self.dialog_button.accepted.connect(self.close_windows)
        self.dialog_button.helpRequested.connect(self.close_windows)
        self.device_selector.currentIndexChanged.connect(self.on_device_selected)
        self.send_cmd.clicked.connect(self.sendcmdevent)
        self.input_cmd.returnPressed.connect(self.sendcmdevent)
        self.refresh_device_selector()
        self.is_admin()
        ##############################################
    
        ##############################################
        # 初始化子窗口
        ##############################################
        self.port_setting_window    = port_setting("src/ui/port_setting.ui", self.device_paths, self.selected_device, main_window_instance=self)
        self.mai_button_window      = mai_button("src/ui/mai_button.ui", self.device_paths, self.selected_device, main_window_instance=self)
    ##############################################
    # 事件
    ##############################################
    
    def sendcmdevent(self):
        """
        发送命令
        """

        # 获取用户输入的命令
        usrinput = self.input_cmd.text()
        if not usrinput:
            show_warning("error", "Input command is empty!")
            return

        # 获取发送句柄
        device = self.devices.get(self.getUserChooseDevice())
        if device is None:
            show_warning("error", "No device selected!")
            return
        deviceComm = device.getSerialComm()

        if usrinput == "om serial":
            send_bytes = (b'\x53\x00\x00')
        elif usrinput == "om start":
            send_bytes = (b'\x53\x10\x00')
        elif usrinput == "om stop":
            send_bytes = (b'\x53\x11\x00')
        elif usrinput == "om data":
            send_bytes = (b'\x53\x12\x00')
        elif usrinput == "om sens":
            send_bytes = (b'\x53\x13\x00')

        else :
            show_warning("error", "Unknown command!")
            self.input_cmd.clear()

        deviceComm.send_bytes(send_bytes)
        print(f"Sent command: {usrinput}")
        self.sendcmd = send_bytes
        self.input_cmd.clear()
        self.checkflag = True


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

    def open_mai_button(self):
        """
        打开灵敏度设置窗口
        """
        self.mai_button_window.show()

    def refresh_device_selector(self):
        """
        为设备选择器添加设备下拉列表
        获取设备路径的二维数组
        清空 device_selector 的下拉列表
        """
        self.device_selector.clear()

        # 根据二维数组的列数，动态生成下拉列表

        # device_paths是一个二维数组，列数为识别到的合法设备数量，行为每个串口子设备的注册表路径
        for i in range(len(self.device_paths)):
            self.devices[i] = Device(device_path=self.device_paths[i])
            if self.devices[i].check_connect():
                # 提取设备关键信息
                self.device_selector.addItem(f"Device {i + 1} ({self.devices[i].getDevicePath()[0][58:68]})")
                print("发现设备")

    def on_device_selected(self, index):
        """
        获取用户选择
        """
        self.userChooseDevice = self.device_selector.itemText(index)
        if not self.userChooseDevice:
            return
        # Start to connect to device
        if self.check_admin(): 
            self.checkadmin.setChecked(True)
        if self.check_device():
            self.checkdevice.setChecked(True)
        # if check_link():
        #     self.checklink.setChecked(True)
        # if check_handshake():
        #     self.checkhandshake.setChecked(True)


        # self.update_port_setting(self.device_selector.itemText(index))

    def getUserChooseDevice(self):
        """
        get user choose device index in devices
        :return: device Dict index
        """
        return self.device_selector.currentIndex()

    def update_port_setting(self, selected_text):
        """
        更新端口设置窗口的信息
        :param selected_text: 选择的设备的文本
        """
        if not selected_text:

            return
        self.selected_device = selected_text[3:]
        if not self.selected_device.isdigit():
            show_warning("error", "The selected device is illegal!")
            return

        # 经过有效性检查后，更新端口设置窗口的信息
        self.port_setting_window.selected_device = self.selected_device
        self.port_setting_window.update_ports()
        self.userChooseDevice = self.selected_device

    def is_admin(self):
        """
        验证当前用户是否是管理员
        :return: 不是返回False, 是返回True
        """ 
        if not self.check_admin():
            return False
        self.admin_button.setText("Admin Active !")
        self.admin_button.setStyleSheet("color: rgb(0, 128, 0)")
        return True

    def request_admin_privileges(self):
        """
        请求管理员权限
        """
        if self.is_admin():
            show_warning("Hey!", "Escalated already!")
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 0)
            self.close()

    def getDevices(self):
        """
        获取当前连接的设备
        :return: 设备列表
        """
        return self.devices


    def check_admin(self):
        """
        验证当前用户是否是管理员
        :return: 不是返回False, 是返回True
        """
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            return False
        return True
    

    def check_device(self):
        """
        检查设备是否连接
        :return: if device is connected, return device object, else return None
        """
        # try to connect to the device
        device = self.devices.get(self.getUserChooseDevice())
        deviceComm = device.getSerialComm()

        port = "COM"+device.getPort("command")

        deviceComm.connect(port=port, baudrate=9600, timeout=0.1, bytesize=8, parity='N', stopbits=1)
        device.setConnStatus(True)

        deviceComm.start_listening(callback=self.on_serial_data)
    
        # DEBUG
        print(f"Selected device: {device}")
        # print(f"Selected deviceComm: {deviceComm}")
        print("Device connected, in port "+ port)

        return True
    
    def on_serial_data(self, data):
        # DEBUG
        self.serial_buffer += data
        while b'\x53' in self.serial_buffer:
            idx = self.serial_buffer.find(b'\x53')
            # Check if idx is -1 or the command is received
            if idx == -1 or idx + 2 >= len(self.serial_buffer):
                break
            # get command byte
            self.command_data.setID(self.serial_buffer[(idx + 1):(idx + 2)])
            length_byte = self.serial_buffer[(idx + 2):(idx + 3)]

            # 判断数据包长度是否正确
            self.command_data.setSize(int.from_bytes(length_byte, 'big'))
            if idx + 2 + self.command_data.getSize() > len(self.serial_buffer):
                break

            self.command_data.setParams(self.serial_buffer[(idx+3):(idx + 3 + self.command_data.getSize())])
            self.command_data.setFullData(self.serial_buffer[(idx):(idx + 3 + self.command_data.getSize())])

            # 删除已处理的数据包
            self.serial_buffer = self.serial_buffer[(idx + 3 + self.command_data.getSize()):]

            # 验证指令字段是否正确
            print(self.command_data)


            if self.checkflag and self.sendcmd is not None:
                self.miniterminal.append("Checking command...")
                if self.command_data.getID() != self.sendcmd[1:2]:
                    msg = f"Command check failed, expected: {self.sendcmd[1:2].hex()} but got: {self.command_data.getID().hex()}"
                    self.miniterminal.append(msg)
                else:
                    self.miniterminal.append("Command check success.")
                self.sendcmd = None  # 无论成功失败都立即清空
                self.checkflag = False


            self.miniterminal.append(f"<span style='color:blue;'>{self.command_data.getParams()}</span>")

    ##############################################

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