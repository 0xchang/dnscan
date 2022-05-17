import time
from tqdm import tqdm
import queue
import threading
import signal
from lib.connects import Requester
import sys

thread_flag = True
Lock=threading.Lock()
count=0

class File_to_queue(threading.Thread):
    '''将文件中的字典存入到相应的队列中'''
    def __init__(self, que, file_name: str = 'dic.txt'):
        super().__init__()
        self.queue = que
        self.file_name = file_name


    def run(self) -> None:
        for string in open(self.file_name, 'r'):
            self.queue.put(string)
        global thread_flag
        thread_flag = False


class Queue_to_req(threading.Thread):
    '''将队列中的数据取出，并提交给connect进行处理'''
    def __init__(self, que,rque,domain,port,save):
        super().__init__()
        self.domain=domain
        self.port=port
        self.queue = que
        self.save=save
        self.rque=rque


    def run(self) -> None:
        global thread_flag
        global count
        global Lock
        while thread_flag or not self.queue.empty():
            Lock.acquire()
            count+=1
            Lock.release()
            dns_child = self.queue.get().replace('\n', '').replace(' ', '')
            if dns_child == '':
                continue
            else:
                self.dn = dns_child + '.' + self.domain
                self.run_connects=Requester(self.dn,self.port)
                self.run_connects.dns_run()
                self.run_connects.request_run()
                self.result=self.run_connects.get_result()
                if self.result is None:
                    continue
                self.rque.put(self.result)
                Lock.acquire()
                tqdm.write(str(self.result))
                Lock.release()


class Queue_to_file(threading.Thread):
    '''将队列中的数据存入文件'''
    def __init__(self,que,path):
        super().__init__()
        self.que=que
        self.path=path
    def run(self) -> None:
        while thread_flag or not self.que.empty():
            with open(self.path,'a+') as f:
                infos=self.que.get()
                for info in infos:
                    f.write(str(info).replace(',','  ')+',')
                f.write('\n')

class Progress_bar(threading.Thread):
    '''创建一个进度条的线程'''
    def __init__(self,file_name):
        super().__init__()
        self.file_name=file_name
        self.flag=False
    def run(self) -> None:
        self.allcount=0
        global count
        for f in open(self.file_name):
            self.allcount+=1
        with tqdm(total=self.allcount) as pbar:
            self.count1=0
            while True:
                time.sleep(0.5)
                Lock.acquire()
                self.count2=count
                pbar.update(self.count2-self.count1)
                Lock.release()
                self.count1 = self.count2
                if self.count1>=self.allcount:
                    time.sleep(1)
                    break
        self.flag=True
    def getFlag(self):
        return self.flag



def file_count_line(file_name):
    f=open(file_name,'r')
    fcount=0
    for i in f:
        fcount+=1
    return fcount


def quit(signum, frame):
    tqdm.write('\nExting!')
    sys.exit(0)


if __name__ == '__main__':

    thread_flag = True
    signal.signal(signal.SIGINT,quit)
    signal.signal(signal.SIGTERM,quit)
    Lock = threading.Lock()
    thread_num = 5

    q = queue.Queue(thread_num * 10)
    rq=queue.Queue()
    threads = []

    thread = File_to_queue( q ,'../dic.txt')
    thread.setDaemon(True)
    threads.append(thread)



    for i in range(thread_num):
        thread = Queue_to_req(q,rq,'baidu.com',[80])
        thread.setDaemon(True)
        threads.append(thread)

    for thread in threads:
        thread.start()


    while True:
        if not thread_flag:
            break

