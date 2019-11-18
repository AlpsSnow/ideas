#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import wave     #wav音频文件处理
import time     
import pyaudio  #播放wav音频文件
#from playsound import playsound
import speech_recognition as sr     #语音识别框架，调用麦克录音
from aip import AipSpeech           #百度AI
import subprocess
import requests         #访问图灵机器人rest api
import json

project_path = os.path.dirname(os.path.abspath(__file__))

#百度AI平台用
AppID = "xxxx"
API_Key = "xxxx"
Secret_Key = "xxxx"
# 百度AI的客户端初始化
AIclient = AipSpeech(AppID,API_Key,Secret_Key)


#图灵机器人平台用
turing_apikey = "xxxx"
turing_URL = "http://openapi.tuling123.com/openapi/api/v2"
headers = {'Content-Type': 'application/json;charset=UTF-8'}    #调用图灵API的各个环节的编码方式均为UTF-8

#录制语音record.wav文件s中，采样率为：16K
def record(rate = 16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate = rate) as source:        
        audio = r.listen(source)
    with open(project_path + "\\record.wav","wb") as f:
        f.write(audio.get_wav_data())

#百度语音识别,wav -> text
def baiduARS():
    with open(project_path + "\\record.wav","rb") as f:
        audio_data = f.read()
        AIresult = AIclient.asr(audio_data, 'wav', 16000,{'dev_pid':1536})
        if AIresult["err_no"] != 0:
            result_text = "指令不识别"            
            return  result_text

        result_text = AIresult["result"][0]        
        return result_text

#百度语音合成，text -> mp3
def baiduTTS(text=""):
    result = AIclient.synthesis(text, 'zh', 1, {
        'vol': 5,
    })

    if not isinstance(result, dict):
        with open(project_path + '\\audio.mp3', 'wb') as f:
            f.write(result)
            f.close()

def speak(text=""):
    # baidu TTS
    baiduTTS(text)

    # ffmpeg.exe: mp3->wav
    os.system('start /MIN /WAIT ffmpeg.exe -i audio.mp3 -f wav audio.wav -y')    

    # 播放wav
    play(project_path + '\\audio.wav')
    
    print(text)

# 播放wav
def play(wavfile):
    wf = wave.open(wavfile, 'rb')
    p = pyaudio.PyAudio()
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        stream_callback=callback)

    stream.start_stream()

    # 等待播放完成
    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

# 图灵机器人
def turing_robot(text=""):

    #构造图灵机器人请求数据
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": ""
            },
            "selfInfo": {
                "location": {
                    "city": "西安",
                    "province": "西安",
                    "street": "北大街"
                }
            }
        },
        "userInfo": {
            "apiKey": turing_apikey,
            "userId": "473767"
        }
    }
    data["perception"]["inputText"]["text"] = text

    #调用图灵机器人的REST API
    response = requests.request("post", turing_URL, json=data, headers=headers)
    response_dict = json.loads(response.text)

    #解析图灵机器人返回数据
    result = response_dict["results"][0]["values"]["text"]
    print("AI 回答: " + result)    
    return result

#控制命令
speech_commands = {
    #'关机': 'shutdown -s -t 1',
    #'重启': 'shutdown -r',
    '打开火狐浏览器': [r'C:\Program Files\Mozilla Firefox\firefox.exe',"https://cn.bing.com/"],
    '关闭火狐浏览器': 'taskkill /F /IM firefox.exe',
    '打开QQ': r'C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe',
    '关闭QQ': 'taskkill /F /IM QQ.exe'
}

if __name__ == "__main__":
    print("robot:",end = "")
    speak("欢迎使用智能语音控制系统:")
    while True:
        print("robot:",end = "")
        speak("请问您想要什么服务?")
        record() #录制语音
        command = baiduARS() #语音识别
        if command == "指令不识别":
            speak("抱歉，识别不了您的指令")
            pass
        else:
            print("你的指令是：{0}".format(command))        
            if command in speech_commands.keys():
                subprocess.Popen(speech_commands[command]) #执行控制命令
                speak("正在执行 "+command+" 任务")
            elif command == "退出系统":
                speak("再见")
                exit()       
            else:
                NLP_resutl = turing_robot(command) #图灵机器人做自然语音处理，聊天
                speak(NLP_resutl)