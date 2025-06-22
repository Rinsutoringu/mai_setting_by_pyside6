
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

    def __repr__(self):
        return f"Device({self.device_path}, {self.touch_port}, {self.aime_port}, {self.led_port}, {self.command_port})"

    def getDevicePath(self):
        return self.device_path

    def setPort(self, touch, aime, led, command):
        self.touch_port = touch
        self.aime_port = aime
        self.led_port = led
        self.command_port = command
        self.update_port()

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
    
    def update_port(self):
        """
        更新设备端口
        """
        # 添加设备端口更新逻辑
