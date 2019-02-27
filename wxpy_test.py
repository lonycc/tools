# -*- utf-8 -*-

from threading import Timer
from wxpy import Bot
import random
from time import sleep
import datetime
import sys

bot = Bot(cache_path=True)
group_name = 'your_group_name'
group_msg = 'your_group_msg'
private_name = 'your_contact_name'
private_msg = 'your_contact_msg'

def sendMessage():
    try:
        group = bot.groups().search(group_name)[0]
        friend = bot.friends().search(private_name)[0]
        a = datetime.datetime.now()
        h = str(a)[11:13]  #获取hour
        m = str(a)[14:16]  #获取minute
        if h == '12' and m[0:1] == '0':  #12时零几分发送群消息然后退出
            group.send(group_msg)
            msg = friend.send(private_msg)
            sleep(5)
            msg.recall()
            sys.exit(0)
        print('.', end='')
        # t = Timer(300, sendMessage)
        ran_int = random.randint(0, 100)
        t = Timer(300 + ran_int, sendMessage)
        t.start()
    except Exception as e:
        print(str(e))
        sys.exit(0)

if __name__ == '__main__':
    sendMessage()
