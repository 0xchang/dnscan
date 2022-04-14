import queue
from lib.opt import get_opt
from lib.opt import Option
from lib.mythread import File_to_queue
from lib.mythread import Queue_to_req
from lib.mythread import quit
from lib.mythread import Queue_to_file
import signal






if __name__=='__main__':
    signal.signal(signal.SIGINT,quit)
    signal.signal(signal.SIGTERM,quit)
    opts=Option(get_opt())
    que=queue.Queue(opts.getThread()*10)
    rque=queue.Queue()
    threads=[]
    thread=File_to_queue(que,opts.getWordlist())
    thread.setDaemon(True)
    threads.append(thread)
    for i in range(opts.getThread()):
        thread=Queue_to_req(que,rque,opts.getDomain(),opts.getPorts(),opts.getOutput())
        thread.setDaemon(True)
        threads.append(thread)

    if opts.getOutput() is not None:
        for i in range(opts.getThread()):
            thread=Queue_to_file(rque,opts.getOutput())
            thread.setDaemon(True)
            threads.append(thread)

    for thread in threads:
        thread.start()



    while True:
        pass
