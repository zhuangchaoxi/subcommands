# subcommands

## 功能概要

#### 因为subprocess本身没有直接提供实时获取命令执行输出，也没有提供命令超时的控制，所以该库主要是对subprocess进行了封装，实现了实时输出同时可以控制超时。

## 安装

<pre>pip install subcommands</pre>

## 使用方法
<pre>
#encoding: u8
from subcommands import BaseCommands

commandObj=BaseCommands()
commandObj.SubCommands("ifconfig; for i in {1..10};do echo $i && sleep 1;done", 5)  #会返回超时
commandObj.SubCommands("ifconfig; for i in {1..10};do echo $i && sleep 1;done", 60) #不会超时
commandObj.SubCommands("ifconfig; for i in {1..10};do echo $i && sleep 1;done") #也不会超时，默认超时时间1小时
</pre>
## 注意
#### SubCommands有两个参数，第一个是要执行的命令，第二个参数是超时时间，单位秒，可以不加，默认值是1小时。
