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

#### 为了解决`playsound`不释放资源的问题，如下修改`playsound.py`文件。
> playsound里的winCommand函数的```if block:```之上添加下面的代码
```
    while True:
        if winCommand('status', alias, 'mode').decode() == 'stopped':
            winCommand('close', alias)
            break
```