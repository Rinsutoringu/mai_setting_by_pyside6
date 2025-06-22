from PySide6.QtWidgets import QMessageBox

def show_warning(errortype="warning", message="Something went wrong!"):
    """
    显示警告弹窗
    :param message: 警告信息
    """
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle(errortype)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()