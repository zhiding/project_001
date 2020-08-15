#!/usr/bin/env python
# coding: utf-8

import hashlib
from flask import Flask, request, make_response
import xml.etree.ElementTree as ET

WX_TOKEN = ""

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/wechat_api/", methods=['GET', 'POST'])
def access():
    if request.method == 'GET':
        token = WX_TOKEN
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        
        sort_str = ''.join(sorted[timestamp, nonce, echostr])
        if hashlib.sha1(sort_str.encode('utf-8')).hexdigest() == signature:
            response = make_response(echostr)
            response.headers['content-type'] = 'text'
            return response

if __name__ == '__main__':
    app.run()
