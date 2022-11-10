import argparse
import sys
import os

class Port(object):
    #将port字符串转为生成器
    def __init__(self,port:str):
        port=port.split(',')
        self.ports=[]
        for p in port:
            p=p.strip()
            if p=='':
                continue
            if p.isdigit():
                self.ports.append(int(p))
            elif '-' in p:
                p=p.split('-')
                if p[0].isdigit() and p[1].isdigit():
                    s,e=int(p[0]),int(p[1])
                    for i in range(s,e+1):
                        self.ports.append(i)
        self.ports=set(self.ports)

    def getPorts(self):
        for port in self.ports:
            yield port

class Option(object):
    #参数处理
    def __init__(self,parse_args):
        self.domain=parse_args.domain
        self.thread=parse_args.thread
        self.ports=Port(parse_args.port).getPorts()
        self.wordlist=parse_args.wordlist
        self.output=parse_args.output
    def getDomain(self):
        if '.' not in self.domain:
            sys.exit('Your domain name have wrong')
        return self.domain
    def getPorts(self):
        return self.ports
    def getThread(self):
        if self.thread<=0 or self.thread > 100:
            sys.exit('The number of threads should be greater than 0 and less than 100')
        return self.thread
    def getWordlist(self):
        if os.path.isfile(self.wordlist):
            return self.wordlist
        else:
            sys.exit('The wordlist is not a file!')
    def getOutput(self):
        if self.output is None:
            self.output=self.domain+'.csv'
        f=open(self.output,'w')
        f.write('域名,是否有cdn,IP地址,开放端口   状态码\n')
        f.close()
        return self.output


def get_opt():
    parse=argparse.ArgumentParser(description='A Domain Name Scaner')
    parse.add_argument('-d', '--domain', metavar='<domain>', help='set domain name',required=True)
    parse.add_argument('-p', '--port', metavar='<port>', default='80', help='set port/ports 80 or 80,443 or 80-443')
    parse.add_argument('-w','--wordlist',metavar='<file>',help='set domain name wordlist file',default='dic.txt')
    parse.add_argument('-t','--thread',metavar='<num>',type=int,help='set num of threads',default=10)
    parse.add_argument('-o','--output',metavar='<file>',help='output to file',default=None)
    return parse.parse_args()

if __name__ == '__main__':
    opts=get_opt()
    domain=opts.domain
    ports=Port(opts.port).getPorts()
    wordlist=opts.wordlist
    thread=opts.thread
    output=opts.output
    for port in ports:
        print(port)
