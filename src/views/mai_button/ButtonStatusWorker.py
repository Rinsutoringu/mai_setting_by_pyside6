from PySide6.QtCore import QThread, Signal

class ButtonStatusWorker(QThread):
    status_changed = Signal(dict)  # 或者传递你需要的结构

    def __init__(self, command_data, parent=None):
        super().__init__(parent)
        self.command_data = command_data
        self._running = True

    def run(self):
        last_status = None
        while self._running:
            # 获取按钮状态（假设为字典或二维数组）
            status = self.command_data.getButtonBitsMatrix()  # 或 getButtonBitsMatrix()
            if status != last_status:
                self.status_changed.emit(status)
                last_status = status
            self.msleep(20)  # 20ms轮询一次

    def stop(self):
        self._running = False