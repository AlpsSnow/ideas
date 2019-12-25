#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import win32gui
import win32con
import win32clipboard as w
import yaml
import os
import time

def getText():
    """获取剪贴板文本"""
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d

def setText(aString):
    """设置剪贴板文本"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

def show_window_attr(hWnd):
    '''
    显示窗口的属性
    :return:
    '''
    if not hWnd:
        return
    title = win32gui.GetWindowText(hWnd)    
    clsname = win32gui.GetClassName(hWnd) 
    print('窗口句柄:%s ' % hWnd)
    print('窗口标题:%s' % title)
    print('窗口类名:%s' % clsname)

def send_qq(to_who, msg):
    """发送qq消息
    to_who：qq消息接收人
    msg：需要发送的消息
    """
    # 将消息写到剪贴板
    setText(msg)
    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None, to_who)
    #show_window_attr(qq)   
    win32gui.ShowWindow(qq, win32con.SW_SHOWNORMAL)
    # 读取剪贴板消息到QQ窗体
    win32gui.SendMessage(qq, win32con.WM_PASTE,0,0)
    # 模拟按下回车键
    win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


# 测试
to_who='匆匆那些屌丝'
msg='这是测试消息'
#send_qq(to_who, msg)

def getConf():
    curPath = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(curPath,'qqmsg.yaml')

    f = open(yamlPath,'r',encoding='utf-8')
    cfg = f.read()    
    dict_obj = yaml.load(cfg)  
    return dict_obj


if __name__ == "__main__":
    print("qq群消息自动发送开始")
    conf = getConf()
    qqlist = conf['qq_group_name']
    msg = conf['msg']
    interval = conf['interval']
    print("发送QQ群名:{0}".format(qqlist))
    print("发送内容:{0}".format(msg))
    print("发送间隔:{0}".format(interval))

    while True:
        for qqname in qqlist:
            print("给{0}群发消息".format(qqname))
            send_qq(qqname, msg)            
        time.sleep(interval)

