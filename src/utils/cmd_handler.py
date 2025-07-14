class CMD_Handler:
    def __init__(self, omconfig, command_data, mai_button, package_receiver):
        self.omconfig = omconfig
        self.signal = self.omconfig.getSignal()
        self.command_data = command_data
        self.mai_button = mai_button
        self.package_receiver = package_receiver

        # 连接信号和槽
        self.signal.command_signal.connect(self.handle_command)

    def handle_command(self, cmd):
        """
        处理接收到的命令
        """
        if cmd == self.command_data.PC_CMD_GET_SERIAL:
            pass

        if cmd == self.command_data.PC_CMD_TOUCH_DBG_START:
            pass

        elif cmd == self.command_data.PC_CMD_TOUCH_DBG_STOP:
            pass

        elif cmd == self.command_data.PC_CMD_TOUCH_DBG_DATA:
            self.mai_button.on_button_status_changed()

        elif cmd == self.command_data.PC_CMD_TOUCH_RESTART:
            pass

        elif cmd == self.command_data.PC_CMD_CFG_GET:
            pass

        elif cmd == self.command_data.PC_CMD_CFG_SET:
            pass

        elif cmd == self.command_data.PC_CMD_CFG_SAVE:
            pass