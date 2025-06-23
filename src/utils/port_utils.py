# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : deviceinfo.py
# @Software: VScode


import winreg as reg
import usb.core
import usb.util


def find_device_reg_path(vid, pid):
    """
    注册表模式函数
    :param vid: 设备的 VID
    :param pid: 设备的 PID
    :return: 一个二维数组，列数为识别到的合法设备数量，行为每个串口子设备的注册表路径, 如果没有找到则返回 None
    """

    usb_path = "SYSTEM\\CurrentControlSet\\Enum\\USB"
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, usb_path) as usb_key:
            device_reg_paths = []
            index = 0
            code_executed = False
            for i in range(reg.QueryInfoKey(usb_key)[0]):

                # VID_xxxx&PID_xxxx&MI_xxxx
                subkey_name = reg.EnumKey(usb_key, i)

                # 检查该子键是否包含我们的 VID和 PID
                if not(vid in subkey_name and pid in subkey_name):
                    index = i
                    continue

                # 丢弃掉前三个设备（串口设备从第四个设备开始，本程序只关心对串口设备的处理）
                if i < index + 4:
                    continue
                
                # 找到合法设备后，打开该子设备的路径（串口设备在注册表中是一个单独的设备）
                full_key_path = f"{usb_path}\\{subkey_name}"
                with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, full_key_path) as device_key:
                    
                    # 获取子设备的子键数量,这是接入的oniimai设备数量,这段代码只会执行一次
                    if not code_executed:
                        device_number = reg.QueryInfoKey(device_key)[0]

                        # 根据设备数量扩容二维数组
                        for i in range(device_number):
                            device_reg_paths.append([])

                        code_executed = True
                    
                    for j in range(device_number):  

                        # 获取子键文件夹名
                        sub_subkey_name = reg.EnumKey(device_key, j) 
                         
                        # 进行字符串拼接，并把结果放入列表
                        device_reg_paths[j].append(f"{full_key_path}\\{sub_subkey_name}")
                        
            return device_reg_paths
    except Exception as e:
        return None

def find_device_usb_path(vid, pid):
    """
    USB模式函数
    :param vid: 设备的 VID
    :param pid: 设备的 PID
    :return: 一个二维数组，列数为识别到的合法设备数量，行为每个串口子设备的注册表路径
    """
    input_vid = int(vid, 16)
    input_pid = int(pid, 16)

    # 识别当前电脑上接入的全部合法设备
    device_serial = []
    usb_devices = usb.core.find(find_all=True, idVendor=input_vid, idProduct=input_pid)
    for index, usb_device in enumerate(usb_devices):
        serial_number = usb.util.get_string(usb_device, usb_device.iSerialNumber)
        device_serial.append([])
        
        # 进行注册表字符串拼接，读取父设备编号
        main_device_path = "SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_0CA3&PID_0021\\" + serial_number
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, main_device_path) as key_path:
            value_name = "ParentIdPrefix"
            parent_id = (reg.QueryValueEx(key_path, value_name))[0]

            # 进行注册表字符串拼接，分别读取四个子设备注册表路径
            device_serial[index].append("SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_0CA3&PID_0021&MI_02\\" + parent_id + "&0002")
            device_serial[index].append("SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_0CA3&PID_0021&MI_04\\" + parent_id + "&0004")
            device_serial[index].append("SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_0CA3&PID_0021&MI_06\\" + parent_id + "&0006")
            device_serial[index].append("SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_0CA3&PID_0021&MI_08\\" + parent_id + "&0008")
    return device_serial

def read_com_port_number(reg_path):
    """
    :param reg_path: 设备注册表路径
    :return: 字符串"COMx"或None
    """

    try:
        # 拼接地址字符串·
        parameters_path = f"{reg_path}\\Device Parameters"

        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, parameters_path) as param_key:
            com_port_number = reg.QueryValueEx(param_key, "PortName")[0]
            return com_port_number
            # 只有这个地址存在时才有返回值
    except Exception as e:
        return None


def write_com_port_value(registry_path, new_port_name):
    """
    :param registry_path: 待更改设备的注册表路径
    :param new_port_name: 设备待写入的新 COM 端口名
    :return: True or False
    """

    parameters_path = f"{registry_path}\\Device Parameters"
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, parameters_path, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, "PortName", 0, reg.REG_SZ, new_port_name)
            return True
    except Exception as e:
        # 修改失败
        return False




if __name__ == "__main__":
    """
    测试代码
    """

    # if not is_admin():
    #     print("请以管理员身份运行此脚本")
    #     exit(1)
    vid = "0CA3"  # 替换为你要查找的 VID
    pid = "0021"  # 替换为你要查找的 PID
    new_com_ports = ["COM46", "COM45", "COM44", "COM43"]  # 替换为你希望设置的新端口名
    index = 0
    which_device = 0  # 你想要访问连接到电脑的哪台设备?

    # 获取存储（多个）设备路径的二维数组

    device_paths = find_device_usb_path(vid, pid)

    # device_paths = find_device_reg_path(vid, pid)

    print("当前识别到", len(device_paths), "个设备")
    print("现在执行对", which_device+1, "号设备的更改")

    # 进一步查找有效的COM子设备
    # device_paths[which_device]指的是当前选择的设备的所有子设备路径
    for device_path in device_paths[which_device]:


        # 确定当前的设备是否是一个有效的 COM 设备，如果是的话则返回其端口
        # 读取当前 COM 端口号
        current_com_port = read_com_port_number(device_path)
        if current_com_port is None:
            print(f"{device_path} 不是一个有效的 COM 设备")
            continue
        # print(f"现在将 {device_path} 的 COM 端口更改为: {new_com_ports[index]}")

        # 更改 COM 端口
        if write_com_port_value(device_path, new_com_ports[index]) == False:
            print(f"更改 {device_path} 的 COM 端口失败")
        index += 1