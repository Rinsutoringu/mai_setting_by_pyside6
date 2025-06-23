from utils.port_utils import read_com_port_number, write_com_port_value
from utils.warning import show_warning


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

        # TODO 自动获取设备当前各设备端口
        if device_path:
            self.get_port()
            self.check_connect()

    def __repr__(self):
        return f"Device({self.device_path},{self.isConnect} {self.touch_port}, {self.aime_port}, {self.led_port}, {self.command_port})"

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

    def get_port(self):
        """
        获取设备端口
        """
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
        if self.command_port is None:
            show_warning("device error", "Cannot get command device port!")

    def set_port(self, port_type, port_value):
        """
        更新注册表设备端口
        """
        if self.device_path:
            port = "COM"+port_value
            if port_type == "touch":
                if not write_com_port_value(self.device_path[0], port):
                    show_warning("port error", "Change touch port fail!")
                self.touch_port = port_value
            elif port_type == "aime":
                if not write_com_port_value(self.device_path[1], port):
                    show_warning("port error", "Change aime port fail!")
                self.aime_port = port_value
            elif port_type == "led":
                if not write_com_port_value(self.device_path[2], port):
                    show_warning("port error", "Change led port fail!")
                self.led_port = port_value
            elif port_type == "command":
                if not write_com_port_value(self.device_path[3], port):
                    show_warning("port error", "Change command port fail!")
                self.command_port = port_value