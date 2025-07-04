from utils.port_utils import read_com_port_number, write_com_port_value
from utils.warning import show_warning
from models.serial_model import SerialCommunicator



class Device:
    
    def __init__(self, device_path=None, touch_port=None, aime_port=None, led_port=None, command_port=None):
        """
        初始化设备对象
        """
        # 设备的注册表路径
        self.device_path = device_path
        # 触摸设备端口
        self.touch_port = touch_port
        # Aime设备端口
        self.aime_port = aime_port
        # LED设备端口
        self.led_port = led_port
        # Command设备端口
        self.command_port = command_port
        # 连接状态
        self.isConnect = False
        # serial comm object
        self.serial_comm = SerialCommunicator()  # 用于保存串口连接对象

        # TODO 自动获取设备当前各设备端口
        if device_path:
            self.get_port()
            self.check_connect()

    def __repr__(self):
        return f"[\nDevice RegPath: \n{self.device_path}\nConnect Status: {self.isConnect} \nTouch Port: {self.touch_port}, Aime Port: {self.aime_port}, LED Port: {self.led_port}, Command Port: {self.command_port}, \nSerial Comm: {self.serial_comm}\n]\n"

    def setDevicePath(self, device_path):
        self.device_path = device_path

    def getDevicePath(self):
        return self.device_path

    def setPort(self, touch, aime, led, command):
        self.touch_port = touch
        self.aime_port = aime
        self.led_port = led
        self.command_port = command

    def getPort(self, port_type):
        if port_type == "touch":
            return self.touch_port
        elif port_type == "aime":
            return self.aime_port
        elif port_type == "led":
            return self.led_port
        elif port_type == "command":
            return self.command_port

    def check_connect(self):
        """
        判断设备是否是当前设备
        """
        # 添加设备连接判断逻辑

        self.isConnect = True
        return True

    def setConnStatus(self, status):
        """
        设置设备连接状态
        """
        self.isConnect = status

    def get_port(self):
        """
        获取设备端口
        """
        if not self.device_path:
            show_warning("device error", "Device Path Not Found!")
            return

        self.touch_port = read_com_port_number(self.device_path[0])[3:]

        if self.touch_port is None:
            show_warning("device error", "Cannot get touch device port!")
        self.aime_port = read_com_port_number(self.device_path[1])[3:]

        if self.aime_port is None:
            show_warning("device error", "Cannot get aime device port!")
        self.led_port = read_com_port_number(self.device_path[2])[3:]

        if self.led_port is None:
            show_warning("device error", "Cannot get led device port!")
        self.command_port = read_com_port_number(self.device_path[3])[3:]
        
        # DEBUG
        # print(f"Device path: {self.device_path}")
        # print(f"Touch port: {self.touch_port}")
        # print(f"Aime port: {self.aime_port}")
        # print(f"LED port: {self.led_port}")
        # print(f"Command port: {self.command_port}")

        if self.command_port is None:
            show_warning("device error", "Cannot get command device port!")

    def set_port(self, port_type, port_value):
        """
        更新注册表设备端口
        """
        if self.device_path:
            port = "COM"+port_value
            if port_type == "touch_select":
                if not write_com_port_value(self.device_path[0], port):
                    show_warning("port error", "Change touch port fail!")
                    return
                self.touch_port = port_value
            elif port_type == "aime_select":
                if not write_com_port_value(self.device_path[1], port):
                    show_warning("port error", "Change aime port fail!")
                    return
                self.aime_port = port_value
            elif port_type == "led_select":
                if not write_com_port_value(self.device_path[2], port):
                    show_warning("port error", "Change led port fail!")
                    return
                self.led_port = port_value
            elif port_type == "command_select":
                if not write_com_port_value(self.device_path[3], port):
                    show_warning("port error", "Change command port fail!")
                    return
                self.command_port = port_value
        show_warning("port success", port_type + " is set to " + port_value)

    def setSerialComm(self, serial_comm):
        self.serial_comm = serial_comm

    def getSerialComm(self):
        return self.serial_comm