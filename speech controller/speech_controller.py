#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
from playsound import playsound
import speech_recognition as sr
from aip import AipSpeech
import subprocess

AppID = "xxx"
API_Key = "xxx"
Secret_Key = "xxxx"

AIclient = AipSpeech(AppID,API_Key,Secret_Key)

project_path = os.path.dirname(os.path.abspath(__file__))

#录制语音record.wav文件中，采样率为：16K
def record(rate = 16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate = rate) as source:
        print("主人，我有什么能为你服务")
        audio = r.listen(source)
    with open(project_path + "\\record.wav","wb") as f:
        f.write(audio.get_wav_data())

#百度语音识别,wav -> text
def listen():
    with open(project_path + "\\record.wav","rb") as f:
        audio_data = f.read()
        AIresult = AIclient.asr(audio_data, 'wav', 16000,{'dev_pid':1536})
        result_text = AIresult["result"][0]
        print("你的指令是："+ result_text)
        return result_text

#百度语音讲话，text -> mp3
# playsound: 播放mp3
def speak(text=""):
    result = AIclient.synthesis(text, 'zh', 1, {
        'vol': 5,
    })

    if not isinstance(result, dict):
        with open(project_path + '\\audio.mp3', 'wb') as f:
            f.write(result)
            f.close()

    playsound(project_path + '\\audio.mp3')

speech_commands = {
    '关机': 'shutdown -s -t 1',
    '重启': 'shutdown -r',
    '打开火狐浏览器': [r'C:\Program Files\Mozilla Firefox\firefox.exe',"https://cn.bing.com/"],
    '关闭火狐浏览器': 'taskkill /F /IM firefox.exe',
    '打开QQ': r'C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe',
    '关闭QQ': 'taskkill /F /IM QQ.exe'
}

if __name__ == "__main__":
    speak("欢迎使用智能语音控制系统")
    while True:
        speak("请问您想要什么服务")
        record()
        command = listen()
        if command in speech_commands.keys():
            subprocess.Popen(speech_commands[command])
            speak("正在执行"+command+"任务")
        if command == "退出智能语音控制系统":
            speak("再见")
            exit()
