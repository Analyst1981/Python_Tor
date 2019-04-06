#!/usr/bin/python
#-*-coding:utf-8-*-

import random
import stem
from stem.control import Controller
import os,sys,time
import requests
from pd_csv import SaveClient
import shodan
from stem import Signal
from stem import process as tor_process
from stem.util import system, term
import stem.util.term

class Proxy:
    def __init__(self,proxy):
        if proxy:
            self._torproxy=proxy
        else:
            self._torproxy=self.shodan_torsocks()
             
    def shodan_torsocks(self):
        proxies=[]
        print('SHODAN WORKING START---') 
        api=shodan.Shodan("此处需要shodanKEY") #
        results=api.search('tor-socks') 
        for result in results['matches']:
            tor_proxy=result['ip_str']+":"+str(result['port'])
            proxies.append(tor_proxy)
        print('SHODAN WORKING END---') 
        return proxies  
    
    @property
    def ConfigureTor(self):
        def print_bootstrap_lines(line):
            print('{a}'.format(a=line))
            if "Bootstrapped " in line:
                print(line)#print(term.format(line,'Green'))
        os.system('TASKKILL /F /IM tor.exe')
        print("存入代理,启动TOR")
        try:
            tor_process.launch_tor_with_config(tor_cmd =os.getcwd()+'\\Tor\\tor.exe',
                config={
                    'SocksPort': '9050',
				    'ControlPort': '9051',
                    'DataDirectory': os.getcwd()+'\\Tor',
                    'GeoIPFile':os.getcwd()+'\\Tor\\geoip',
                    'GeoIPv6File':os.getcwd()+'\\Tor\\geoip6',
                    'Log notice file': os.getcwd()+'\\notices.log',
                    'HashedControlPassword':'16:9498BFA3B7CFC4DE607FE788AB55A0061EA2CC0EE78781B2F8C1FAE203',
                    'CookieAuthentication':'1',
                    'HiddenServiceStatistics':'0',
                    'Log notice': 'stdout',
                    'MaxCircuitDirtiness':'60',
                    'Socks5Proxy': random.choice(self._torproxy)
                    },
                    init_msg_handler=print_bootstrap_lines
                    )
        except:
            self._torproxy=self.shodan_torsocks()
            self.ConfigureTor