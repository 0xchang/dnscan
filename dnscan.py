#dnscan-域名扫描工具
#time:2022/4/17 0:36
#Author: 0xchang



import queue
import time

import tqdm

from lib.opt import get_opt
from lib.opt import Option
from lib.mythread import File_to_queue
from lib.mythread import Queue_to_req
from lib.mythread import quit
from lib.mythread import Queue_to_file
from lib.mythread import Progress_bar
import signal

if __name__=='__main__':
    #设置信号
    signal.signal(signal.SIGINT,quit)
    signal.signal(signal.SIGTERM,quit)
    #获取参数
    opts=Option(get_opt())
    #设置队列
    que = queue.Queue(opts.getThread() * 10)
    rque=queue.Queue()
    #设置读入线程
    threads=[]
    readthread=File_to_queue(que,opts.getWordlist())
    readthread.setDaemon(True)
    threads.append(readthread)
    #设置进度条进程
    barthread=Progress_bar(opts.getWordlist())
    barthread.setDaemon(True)
    threads.append(barthread)
    #设置request线程
    for i in range(opts.getThread()):
        thread=Queue_to_req(que,rque,opts.getDomain(),opts.getPorts(),opts.getOutput())
        thread.setDaemon(True)
        threads.append(thread)
    #设置保存文件线程
    if opts.getOutput() is not None:
        thread=Queue_to_file(rque,opts.getOutput())
        thread.setDaemon(True)
        threads.append(thread)

    for thread in threads:
        thread.start()


    #设置循环，防止主线程提前退出
    while True:
        time.sleep(1)
        if barthread.getFlag():
            break

    print('\nThe scan of the domain name is completed!')
