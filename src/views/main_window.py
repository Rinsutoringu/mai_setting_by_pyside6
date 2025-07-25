# @Author  : RinChord
# @File    : main_window.py
# @Software: VScode

import sys
import os
import ctypes
from PySide6.QtCore import QFile, QIODevice, QObject, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialogButtonBox, QComboBox, QCheckBox, QTextBrowser, QLineEdit

# 导入设备模型
from models.device_model import Device
from models.command_model import CommandData
from utils.omconfig import omConfig

# 其他窗口模块
from .port_setting import port_setting
from .mai_button.mai_button import mai_button


# 工具函数
from utils.port_utils import find_device_usb_path
from utils.warning import show_warning
from utils.package_receive import package_receive
from utils.debuglog import debug_log
from utils.cmd_listener import CMD_listener
from utils.cmd_handler import CMD_Handler


class CommandSignal(QObject):
    log_signal = Signal(str)
    command_signal = Signal(bytes)

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

        ##############################################
        # 初始化持有类对象实例
        ##############################################

        self.omconfig = omConfig()
        self.command_data = CommandData(self.omconfig, command=0, payload=[], payload_length=0)
        self.package_receiver = package_receive(self.omconfig)
        
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
        # 连接事件和槽
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

        self.command_signal = CommandSignal()
        self.command_signal.log_signal.connect(self.show_log)

        ##############################################
        # 初始化函数
        ##############################################
        self.refresh_device_selector()
        self.is_admin()
        ##############################################
    
        ##############################################
        # 初始化子窗口
        ##############################################
        self.port_setting_window = port_setting(
            ui_file_path    = "src/ui/port_setting.ui", 
            omconfig        = self.omconfig, 
            device_paths    = self.device_paths, 
            selected_device = self.selected_device, 
            main_window_instance = self)
        
        self.mai_button_window = mai_button(
            ui_file_path    = "src/ui/mai_button.ui", 
            omconfig        = self.omconfig, 
            device_paths    = self.device_paths, 
            selected_device = self.selected_device, 
            command_data    = self.command_data, 
            main_window_instance = self
        )

        # 保存信号句柄
        self.omconfig.setSignal(self.command_signal)

        self.cmd_listener = CMD_listener(
            command_data=self.command_data,
            omconfig=self.omconfig,
            package_receiver=self.package_receiver
        )
        self.cmd_listener.start()

        self.cmd_handler = CMD_Handler(
            omconfig=self.omconfig,
            command_data=self.command_data,
            mai_button=self.mai_button_window,
            package_receiver=self.package_receiver
        )

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

        # 指令对照表
        # 0x00 获取序列号
        # 0x10 启动触摸数据发送流
        # 0x11 停止触摸数据发送流

        if usrinput == "om serial":
            send_bytes = self.command_data.PC_CMD_GET_SERIAL
        elif usrinput == "om start":
            send_bytes = self.command_data.PC_CMD_TOUCH_DBG_START
        elif usrinput == "om stop":
            send_bytes = self.command_data.PC_CMD_TOUCH_DBG_STOP
        elif usrinput == "om restart":
            send_bytes = self.command_data.PC_CMD_TOUCH_RESTART

        else :
            show_warning("error", "Unknown command!")
            self.input_cmd.clear()
            return

        # 转成16进制字节并拼接数据
        send_bytes = bytes([0x53, send_bytes, 0x00])
        deviceComm.send_bytes(send_bytes)
        self.command_data.setUserCMD(send_bytes)
        self.input_cmd.clear()

        msg = "Sent command: " + " ".join("0x"+f"{b:02x}" for b in send_bytes)
        print(debug_log(msg))

    def show_log(self, msg):
        """
        显示日志
        :param msg: 日志消息
        """
        # 这里安全地操作GUI控件
        msg = debug_log(msg)
        print(msg)
        self.miniterminal.append(msg)


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
            self.devices[i] = Device(omconfig=self.omconfig, device_path=self.device_paths[i])
            if self.devices[i].check_connect():
                # 提取设备关键信息
                self.device_selector.addItem(f"Device {i + 1} ({self.devices[i].getDevicePath()[0][58:68]})")
                msg = f"Device {i + 1} ({self.devices[i].getDevicePath()[0][58:68]}) is connected."
                print(debug_log(msg))

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
        print(debug_log(f"Selected device: {device}"))
        print(debug_log(f"Selected deviceComm: {deviceComm}"))
        print(debug_log(f"Device connected, in port {port}"))

        return True

    def on_serial_data(self, data):
        """
        串口数据接收回调函数
        """
        # print(debug_log("接收到数据:", " ".join("0x"+f"{b:02x}" for b in data)))
        result = self.package_receiver.receive_byte(data)
        # 如果接收到完整的数据包，处理数据包
        if result is not None:
            # 设置接收完成变量
            self.cmd_listener.setIsReceive(True)
            self.command_data.setFullData(result)

        # self.miniterminal.append(f"<span style='color:blue;'>{result}</span>")

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