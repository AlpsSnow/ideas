### 定时自动给QQ群发送消息

#### 使用
1. 配置文件：qqmsg.yaml
```yaml
# qq群名
qq_group_name: ['匆匆那些屌丝','小猪淘宝优惠群']

# 发送内容
msg: '自动发送消息测试消息'

# 发送间隔：10秒一次
interval: 10
```

2. 发送群消息时要求qq群的窗口是独立的，现在新版的qq一般都是将所有的聊天窗口聚合在一起，因此要设置将qq窗口分离，或者将需要发送消息的那个窗口单独分离出来。 

3. 执行`dist/sendqqmsg.exe`

#### 将py文件转换为exe文件
1. 安装 pyinstaller
```python
pip install pyinstaller
```
2. 利用 pyinstaller 将py文件转换为exe文件
```python
pyinstaller -F sendqqmsg.py
```
3. 最终的打包的exe文件存在dist目录下

参考：https://blog.csdn.net/weixin_43846898/article/details/90339976
