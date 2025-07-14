from utils.debuglog import debug_log

class CommandData:
    def __init__(self, omconfig, command, payload, payload_length):

        self.PC_CMD_GET_SERIAL = 0x00       # 序列号
        self.PC_CMD_TOUCH_DBG_START = 0x10  # 触摸调试开始
        self.PC_CMD_TOUCH_DBG_STOP = 0x11   # 触摸调试结束
        self.PC_CMD_TOUCH_DBG_DATA = 0x12   # 触摸调试结束
        self.PC_CMD_TOUCH_RESTART = 0x13    # 触摸调试结束

        self.PC_CMD_CFG_GET = 0x20          # 获取配置
        self.PC_CMD_CFG_SET = 0x21          # 设置配置
        self.PC_CMD_CFG_SAVE = 0x23         # 保存配置

        self.command = command
        self.payload = payload
        self.payload_length = payload_length
        self.buttonStatus = None
        self.fulldata = None
        self.status = None
        self.usersendcmd = None
        self.omconfig = omconfig
        self.signal = None  # 获取log句柄
        # print(1)

    def __repr__(self):
        return f"CommandData(id={self.command}, params={self.payload}, size={self.payload_length}), buttonStatus={self.buttonStatus}, fullData={self.fulldata}"

    # 获取用户发送的指令
    def setUserCMD(self, cmd):
        self.usersendcmd = cmd

    def getUserCMD(self):
        return self.usersendcmd

    # 获取接收到的指令
    def setFullData(self, full_data):
        self.fulldata = full_data
        self.SplitData()

    def SplitData(self):
        if self.signal is None:
            self.signal = self.omconfig.getSignal()
        if self.fulldata is not None:
            index = 1
            self.command = self.fulldata[index]
            index += 1
            self.status = self.fulldata[index]
            index += 1
            self.payload_length = self.fulldata[index]
            index += 1
            self.payload = self.fulldata[index:index + self.payload_length]

            self.checkPacket()


    # 内部函数
    def getCMD(self):
        if self.fulldata is not None:
            return self.command
    def getStatus(self):
        if self.fulldata is not None:
            return self.status
    def getPLL(self):
        if self.fulldata is not None:
            return self.payload_length
    def getPL(self):
        if self.fulldata is not None:
            return self.payload

    # button状态的内部方法：将8个uint8从小位拼接成一个64位bool数组
    def convertButtonStatus(self):
        buttonStatus = []
        # payload字段前八位是按钮状态的bool值
        for byte in self.payload[0:8]:
            for bit in range(8):
                # 从后往前依次取出每一位
                buttonStatus.append((bool((byte >> bit) & 1)))
        return buttonStatus

    # 获取按钮状态数组
    def getButtonStatus(self):
        if self.command == self.PC_CMD_TOUCH_DBG_DATA:
            return self.convertButtonStatus()
        else :
            return None
        
    # 确定回复的指令是否与发送指令一致
    def checkPacket(self):
        if self.getUserCMD() is not None:
            msg = debug_log("Start Checking command...")
            self.signal.log_signal.emit(msg)

            if self.getUserCMD()[1:2] != self.getCMD().to_bytes(1, 'big'):
                # msg = f"Command check failed, user input: 0x{self.getUserCMD()[1:2].hex()} but got: 0x{self.getCMD().to_bytes(1, 'big').hex()}"
                msg = debug_log("CMD Check Failed")
                self.signal.log_signal.emit(msg)

                self.setUserCMD(None)
                return False
            
            else:
                self.setUserCMD(None)  
                msg = debug_log("Command check passed.")
                self.signal.log_signal.emit(msg)

                return True