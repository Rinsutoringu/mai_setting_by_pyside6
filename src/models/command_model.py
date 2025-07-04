

class CommandData:
    def __init__(self, command_id, command_params, command_size):
        self.command_id = command_id
        self.command_params = command_params
        self.command_size = command_size
        self.buttonStatus = None
        self.fulldata = None

    def __repr__(self):
        return f"CommandData(id={self.command_id}, params={self.command_params}, size={self.command_size}), buttonStatus={self.buttonStatus}, fullData={self.fulldata}"

    def clear(self):
        self.command_id = 0
        self.command_params = 0
        self.command_size = 0
        self.buttonStatus = None
        self.fulldata = None

    def setID(self, command_id):
        self.command_id = command_id

    def getID(self):
        return self.command_id

    def setFullData(self, full_data):
        self.fulldata = full_data

    def getFullData(self):
        return self.fulldata

    def setParams(self, command_params):
        self.command_params = command_params
        # print(f"DEBUG: CommandData.setParams called with {command_params}")
        if self.command_id == b'\x12':
            # print("DEBUG: Command ID is 0x12, processing button status matrix.")
            if not self.command_params or len(self.command_params) < 8:
                return [[0]*8 for _ in range(8)]
            matrix = []
            for i in range(8):
                byte = self.command_params[i]
                if isinstance(byte, str):
                    value = int(byte, 16)
                else:
                    value = byte
                bin_str = format(value, '08b')
                matrix.append([int(b) for b in bin_str])
            self.buttonStatus = matrix

    def getParams(self):
        return self.command_params

    def setSize(self, command_size):
        self.command_size = command_size

    def getSize(self):
        return self.command_size
        

    def getButtonBitsMatrix(self):
        """
        将 command_params[0:8] 转换而成的 8x8 的二进制二维数组。
        每个元素为 0 或 1。
        """
        return self.buttonStatus
    
