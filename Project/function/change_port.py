# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : deviceinfo.py
# @Software: VScode

## vid=0x0CA3, pid=0x0021
'''

'''
import winreg as reg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 参数： vid：设备的 VID， pid：设备的 PID
# 返回： 一个包含符合当前设备注册表路径的列表
def find_device_usb_path(vid, pid):
    usb_path = "SYSTEM\\CurrentControlSet\\Enum\\USB"
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, usb_path) as usb_key:
            device_reg_paths = []
            for i in range(reg.QueryInfoKey(usb_key)[0]):

                # VID_xxxx&PID_xxxx&MI_xxxx
                subkey_name = reg.EnumKey(usb_key, i)

                # 检查该子键是否包含我们的 VID和 PID
                if not(vid in subkey_name and pid in subkey_name):
                    continue

                full_key_path = f"{usb_path}\\{subkey_name}"
                with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, full_key_path) as device_key:
                    for j in range(reg.QueryInfoKey(device_key)[0]):  # 获取子键数量
                        sub_subkey_name = reg.EnumKey(device_key, j)  # 获取子键名称
                        device_reg_paths.append(f"{full_key_path}\\{sub_subkey_name}")
                        
            return device_reg_paths
    except Exception as e:
        print(f"错误: {e}")
    return None

def read_com_port_number(reg_path):
    """
    :param reg_path: 设备注册表路径
    :return: 字符串"COMx"或None
    """
    try:
        parameters_path = f"{reg_path}\\Device Parameters"
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, parameters_path) as param_key:
            com_port_number = reg.QueryValueEx(param_key, "PortName")[0]
            return com_port_number
            
    except Exception as e:
        return None


# 参数：  registry_path：待更改设备的注册表路径，例Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USB\VID_0CA3&PID_0021&MI_06\6&166091be&0&0006\Device Parameters
#         new_port_name：设备待写入的新 COM 端口名
def write_com_port_value(registry_path, new_port_name):
    # print("现在开始更改")
    parameters_path = f"{registry_path}\\Device Parameters"
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, parameters_path, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, "PortName", 0, reg.REG_SZ, new_port_name)
            # print(f"成功将 {parameters_path} 的 PortName 更改为: {new_port_name}")
    except Exception as e:
        print(f"修改 {parameters_path} 的 PortName 时发生错误: {e}")



if __name__ == "__main__":
    if not is_admin():
        print("请以管理员身份运行此脚本")
        exit(1)
    vid = "0CA3"  # 替换为你要查找的 VID
    pid = "0021"  # 替换为你要查找的 PID
    new_com_ports = ["COM6", "COM51", "COM21", "COM90"]  # 替换为你希望设置的新端口名
    index = 0

    # 查找设备路径
    device_paths = find_device_usb_path(vid, pid)

    for path in device_paths:
        print(f"现在查找设备路径{path}")


    # 进一步查找有效的COM子设备
    for device_path in device_paths:
        print(f"现在查找设备路径{device_path}")
        current_com_port = read_com_port_number(device_path)
        if current_com_port is None:
            print(f"{path} 不是一个有效的 COM 设备")
            continue
        print(f"现在将 {path} 的 COM 端口更改为: {new_com_ports[index]}")
        write_com_port_value(path, new_com_ports[index])
        index += 1