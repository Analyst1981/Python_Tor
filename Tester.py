#!/usr/bin/python
#-*-coding:utf-8-*-

import asyncio
import aiohttp
from aiosocksy import Socks5Auth
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
import time,os,sys
import pandas as pd 

class TesterProxy(object):
    def __init__(self):
       
        self.useproxy=[]
    
    async def test_single_proxy(self,proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        #auth = Socks5Auth(login=None, password=None),
        connector = ProxyConnector()
        socks = 'socks5://'+proxy
        print("测试代理{0}".format(proxy))
        async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
            try:
                async with session.get('http://spys.one',proxy=socks) as resp: # proxy_auth=auth
                    #print(await resp.text())
                    if resp.status == 200:
                        self.useproxy.append(proxy)
                        print("存入代理{0}".format(proxy))
            except: #aiohttp.ProxyConnectionError:
                #print('connection problem')
                pass
                
    def run(self):
        """
        测试主函数
        :return:
        """
        print('测试器开始运行')
        data = pd.read_csv(os.getcwd()+'\\checked_proxy.csv')
        #print(data['0'])
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in data['0'][:10]]
            loop.run_until_complete(asyncio.wait(tasks))
            sys.stdout.flush()
            time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
        return self.useproxy
if __name__ == '__main__':
    m=TesterProxy()
    m.run()