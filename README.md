# ideas

### `pip`国内下载源设置

> `C:\Users\xxx\AppData\Roaming`下创建`pip\pip.ini`文件，追加如下的内容。
```
[global]
timeout = 6000
index-url = http://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
```

#### 为了解决`playsound`不释放资源的问题，如下修改`playsound.py`文件。
> playsound里的winCommand函数的```if block:```之上添加下面的代码
```
    while True:
        if winCommand('status', alias, 'mode').decode() == 'stopped':
            winCommand('close', alias)
            break
```