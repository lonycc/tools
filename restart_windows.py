# coding=utf-8

import os
import time
import re

#定义标题颜色及字体大小
def setUi():
    os.system('color B')
    os.system('mode con cols=100 lines=30')
    os.system('title 自动关机小工具')
    print('\n****预约关机服务****\n')


#计算关机时间函数
def calculate_time(dt):
    now = int(time.time())
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    book_time  = int(s)
    if book_time - now < 10:
        return False, 0
    return True, book_time - now

#定义关机服务
def shutdown_order():
    print('\n请输入关机日期\n',)
    get_date = input('格式yyyy-mm-dd, 如2018-03-12 \n-> ')
    if re.match(r'^(?:(?!0000)[0-9]{4}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[0-9]{2}(?:0[48]|[2468][048]|[13579][26])|(?:0[48]|[2468][048]|[13579][26])00)-02-29)$', get_date) == None:
        return '\n日期格式不规范'

    print('\n请输入关机时间\n')
    get_time = input ('格式hh:mm:ss, 如 10:30:00 \n-> ')
    if re.match(r'^([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$', get_time) == None:
        return '\n时间格式不规范'

    timeValid, seconds = calculate_time(get_date + " " + get_time)
    if timeValid == False:
        return '\n您输入的日期已经过期'
    else:
        shutdown_time = 'shutdown /s /t {0}'.format(seconds)
        response = os.system(shutdown_time)
        if response == 0:
            return '\n预定成功'
        else :
            return '\n预定失败'

#定义取消预约关机服务
def cancelled_order():
    response = os.system('shutdown /a')
    if response == 0:
        return '\n已经取消预约关机服务'
    else:
        return '\n没有任何预约关机服务'

#主程序
def main():
  setUi()
  print('\n', ' ' * 15,)
  get_order = input('预约关机请按S或s\n取消预约关机请按C或c \n-> ')
  if get_order == 'C' or get_order == 'c':
      response = cancelled_order()
      print(response)
  elif get_order == 'S' or get_order == 's':
      response = shutdown_order()
      print(response)
  else:
      print ('\n\n','命令有错误')
  print('\n\n','3秒后退出\n')
  time.sleep(3)

if __name__ == '__main__':
    main()
