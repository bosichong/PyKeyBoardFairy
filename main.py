# -*- coding: utf-8 -*-
'''
PyKeyBoardFairy
Python编写的简单版键盘精灵

Python Flask Django 开心学习交流q群：217840699
Author  : J.sky
Mail    : bosichong@qq.com

'''



__version__ = "0.1.0"
from pynput.keyboard import Key, Controller, Listener
import threading
import time


'''
按键配置说明：
"key_type": "interval",#按键种类：
interval：魔法辅助技能键，间隔一定时间按一次
always：一直按着不放开的键，中间有少量的间暂停
"key_switch": Key.ctrl,#开关控制键，负责控制模拟这个技能键的开关
"key": 'b',#模拟的技能键
"is_start": 0,#开关，确定当前技能键在程序开启时，默认是关闭的，一般为0及可
"t": 0.5,#当前按键模拟按下离开的间隔时间，以秒为单位

'''
keyList = [
    {
        "key_type": "interval",
        "key_switch": Key.ctrl,
        "key": 'b',
        "is_start": 0,
        "t": 0.5,
    }, {
        "key_type": "always",
        "key_switch": Key.ctrl,
        "key": 'c',
        "is_start": 0,
        "t": 0.5,
        "t1":5
    },

]


key_b = {
    "key": 'b',
    "is_start": 0,
    "t": 0.5,
}
key_c = {
    "key": 'c',
    "is_start": 0,
    "t": 0.5,
}
key_d = {
    "key": 'd',
    "is_start": 0,
    "t": 0.5,
}

keyboard = Controller()


def on_press(key):
    ''''
    当开关键被按下，暂停或启动模拟按键
    '''
    for k in keyList:
        if key == k["key_switch"]:
            if k["is_start"] == 0:
                k["is_start"] = 1
            else:
                k["is_start"] = 0

def on_release(key):
    pass

def pressKey(key):
    '''技能键，有间隔时间'''
    while True:
        if key["is_start"]:
            keyboard.press(key["key"])
            keyboard.release(key["key"])
        time.sleep(key["t"])
        # print(keys["is_start"])

def pressKeyAlways(key):
    '''技能键，一直按着的及技能键，中间有少量时间间隔。'''
    while True:
        if key["is_start"]:
            keyboard.press(key["key"])
            time.sleep(key["t1"])
            keyboard.release(key["key"])
        time.sleep(key["t"])
        # print(keys["is_start"])


def createKeyThread(keylist):
    '''
    根据配置文件，创建所有的按键线程。
    '''

    for key in keylist:
        if key["key_type"] == "interval":
            # print(key["key_type"])
            t = threading.Thread(target=pressKey, args=(key,))
            t.start()
        elif key["key_type"] == "always":
            # print(key["key_type"])
            t1 = threading.Thread(target=pressKeyAlways, args=(key,))
            t1.start()
        else:
            raise "没有这种类型的按键，请检查并重新设置按键的类型！"


def main():
    createKeyThread(keyList)

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()




if __name__ == '__main__':
    main()