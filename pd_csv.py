#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import pandas as pd
import requests
import random
import csv
from Tester import  TesterProxy

class SaveClient(object):
    def __init__(self):
        self.data_old = os.getcwd()+'\\checked_proxy.csv'

    def write(self,data):

        data_df= pd.DataFrame(data)
        data_df.to_csv(self.data_old,header=True)
        
        

    def read(self):
        data = pd.read_csv(self.data_old)
        return data

    def useproxy(self):
        
        t = TesterProxy()
        useproxy=t.run()
        return useproxy






