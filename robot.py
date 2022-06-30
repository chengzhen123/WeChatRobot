#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 14:01
# @Author  : ChengZhen

import requests
import json

## 调用青云客的API，免费的API
def qingyunke(msg:str):
    data = requests.get("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + msg).content
    data = json.loads(data)
    data = data['content'].replace("{br}","\n")
    return data


## 在本地创建的医疗机器人
## 有兴趣的可以参考 https://zhuanlan.zhihu.com/p/379202949 文章内容，将 local.py 改成api形式即可。
def medical_robot(msg:str):
    url = "http://localhost:60063/service/api/medical_robot"
    data = {"question": msg }

    print('data', data)
    headers = {'Content-Type': 'application/json;charset=utf8'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    # print('response', response)
    if response.status_code == 200:
        response = json.loads(response.text)
        # print(response, '========')
        return response["data"]
    else:
        return "您的问题我无法理解，我还需要学习"
