import ctypes


def is_admin():
    """
    验证当前用户是否是管理员
    :return: 不是返回False, 是返回True
    """
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        return False
    return True