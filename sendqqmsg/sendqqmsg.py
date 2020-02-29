#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import win32gui
import win32con
import win32clipboard as w
import yaml
import os
import time
from PIL import Image
from io import BytesIO

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

def setImage(imgpath):
    img = Image.open(imgpath)
    output = BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    w.OpenClipboard() #打开剪贴板
    w.EmptyClipboard()  #先清空剪贴板
    w.SetClipboardData(win32con.CF_DIB, data)  #将图片放入剪贴板
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

def send_qq(to_who, msg_type, data):
    """发送qq消息
    to_who：qq消息接收人
    msg：需要发送的消息
    """
    # 将内容写到剪贴板
    if msg_type == 0 :
        setText(data)
    elif msg_type == 1 :
        setImage(data)

    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None, to_who)
    #show_window_attr(qq)   
    win32gui.ShowWindow(qq, win32con.SW_SHOWNORMAL)
    # 读取剪贴板消息到QQ窗体
    win32gui.SendMessage(qq, win32con.WM_PASTE,0,0)
    # 模拟按下回车键
    win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

# 解析yaml文件
def getConf():
    curPath = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(curPath,'qqmsg.yaml')

    f = open(yamlPath,'r',encoding='utf-8')
    cfg = f.read()    
    dict_obj = yaml.load(cfg, Loader=yaml.FullLoader)  
    return dict_obj


if __name__ == "__main__":
    print("qq群消息自动发送开始")
    conf = getConf()
    qqlist = conf['qq_group_name']
    msg_type = conf['msg_type']
    msg = conf['msg']
    imgname = conf['imgname']
    interval = conf['interval']
    print("发送QQ群名:{0}".format(qqlist))
    print("发送类型:{0}".format(msg_type))
    print("文字内容:{0}".format(msg))
    print("图片名:{0}".format(imgname))
    print("发送间隔:{0}".format(interval))

    imgpath = ''
    if msg_type == 1 or msg_type == 2:
        curPath = os.path.dirname(os.path.realpath(__file__))
        imgpath = os.path.join(curPath,imgname)

    while True:
        for qqname in qqlist:
            print("给{0}群发消息".format(qqname))
            if msg_type == 0 :
                send_qq(qqname, msg_type, msg)
            elif msg_type == 1 :
                send_qq(qqname, msg_type, imgpath)
            else :
                send_qq(qqname, 0, msg)
                send_qq(qqname, 1, imgpath)
        time.sleep(interval)

