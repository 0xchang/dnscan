import requests
from dns import resolver
from lib.settings import USER_AGENTS
import random

class Requester(object):
    def __init__(self,domain,port=None):
        super().__init__()
        if port is None:
            port=[]
        self.domain=domain
        self.port=port
        self.ip_true=False
        self.cdn=False
        self.UA=random.choice(USER_AGENTS)
        self.port_true=[]
    def dns_run(self):
        try:
            self.ip=resolver.resolve(self.domain,'A')
            if len(self.ip)>=2:
                self.cdn=True
            else:
                self.cdn=False
            self.ip_true=True
        except Exception:
            pass
    def request_run(self):
        if self.ip_true:
            headers={'User-Agent':self.UA}
            for port in self.port:
                if port==443:
                    url='https://'+self.domain
                else:
                    url='http://'+self.domain+':{}'.format(port)
                try:
                    res=requests.get(url=url,headers=headers,timeout=1)
                    self.port_true.append((port,res.status_code,))
                except Exception:
                    continue

    def get_result(self):
        if self.ip_true:
            ips=[]
            result='{: <30}'.format(self.domain)+'(have {} cdn)'.format('   ' if self.cdn else 'not')
            for ip in self.ip:
                ips.append(str(ip))
            result+=' '*3+str(ips)
            result+=' '*3
            if self.port_true!=[]:
                for port in self.port_true:
                    result+='(port:'+str(port[0])+',status:'+str(port[1])+') '
            return result
        else:
            return None



if __name__=='__main__':
    a=Requester('www.baidu.com',[80,443])
    a.dns_run()
    a.request_run()
    a.get_result()