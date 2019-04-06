#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import proxy
import time 
from Spider_Socks import Spider_Socks
from multiprocessing import Process
from pd_csv import SaveClient
import multiprocessing

class Scheduler(object):
    def __init__(self,use_proxy):
        self._useproxy=use_proxy
    def run(self): 
        print("启动主程序") 
        p = proxy.Proxy(self._useproxy)
        p.ConfigureTor
        print('爬取代理开始运行')
        t= Spider_Socks(self._useproxy)
        t.run() 
        print('继续运行Tor')
        
if __name__ == '__main__':
    print("启动检查代理") 
    use= SaveClient()
    proxies=use.useproxy()
    s = Scheduler(proxies)
    s.run()