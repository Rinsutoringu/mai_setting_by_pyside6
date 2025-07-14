from PySide6.QtCore import QThread, Signal
from utils.debuglog import debug_log


class CMD_listener(QThread):

    def __init__(self, command_data, omconfig, package_receiver, parent=None):
        super().__init__(parent)
        self.command_data = command_data
        self.omconfig = omconfig
        self._running = True
        self.sleep_time = self.omconfig.getUpdateTime()
        self.signal = self.omconfig.getSignal() # 获取信号句柄
        self.package_receiver = package_receiver
        self.isReceive = False # 信号量

    def run(self):
        while self._running:
            try:
                self.msleep(self.sleep_time)  # 等待一段时间以避免过于频繁的轮询
                # 每收到一个数据包就执行一次
                if self.getIsReceive():
                    self.setIsReceive(False)  # 重置接收完成变量
                    cmd = self.command_data.getCMD()
                    if cmd is not None:
                        self.signal.command_signal.emit(cmd)

            except Exception as e:
                print(debug_log("CommandListener error:", e))

    def stop(self):
        self._running = False

    def setIsReceive(self, isReceive):
        """
        设置接收完成变量
        """
        self.isReceive = isReceive

    def getIsReceive(self):
        """
        获取接收完成变量
        """
        return self.isReceive