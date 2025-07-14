from utils.debuglog import debug_log

class package_receive:
    AWAIT = 0       # 待命
    IN_PACKET = 1   # 正在读取
    ESCAPE = 2      # 转义状态

    def __init__(self, omconfig):
        self.state = self.AWAIT
        self.buffer = bytearray()
        self.packet = bytearray()
        self.omconfig = omconfig
        self.OMT = None

    def receive_byte(self, byte):
        # if self.OMT is None:
        #     self.OMT = self.omconfig.getOMT()
        
        # print(debug_log("传入的数据:", " ".join(f"0x{b:02x}" for b in byte)))
        for i in byte:
            if self.state == self.AWAIT:
                # 如果当前状态是待命状态，检查当前字节是否是包开始标志
                # 如果是包开始标志，就将状态设置为正在读取状态，并清空
                if i == 0x53:
                    self.state = self.IN_PACKET
                    self.buffer.clear()

            # 如果当前状态是正在读取状态
            if self.state == self.IN_PACKET:
                # 如果当前字节是转义字符就直接跳过
                if i == 0x7c:
                    self.state = self.ESCAPE
                    return
                else :
                    # 如果当前字节不是转义字符，就将其添加到数据缓冲区
                    self.buffer.append(i)
                # 检查数据缓冲区是否已经接收完一个完整的数据包
                if self.isFinish():
                    self.state = self.AWAIT
                    # print(debug_log("当前数据包接收完成:", " ".join(f"0x{b:02x}" for b in self.buffer)))
                    # self.OMT.append(debug_log("当前数据包接收完成"))
                    return self.buffer
                
            if self.state == self.ESCAPE:
                # 如果当前状态是转义状态，无论下一个字节是什么，都将其添加到数据缓冲区
                self.buffer.append(i)
                self.state = self.IN_PACKET


    def isFinish(self):

        # 检查是否收到了包头
        if len(self.buffer) < 4:
            return False
        
        # 包头已经确定收到了，确定PL是否完整收到
        # length是一个十六进制数，表示后续参数的长度，需要进行类型转换
        length = self.buffer[3]

        if len(self.buffer) < 4 + length:
            return False
        return True