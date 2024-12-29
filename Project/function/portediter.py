# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : portediter.py
# @Software: VScode


import serial.tools.list_ports

'''
这个函数将用来获取当前usb设备的端口

参数为设备名称
返回：
    所获取的端口号(若无则返回None)
'''

# todo: 需适配拼机场景
def getdevices() -> dict:
    ports = serial.tools.list_ports.comports()
    port_dict = {}
    for port in ports:
        if port.description in ["Mai Pico AIME Port", 
                                "Mai Pico LED Port", 
                                "Mai Pico Command Line Port", 
                                "Mai Pico Touch Port"]:
            port_dict[port.device] = port.description
        else: continue
    return port_dict



'''
这个函数将用来修改当前usb设备的端口

参数为设备名称及需更改的端口号
返回：
    获取的端口号(若失败或无则返回None)
'''
def setport(device, port):
    print("现在设置",device, "设备为", port, "端口")