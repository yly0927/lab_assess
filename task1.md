 任务一:

虚拟环境搭建  编辑器：Cursor  

软件：Anaconda，Git  

学习辅助：AI，b站

踩坑记录

1、cursor内置终端Powershell无法识别conda Anaconda安装时没有添加系统环境变量。普通PowerShell不会自动加载conda程序，所以无法识别conda命令。 

canda环境的创建，激活，包安装等操作使用Anaconda Powershell Prompt(独立终端)进行

2、在python交互环境中敲git,pip等命令

使用exit()退出python环境

3、创建文件时后缀弄错

熟悉Windows文件后缀，黄色图标不是代码文件

4、ai帮我梳理的python官网了安装指令，但是我配置git代理时，ai给的端口号与我的本地软件不一致

后续查阅代理软件的设置才改对

如何判断哪个版本的pytorch？

1、先确认自己电脑的配置（NVIDIA RTX 5060独显 AMD骁龙处理器）

 理论上适配CUDA，对应我的windows，且显卡驱动版本为592.01，应该装配CUDA版

2、经过尝试，CUDA版安装时网络多次超时、下载失败，后安装cpu版，后续网络稳定后再安装CUDA版。

3、随后进入pytorch官网，根据官网安装向导，复制安装指令，随后输入指令验证环境配置是否成功