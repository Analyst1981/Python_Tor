#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import re
import time
import random
import threading
from multiprocessing import Pool
import requests
from requests.exceptions import ConnectionError
from pd_csv import SaveClient
import string




class Spider_Socks(object):

    def __init__(self,proxy):
        self.saveclient= SaveClient()
        self._xpp= '5'
        self._xf1='4'
        self._xf2 = '0'
        self._xf4 = '0'
        self._xf5 = '2'
        if proxy:
            self._proxy_=random.choice(proxy)
            
        else:
            self._proxy_='127.0.0.1:9050'
            
        self.unchecked = []
        

    def get_index(self):
        print('爬取代理开始')
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'}
        data = {
            'xpp': self._xpp,
            'xf1': self._xf1,
            'xf2': self._xf2,
            'xf4': self._xf4,
            'xf5': self._xf5
            }
        print("参数准备完毕")
        while True:
            try:
                proxies={'http':'socks5://'+self._proxy_,'https':'socks5://'+self._proxy_}
                rsp = requests.post('http://spys.one/en/socks-proxy-list/', headers=header,proxies=proxies,data=data)
                if rsp.status_code == 200:
                    html = rsp.text
                    print("已经获得网页数据")
                    return html
            except ConnectionError:
                #self._proxy_='127.0.0.1:9050'
                proxies={'http':'socks5h://127.0.0.1:9050','https':'socks5h://127.0.0.1:9050'}
                try:
                    rsp = requests.post('http://spys.one/en/socks-proxy-list/', headers=header,proxies= proxies,data=data)
                    if rsp.status_code == 200:
                        html = rsp.text
                        print("已经获得网页数据")
                        return html
                except ConnectionError:
                    use= SaveClient()
                    self._proxy_=random.choice(use.useproxy())
                    print('Please run your proxy app and try again.')
            continue
    def get_proxy_info(self,html):
        pattern = re.compile('onmouseout.*?spy14>(.*?)<s.*?write.*?nt>\"\+(.*?)\)</scr.*?\/en\/(.*?)-', re.S)
        infos = re.findall(pattern, html)
        return infos

    def parse_proxy_info(self,html,infos):
        print('Get {} proxies.'.format(len(infos)))
        print('Start to get proxy details...')
        port_word = re.findall('\+\(([a-z0-9^]+)\)+', html)
        # DECRYPT PORT VALUE
        port_passwd = {}
        #print (html)
        portcode = (re.findall('table><script type="text/javascript">(.*)</script>', html))[0].split(';')
        for i in portcode:
            ii = re.findall('\w+=\d+', i)
            for i in ii:
                kv = i.split('=')
                if len(kv[1]) == 1:
                    k = kv[0]
                    v = kv[1]
                    port_passwd[k] = v
                else:
                    pass
        # GET PROXY INFO
        for a in infos:
            proxies_info = {
                'ip': a[0],
                'port': a[1],
                'protocol': a[2]
                }
            port_word = re.findall('\((\w+)\^', proxies_info.get('port'))
            port_digital = ''
            for s in port_word:
                port_digital += port_passwd[s]
            test_it = '{0}://{1}:{2}'.format(proxies_info.get('protocol'), proxies_info.get('ip'), port_digital)
            if 'socks' in test_it:
                test_it = '{0}:{1}'.format(proxies_info.get('ip'), port_digital)
            print("存入代理{}".format(test_it))
            self.unchecked.append(test_it)
        return self.unchecked
    def run(self):
        html = self.get_index()
        infos = self.get_proxy_info(html)
        proxies=self.parse_proxy_info(html,infos)
        self.saveclient.write(proxies)