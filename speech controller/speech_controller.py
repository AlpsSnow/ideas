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
AppID = "17679016"
API_Key = "BUc9Nj2LEej0f3wtcLpRdHyH"
Secret_Key = "ujsCYtPqgFn9mVk1dCj4uRna8ANEiA0O"
# 百度AI的客户端初始化
AIclient = AipSpeech(AppID,API_Key,Secret_Key)


#图灵机器人平台用
turing_apikey = "d30b5f0dd0ef488fa4051d699ede7472"
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
            print("你的指令不识别！")
            return  "指令不识别"

        result_text = AIresult["result"][0]
        print("你的指令是："+ result_text)
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
    os.system('ffmpeg.exe -i audio.mp3 -f wav audio.wav -y')    

    # 播放wav
    play(project_path + '\\audio.wav')

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

# The Turing chatbot
def turing_robot(text=""):
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
    #调用图灵机器人的rest api
    response = requests.request("post", turing_URL, json=data, headers=headers)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI 回答: " + result)    
    return result


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
        command = baiduARS()
        if command in speech_commands.keys():
            subprocess.Popen(speech_commands[command])
            speak("正在执行"+command+"任务")
        elif command == "退出系统":
            speak("再见")
            exit()
        elif command == "指令不识别":
            pass
        else:
            robot_resutl = turing_robot(command)
            speak(robot_resutl)