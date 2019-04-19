#!/usr/bin/python
#-*-coding:utf-8-*-
from io import StringIO 
import socket 
import socks  # SocksiPy module 
import stem.process  
from stem.util import term
import sys
import time
import stem
from stem.connection import connect
import datetime
import os
import shodan
import random
"""
def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))
print(term.format("Starting Tor:\n", term.Attr.BOLD))

tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort': str(SOCKS_PORT),
    'ExitNodes': '{ru}',
  },
  init_msg_handler = print_bootstrap_lines,
)

print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
print(term.format(query("https://www.atagar.com/echo.php"), term.Color.BLUE))

tor_process.kill()  # stops tor


"""


class StartTor(object):
    def __init__(self):
        #self.shodan_torsocks()
        with open("tor-socks.txt","r") as f:
            self.tor_socks=f.readlines()
        
    def shodan_torsocks(self):
        #proxies=[]
        f=open("tor-socks.txt","w")
        print('SHODAN WORKING START---')
        try:
            api=shodan.Shodan("") #此处需要shodan的KEY
            results=api.search('tor-socks') 
            for result in results['matches']:
                tor_proxy=result['ip_str']+":"+str(result['port'])
                f.write(tor_proxy)
                f.write("\n")
        except shodan.APIError as e:
            print("Error:%s"%e)
        f.close()
            #proxies.append(tor_proxy)
        print('SHODAN WORKING END---') 
        #return proxies  
    

    def start_tor(self):
        print("[{d}]- 启动TOR -".format(d=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))  
        def print_bootstrap_lines(line):
            if "Bootstrapped " in line:
                print(line) 
        try:
            stem.process.launch_tor_with_config(tor_cmd =os.getcwd()+'\\Tor\\tor.exe',
                config = {'SocksPort': '9050','ControlPort': '9051',  #str(SOCKS_PORT),
                'DataDirectory': os.getcwd()+'\\Tor',
                'GeoIPFile':os.getcwd()+'\\Tor\\geoip',
                'GeoIPv6File':os.getcwd()+'\\Tor\\geoip6',
                'HashedControlPassword':'16:9498BFA3B7CFC4DE607FE788AB55A0061EA2CC0EE78781B2F8C1FAE203',  #password='r0oth3x49'
                'CookieAuthentication':'1',
                #'HiddenServiceStatistics':'0',
                'Log': ['NOTICE stdout','notice file '+os.getcwd()+'\\notices.log',
                    'ERR file '+os.getcwd()+'\\tor_error_log',
                        ],
                #'HiddenServiceDir':os.getcwd()+'\\data',
                #'HiddenServicePort':'80  127.0.0.1:5000',
                'MaxCircuitDirtiness':'60',
                'Socks5Proxy': '{}'.format(random.choice(self.tor_socks)),
                },timeout = 90,init_msg_handler = print_bootstrap_lines,
                ) 
        except:
            self.start_tor()
    def run(self):
        if(os.name=="nt"):
            os.system('TASKKILL /F /IM tor.exe')
        self.start_tor()