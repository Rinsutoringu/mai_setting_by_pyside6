from PySide6.QtCore import QThread, Signal

class ButtonStatusWorker(QThread):
    status_changed = Signal(dict)

    def __init__(self, command_data, parent=None):
        super().__init__(parent)
        self.command_data = command_data
        self._running = True

    def run(self):
        last_status = None
        while self._running:
            # 获取按钮状态
            # print("Polling button status...")
            status = self.command_data.getButtonStatus()
            if status is None:
                # print("No button status available.")
                continue
            print("获取有效按钮状态")
            if status != last_status:
                self.status_changed.emit(status)
                last_status = status
            self.msleep(100) #轮询时间配置

    def stop(self):
        self._running = False