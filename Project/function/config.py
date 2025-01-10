# -*- coding: utf-8 -*-
# @Time    : 2025/1/11
# @Author  : RinChord
# @File    : config.py
# @Software: VScode

import json


class Config:
    
    def __init__(self, file_path):

        # 初始化配置文件路径
        self.file_path = file_path
        # 载入配置文件内容
        self.config = Config.load_config(file_path)
        if not self.config:
            print("配置文件为空")
            return False

    def load_config(file_path):
        try:
            with open(file_path, 'r') as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("配置文件格式错误")
            return {}

    def save_config(file_path, config):
        with open(file_path, 'w') as file:
            json.dump(config, file, indent=4)