import queue
import threading
import signal
from lib.connects import Requester
import sys

thread_flag = True
Lock=threading.Lock()

class File_to_queue(threading.Thread):
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
    def __init__(self, que,rque,domain,port,save):
        super().__init__()
        self.domain=domain
        self.port=port
        self.queue = que
        self.save=save
        self.rque=rque

    def run(self) -> None:
        global thread_flag
        while thread_flag or not self.queue.empty():
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
                self.rque.put(self.result+'\n')
                global Lock
                Lock.acquire()
                print(self.result)
                Lock.release()

class Queue_to_file(threading.Thread):
    def __init__(self,que,path):
        super().__init__()
        self.que=que
        self.path=path
    def run(self) -> None:
        while thread_flag or not self.que.empty():
            with open(self.path,'a+') as f:
                f.write(self.que.get())



def quit(signum, frame):
    print('\nExting!')
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

