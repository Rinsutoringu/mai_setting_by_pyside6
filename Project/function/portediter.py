# -*- coding: utf-8 -*-
# @Time    : 2024/12/30
# @Author  : RinChord
# @File    : portediter.py
# @Software: VScode


'''
这个函数将用来获取当前usb设备的端口

参数为设备名称
返回：
    所获取的端口号(若无则返回None)
'''
def getport(device):
    port = "22", "33", "44", "55"
    print("现在获取",device, "设备的端口为", port)
    return port

'''
这个函数将用来修改当前usb设备的端口

参数为设备名称及需更改的端口号
返回：
    获取的端口号(若失败或无则返回None)
'''
def setport(device, port):
    print("现在设置",device, "设备为", port, "端口")