# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : portediter.py
# @Software: VScode

# todo: 需适配拼机场景
'''
实现思路：
    0.获取当前连接到计算机的所有usb设备,将其PID和VID返回为字典
    1.根据PID和VID寻找正确的设备
    2.读取这个usb复合设备
    3.把这个复合设备里面的四个子设备的设备名和端口号作为字典返回
    
'''

import usb.core
import usb.util
import serial.tools.list_ports
import serial


'''
这个函数将用来获取当前连接到计算机的所有usb设备
判断需要的USB设备在不在里面
如果在里面，返回True，否则返回False
参数：
    oniimai设备的PID和VID

返回：
    一个字典,键为设备PID,值为设备VID
'''
def getusbdevice(oniimai_pid, oniimai_vid):
    target_found = False

    # 获取所有USB设备
    devices = usb.core.find(find_all=True)
    usb_devices = {}


    
    # 遍历所有设备
    for device in devices:
        pid = device.idProduct
        vid = device.idVendor
        usb_devices[pid] = vid
        
        # 判断是否找到目标设备
        if device.idProduct == oniimai_pid:
            if device.idVendor == oniimai_vid:
                print("找到了目标设备")
                target_found = True
                return usb_devices, target_found
    return usb_devices, target_found

# 示例调用
if __name__ == "__main__":
    devices, target_found = getusbdevice(oniimai_pid = 0x8367, oniimai_vid = 0xAAEE)
    for pid, vid in devices.items():
        print(f"设备PID: {pid:#06x}, 设备VID: {vid:#06x}")
    if target_found:
        print("目标设备已连接")
    else:
        print("目标设备未连接")

'''
这个函数将用来获取特定USB复合设备的子设备信息

参数：
    target_pid: 目标设备的PID
    target_vid: 目标设备的VID

返回：
    一个字典，键为子设备名称，值为端口号
'''
def get_device_info(target_pid, target_vid):
    device = usb.core.find(idVendor=target_vid, idProduct=target_pid)
    if device is None:
        print("未找到目标设备")
        return None

    device_info = {}
    for cfg in device:
        for intf in cfg:
            for ep in intf:
                endpoint_address = ep.bEndpointAddress
                interface_number = intf.bInterfaceNumber
                device_info[f"子设备_{interface_number}"] = endpoint_address

    return device_info

# 示例调用
# if __name__ == "__main__":
#     devices, status = getusbdevice()
#     for pid, vid in devices.items():
#         print(f"设备PID: {pid}, 设备VID: {vid}")

#     if status:
#         print("Device found")
#         # 假设目标设备的PID和VID


#         device_info = get_device_info(target_pid, target_vid)
#         if device_info:
#             for name, port in device_info.items():
#                 print(f"{name}: 端口号 {port}")

#     else:print("Device not found")

'''
这个函数将用来修改指定串口设备的端口

参数：
    device_name: 设备名称
    new_port: 新的端口号

返回：
    True 表示成功，False 表示失败
'''
def setport(device_name, new_port):
    try:
        # 查找所有串口设备
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device == device_name:
                # 打开串口设备
                ser = serial.Serial(port.device)
                ser.port = new_port
                ser.close()
                print(f"设备 {device_name} 的端口已更改为 {new_port}")
                return True
        print(f"未找到设备 {device_name}")
        return False
    except Exception as e:
        print(f"更改端口时出错: {e}")
        return False

# 示例调用
# if __name__ == "__main__":
#     devices = getusbdevice()
#     for pid, vid in devices.items():
#         print(f"设备PID: {pid}, 设备VID: {vid}")

#     # 假设目标设备的PID和VID
#     target_pid = 0x1234  # 替换为实际的PID
#     target_vid = 0x5678  # 替换为实际的VID

#     device_info = get_device_info(target_pid, target_vid)
#     if device_info:
#         for name, port in device_info.items():
#             print(f"{name}: 端口号 {port}")

#     # 示例调用 setport 函数
#     device_name = "COM3"  # 替换为实际的设备名称
#     new_port = "COM4"  # 替换为新的端口号
#     setport(device_name, new_port)