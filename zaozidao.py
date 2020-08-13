#!/usr/bin/env python
# coding: utf-8

import os
from datetime import datetime
import time
import requests
import html2text as ht
from bs4 import BeautifulSoup

SHIBAO_URL = "http://www.gushixiaoxi.com/tag/etagid372/0"
ZHONGZHENG_URL = "http://www.gushixiaoxi.com/tag/etagid373/0"
SHANGZHENG_URL = "http://www.gushixiaoxi.com/tag/etagid374/0"

class Zaozhidao(object):
    def run(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.content, 'html.parser')
        target_url = soup.select('article header h2 a')[0]['href']

        req = requests.get(target_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        article = str(soup.select('.content_bw')[0])
        # adhoc
        article = article.replace('<p><br/></p>', '').replace('<p><br/>', '<p>')
        article = article.replace('您现在体验的是金融证券资讯，把握投资先机，尽享尊贵服务，资讯产品将助您决策领先一步、投资胜人一筹！', '')

        # add title
        article = '<h2>{}</h2>{}<br/>'.format(self.name, article)
        print(article)

        self.text = self.text_maker.handle(article)
        with open(self.output, 'w') as f:
            f.write(self.text)

        return 0

class Shibao(Zaozhidao):
    def __init__(self):
        self.name = '时报早知道'
        self.style_name = '<p style=\"color:red\">{}</p>'.format(self.name)
        self.text_maker = ht.HTML2Text()
        self.url = SHIBAO_URL
        self.output = '_'.join([datetime.now().strftime("%Y_%m_%d"), self.name]) + '.md'

class Zhongzheng(Zaozhidao):
    def __init__(self):
        self.name = '中证早知道'
        self.text_maker = ht.HTML2Text()
        self.url = ZHONGZHENG_URL
        self.output = '_'.join([datetime.now().strftime("%Y_%m_%d"), self.name]) + '.md'

class Shangzheng(Zaozhidao):
    def __init__(self):
        self.name = '上证早知道'
        self.text_maker = ht.HTML2Text()
        self.url = SHANGZHENG_URL
        self.output = '_'.join([datetime.now().strftime("%Y_%m_%d"), self.name]) + '.md'

def main():
    sb = Shibao()
    zz = Zhongzheng()
    sz = Shangzheng()

    sb.run()
    zz.run()
    sz.run()

    output = datetime.now().strftime("%Y_%m_%d") + '.md'
    with open(output, 'w') as f:
        f.write(sb.text + zz.text + sz.text)

if __name__ == '__main__':
    main()
