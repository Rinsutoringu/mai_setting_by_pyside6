from PySide6.QtCore import QThread, Signal

class ButtonStatusWorker(QThread):
    status_changed = Signal(dict)

    def __init__(self, command_data, omconfig, parent=None):
        super().__init__(parent)
        self.command_data = command_data
        self.omconfig = omconfig
        self._running = True
        self.sleep_time = self.omconfig.getDisplayUpdateTime()  # 默认轮询时间为100毫秒

    def run(self):
        last_status = None
        while self._running:
            # 等待一段时间以避免过于频繁的轮询
            self.msleep(self.sleep_time)

            # 如果数据包指令不是0x12，继续等待
            if self.command_data.getCMD() != 0x12:
                continue

            status = self.command_data.getButtonStatus()
            # 如果按钮状态无效或未变化，继续等待
            if (not status) or (status == last_status):
                continue

            # 如果按钮状态有效且发生变化，发出信号
            self.status_changed.emit(status)
            last_status = status

            # 如果按钮状态发生变化，发出信号
            if last_status is not None:
                print("[调试信息]：按钮状态变化", last_status, "->", status)
            else:
                print("[调试信息]：初始按钮状态", status)

    def stop(self):
        self._running = False