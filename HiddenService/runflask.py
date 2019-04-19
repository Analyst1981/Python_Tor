#!/usr/bin/python
#-*-coding:utf-8-*-
from flask import Flask
from HiddenService import HiddenService
import start_tor 

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello onion!'


stor=start_tor.StartTor()
stor.run()
hidden = HiddenService()
print(hidden.onion)

port = hidden.ports[80]
app.run(port=port)