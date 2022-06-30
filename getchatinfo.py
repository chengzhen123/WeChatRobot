#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 13:59
# @Author  : ChengZhen


from getocr import *
import pandas as pd

## 识别是否是对方发送消息的 x 点位
Location_Friend_Spt = 200
# GroupName = ['高艳子', '吴倩', '飞飞', '李苏娟']

def ChatInfo(fR_js):
    Friendlt = []
    Melt = []
    for word in fR_js['pages'][0]['lines']:
        if 'words' in word.keys():
            if word['coord'][0]['x'] < Location_Friend_Spt:
                print('Fri->', word['words'][0]['content'])
                Friendlt.append(word['words'][0]['content'])
            else:
                print('                                ', word['words'][0]['content'], '<-Me')
                Melt.append(word['words'][0]['content'])
    ## 返回朋友的所有消息
    return Friendlt

def OneChat(Frilt):
    ## 返回对方最新的消息
    return {'':Frilt[-1]}

def GroupChat(Frilt,GroupName):
    ## 获取群聊里面每个人最新消息
    def FriName(x):
        if x in GroupName:
            return x
        else:
            return pd.NA

    df = pd.DataFrame({"Dialogue": Frilt})
    df['FriName'] = df['Dialogue'].apply(FriName)
    df['FriName'] = df['FriName'].fillna(method='ffill')
    df['row_num'] = df.index.to_list()
    df = df[df['FriName'].notnull()]
    df = df.sort_values(['FriName','row_num'],ascending=[True,False]).drop_duplicates(['FriName'])
    ## 返回对方最新的消息
    dialogue = df['Dialogue'].tolist()
    FriName = df['FriName'].tolist()
    ## 将每个人最新消息，存储在json里面
    dial_info_json = {}
    for index, value in enumerate(dialogue):
        dial_info_json[FriName[index]] = value

    return dial_info_json


# if __name__ =='__main__':
#     filename = 'image/2022_06_29_16_26_55.jpg'
#     # filename ='C:\\Users\\Administrator\\Desktop\\1656492020518.png'
#     fR_js = OCR_XF(filename)
#     frilt = ChatInfo(fR_js)
#     print(frilt)
#     print ('==================================')
#     # print(OneChat(frilt))
#     print(GroupChat(frilt,GroupName))

    # print(Friendlt,'\n',Melt)


