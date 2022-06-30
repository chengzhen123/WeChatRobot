#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 14:00
# @Author  : ChengZhen

import glob
import os
from PIL import ImageGrab, Image
import time
import pyperclip
from pymouse import PyMouse
from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()
file_path = "image/"

def snapshot():
	# 屏幕快照方法
    # (x1, y1), (x2, y2) 用于控制对屏幕聊天截图的范围
    # 需要自己调整 两个点位的分辨率坐标
    (x1, y1), (x2, y2) = (400, 80), (3840 / 2 - 300, 2160 - 490)
    box = (x1, y1, x2, y2)
    pic = ImageGrab.grab(box)
    name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    full_path = os.path.join(file_path, '%s.jpg' % name)
    pic.save(full_path)
    return full_path

## 删除屏幕截图
def remove_snapshot(full_path):
    if os.path.exists(full_path):
        os.remove(full_path)

## 用鼠标控制在微信输入框输入
def mock_msg(msg: str):
	# 模拟键鼠发消息方法
    # 获取机器人回答
    answer = msg
    # 复制文本到剪贴框
    pyperclip.copy(answer)
    pyperclip.paste()
    # 模拟鼠标点击，用于获取聊天软件输入框焦点
    x_pos = 260
    y_pos = 1260
    print('x', x_pos, 'y', y_pos)
    m.click(x_pos, y_pos, 1)
    # 模拟键盘点击 ctrl+v，用于将剪贴框文字粘贴到输入框
    k.press_key(k.control_key)
    k.tap_key('v')
    k.release_key(k.control_key)
    # 模拟键盘发送消息
    k.tap_key(k.enter_key)

