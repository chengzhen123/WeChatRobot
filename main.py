#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 13:59
# @Author  : ChengZhen

from getscreen import *
from getocr import *
from getchatinfo import *
from robot import *
## 是否是群聊
IsGroupChat = 1
## 群聊中所有的朋友的昵称
GroupName = ['高艳子', '吴倩', '飞飞', '李苏娟','微辣帅小镇']
GroupName = ['吴瑶', '万慧', '李磊', '微辣帅小镇']
GroupName = ['陈士轩', '白帆', '微辣帅小镇']

IsStopDialog = 0

## 10s 回复一次
sleeptime = 10

if __name__ == "__main__":
    ## 判断是否是群聊
    if IsGroupChat==1:
        LastChat = "lastchat/groupchat.txt"
    else:
        LastChat = "lastchat/onechat.txt"

    with open(LastChat, "w+", encoding="utf-8") as o:
        o.write("{'Robot':'~~~重置对方的最后一句话~~~'}")
        o.close()

    ## 打招呼
    mock_msg('您好，我是医疗机器人，请和我聊天吧！')

    while IsStopDialog==0:
        ## 屏幕截图
        f_path = snapshot()
        print(f_path)
        ## 识别截图内容
        fR_js = OCR_XF(f_path)
        ## 删除截图
        # remove_snapshot(f_path)
        ## 截取 对方发送的消息 列表
        message_lt = ChatInfo(fR_js)
        #### 得到最后一句聊天内容，并且，最后一句是对方发出
        if IsGroupChat == 1:
            finalText = GroupChat(message_lt,GroupName)
        else:
            finalText = OneChat(message_lt)

        ## 删除引用自己谈话的内容，如果是引用其他人的，可以将微信昵称，放在到 GroupName中
        if '微辣帅小镇' in finalText.keys():
            del finalText['微辣帅小镇']

        ## 读出上一次最后一句话内容
        with open(LastChat, encoding="utf-8") as f:
            data = f.readlines()[0]
            data = json.loads(data.replace("'", '"'))
            f.close()

        ## 存储当前最后一句话
        with open(LastChat, "w+", encoding="utf-8") as o:
            o.write(str(finalText))
            o.close()

        ## 判断每个人是否是最新消息，如果不是，就删除此人，只保留有最新消息的人
        del_k = []
        for k in finalText.keys():
            if (k in data.keys()):
                if finalText[k]==data[k]:
                    print(k,'没有发出最新消息')
                    del_k.append(k)
        for i in del_k:
            del finalText[i]

        ## 只回复 有最新消息的人
        if finalText!={}:  ## 说明有最人发出最新消息
            for k in finalText.keys():
                try:
                    # answer = "这个是机器人回复：\n" + "@" + k + " " + qingyunke(finalText[k])
                    ## 医疗机器人，需要开启医疗机器人的服务
                    answer = "这个是机器人回复：\n" + "@" + k + " " +  medical_robot(finalText[k])
                except:
                    answer = "这个是机器人回复：\n" + "@" + k + " 对不起：我还无法理解您的意思，请换一种说法。"
                ## 发出内容
                # print(answer)
                mock_msg(str(answer))
        else:
            print('没有人发出最新消息')

        ## 10s一次
        time.sleep(sleeptime)
        ## 到达预定的时间，会自动断开
        if datetime.now().minute == 30:
            IsStopDialog = 1
            mock_msg("这个是机器人回复："  + "聊天时间到，下次再聊哦")


