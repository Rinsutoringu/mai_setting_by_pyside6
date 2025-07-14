class omConfig:
    def __init__(self):
        self.update_time = 50
        self.serial_update_time = self.update_time
        self.display_update_time = self.update_time

    def getUpdateTime(self):
        return self.update_time
    
    def getSerialUpdateTime(self):
        return self.serial_update_time

    def getDisplayUpdateTime(self):
        return self.display_update_time