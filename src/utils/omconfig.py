class omConfig:
    def __init__(self):
        self.update_time = 100
        self.serial_update_time = self.update_time
        self.display_update_time = self.update_time

        ###############################
        # please do not edit this config
        ###############################
        
        # 信号对象，各线程通过本类进行沟通
        self.signal = None


    def getUpdateTime(self):
        return self.update_time
    
    def getSerialUpdateTime(self):
        return self.serial_update_time

    def getDisplayUpdateTime(self):
        return self.display_update_time

    def setSignal(self, signal):
        self.signal = signal

    def getSignal(self):
        return self.signal