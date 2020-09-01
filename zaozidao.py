#!/usr/bin/env python
# coding: utf-8

import os
import re
from datetime import datetime
import time
import requests
import html2text as ht
from bs4 import BeautifulSoup

SHIBAO_URL = "http://www.gushixiaoxi.com/tag/etagid372/0"
ZHONGZHENG_URL = "http://www.gushixiaoxi.com/tag/etagid373/0"
SHANGZHENG_URL = "http://www.gushixiaoxi.com/tag/etagid374/0"

cookies = {
    "srcurl": "687474703a2f2f7777772e67757368697869616f78692e636f6d2f7461672f6574616769643337322f302f",
    "security_session_mid_verify": "211b25334c5a10beb20d87349ebfc876",
    "security_session_verify": "ed5089f69c1c29d11a62c84ec270d316"
}

headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}


class Zaozhidao(object):
    def markdown(self):
        pass

    def run(self):
        req = requests.get(self.url, cookies=cookies, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        target_url = soup.select('article header h2 a')[0]['href']

        req = requests.get(target_url, cookies=cookies, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        article = str(soup.select('.content_bw')[0])

        self.article = article

        self.markdown()

        self.text = self.text_maker.handle(self.article)
        with open(self.output, 'w') as f:
            f.write(self.text)

        return 0

class Shibao(Zaozhidao):
    def __init__(self):
        self.name = '时报早知道'
        self.style_name = '<p>{}</p>'.format(self.name)
        self.text_maker = ht.HTML2Text()
        self.url = SHIBAO_URL
        self.output = '_'.join([datetime.now().strftime("%Y_%m_%d"), self.name]) + '.md'

    def markdown(self):
        article = self.article
        # head 3
        article = article.replace('<br/>&gt;', '</b><br/><br/><b>+ ')
        article = article.replace('<br/><p>&gt;', '</b><br/><br/><b>+ ')
        # delete newline
        article = article.replace('<p><br/></p>', '').replace('<p><br/>', '<p>')
        # head 2
        article = article.replace('【资讯导读】</b><br/>', '<h3>资讯导读</h3>').replace(
                    '</p><br/>【主编视角】</b><br/>', '</b><br/><h3>主编视角</h3>').replace(
                    '<br/><br/>【今日头条】</b><br/>', '</b><br/><h3>今日头条</h3>').replace(
                    '【投资聚焦】</b><br/>', '<h3>投资聚焦</h3>').replace(
                    '【独家参考】</b><br/>', '<h3>独家参考</h3>').replace(
                    '【财经要闻】</b><br/>', '<h3>财经要闻</h3>').replace(
                    '<br/><br/>【公告淘金】<br/>', '</b><br/><h3>公告淘金</h3>').replace(
                    '【热点数据】</b><br/>', '<h3>热点数据</h3>').replace(
                    '【资金风向】</b><br/>', '<h3>资金风向</h3>').replace('。<br/>', '。<br/><br/>')
        # delete '------'
        article = article.replace('<br/>------<br/>', '</b><br/><br/>').replace('<br/></b><br/>', '<br/><br/>')
        #print(article)
        # title
        article = '<h1>{}</h1>{}<br/>'.format(self.name, article)
        self.article = article

class Zhongzheng(Zaozhidao):
    def __init__(self):
        self.name = '中证早知道'
        self.text_maker = ht.HTML2Text()
        self.url = ZHONGZHENG_URL
        self.output = '_'.join([datetime.now().strftime("%Y_%m_%d"), self.name]) + '.md'

    def markdown(self):
        article = self.article
        article = article.replace('您现在体验的是金融证券资讯，把握投资先机，尽享尊贵服务，资讯产品将助您决策领先一步、投资胜人一筹！', '')
        # delete newline
        article = article.replace('<p><br/></p>', '').replace('<p><br/>', '<p>')
        # head 2
        article = article.replace('<p>【今日导读】</p>', '<h3>今日导读</h3>').replace(
                    '<p>【中证头条】</p>', '<h3>中证头条</h3>').replace(
                    '<p>【中证聚焦】</p>', '<h3>中证聚焦</h3>').replace(
                    '<p>【要闻精选】</p>', '<h3>要闻精选</h3>').replace(
                    '<p>【产经透视】</p>', '<h3>产经透视</h3>').replace(
                    '<p>【公司动向】</p>', '<h3>公司动向</h3>').replace(
                    '<p>【资金观潮】</p>', '<h3>资金观潮</h3>').replace('。<br/>', '。<br/><br/>')
        #print(article)
        # title
        article  = '<h1>{}</h1>{}<br/>'.format(self.name, article)
        self.article = article

class Shangzheng(Zaozhidao):
    def __init__(self):
        self.name = '上证早知道'
        self.text_maker = ht.HTML2Text()
        self.url = SHANGZHENG_URL
        self.output = '_'.join([datetime.now().strftime("%Y_%m_%d"), self.name]) + '.md'

    def markdown(self):
        article = self.article
        # delete newline
        article = article.replace('<p><br/></p>', '').replace('<p><br/>', '<p>')
        # head 3
        article = article.replace('<br/>&gt;', '</b><br/><b>+ ')
        # head 2
        article = article.replace('【今日导读】</b>', '<h3>今日导读</h3>').replace(
                    '<br/>【上证聚焦】<br/>', '</b><br/><h3>上证聚焦</h3>').replace(
                    '<br/>【上证精选】<br/>', '<br/><h3>上证精选</h3>').replace(
                    '<br/>【产业情报】<br/>', '<br/><h3>产业情报</h3>').replace(
                    '<br/>【公告解读】<br/>', '<br/><h3>公告解读</h3>').replace(
                    '<br/>【交易闹铃】<br/>', '<br/><h3>交易闹铃</h3>').replace(
                    '<br/>【资金观潮】<br/>', '<br/><h3>资金观潮</h3>').replace('。<br/>', '。<br/><br/>')
        # add newline
        article = article.replace('<br/>------<br/>', '<br/><br/>------<br/><br/>')
        #print(article)
        # title
        article  = '<h1>{}</h1>{}<br/>'.format(self.name, article)
        self.article = article

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
