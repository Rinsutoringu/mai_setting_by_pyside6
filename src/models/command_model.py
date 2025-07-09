

class CommandData:
    def __init__(self, command_id, command_params, command_size):
        self.command_id = command_id
        self.command_params = command_params
        self.payload_size = command_size
        self.buttonStatus = None
        self.fulldata = None
        self.vef = None
        self.usersendcmd = None

    def __repr__(self):
        return f"CommandData(id={self.command_id}, params={self.command_params}, size={self.payload_size}), buttonStatus={self.buttonStatus}, fullData={self.fulldata}"

    def clear(self):
        self.command_id = 0
        self.command_params = 0
        self.payload_size = 0
        self.buttonStatus = None
        self.fulldata = None

    def setFullData(self, full_data):
        self.fulldata = full_data

    # 获取数据包
    def setPayloadSize(self, payload_size):
        self.payload_size = payload_size

    def getPayloadSize(self):
        return self.payload_size

    # 转换为二进制并拼接在一起
    def converButtonStatus(self):
        buttonStatus = []
        for byte in self.command_params:
            for bit in range(8):
                # 从后往前依次取出每一位
                buttonStatus.append((bool((byte >> bit) & 1)))
        return buttonStatus

    def getButtonStatus(self):
        if self.command_id == b'\x12':
            return self.converButtonStatus()
        else :
            return None
        
    # 获取用户发送的指令
    def setUserSendCmd(self, cmd):
        self.usersendcmd = cmd

    def getUserSendCMDID(self):
        return self.usersendcmd
    
    def checkPacket(self):
        if self.getUserSendCMDID() is not None:
            msg = "[DEBUG] Start Checking command..."
            print(msg)
            if self.getCMDID() != self.getUserSendCMDID()[1:2]:
                msg = f"Command check failed, expected: {self.getUserSendCMDID()[1:2].hex()} but got: {self.getCMDID().hex()}"
                print(msg)
            else:
                self.setUserSendCmd(None)  # 无论成功失败都立即清空

    def handleFullData(self):
        """
        处理接收到的数据包
        """
        if self.fulldata is not None:
           # 处理完整数据包
           pass
        else:
            print("[DEBUG] Start handling full data.")
