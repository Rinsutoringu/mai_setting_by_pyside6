

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

    def getParams(self):
        return self.command_params

    def setSize(self, command_size):
        self.command_size = command_size

    def getSize(self):
        return self.command_size
