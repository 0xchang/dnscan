# dnscan

#### 介绍
A dnscan tool

#### 软件架构
```
+--- dic.txt
+--- dnscan.py
+--- lib
|   +--- connects.py
|   +--- mythread.py
|   +--- opt.py
|   +--- settings.py
```


#### 安装教程

pip install -r requirements.txt

#### 使用说明

python dnscan.py -h

#### 更新 2022-11-10
修补使用p参数时使用eval函数存在的安全漏洞。


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


