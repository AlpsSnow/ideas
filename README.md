# ideas

### `pip`国内下载源设置

> `windows`下配置方法：`C:\Users\xxx\AppData\Roaming`下创建`pip\pip.ini`文件，追加如下的内容。

> `linux`下配置方法：创建`.pip\pip.conf`文件，追加如下的内容后，拷贝到当前用户和`root`用户的`~`目录下。
```
[global]
timeout = 6000
index-url = http://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
```

### 使用
1.```pip install -r requirement.txt```
2.```pip install PyAudio```如果安装失败，参照`问题1`解决
3.将`ffmpeg.exe`的路径添加到系统环境变量`PATH`
3.```python speech_controller.py```

### 问题
问题1: Win10安装`PyAudio`失败（因为`SpeechRecognition`需要使用麦克风装置，所以必须安装`PyAudio`）

> 1.[下载PyAudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

> 2.pip install PyAudio的whl文件


问题2:`playsound`不释放资源 （目前已经放弃该方法）
> 如下修改`playsound.py`文件。
playsound里的winCommand函数的```if block:```之上添加下面的代码
```python
    while True:
        if winCommand('status', alias, 'mode').decode() == 'stopped':
            winCommand('close', alias)
            break
```


