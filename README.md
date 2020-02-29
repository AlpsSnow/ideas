# ideas

### `pip`国内下载源设置

> `windows`下配置方法：`%APPDATA%`下创建`pip\pip.ini`文件，追加如下的内容。

> `linux`下配置方法：创建`$HOME/.pip/pip.conf`文件，追加如下的内容后，拷贝到当前用户和`root`用户的`~`目录下。
```
[global]
timeout = 6000
index-url = http://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
```

### idea列表
1. [智能语音](./speech&#32;controller/readme.md)
2. [使用vscode调试ruby](./ruby/readme.md)
3. [定时自动给QQ群发送消息](./sendqqmsg/readme.md)
4. [读取银行回执单](./readreceipt/readme.md)
5. [用matplotlib画Chrome浏览器logo](./pltChromeLogo/readme.md)