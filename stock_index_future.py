#!/usr/bin/env python
# coding: utf-8

import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from HTMLTable import HTMLTable
import json
import html2text as ht
import imgkit
from PIL import Image

class StockIndexFutureHandler(object):
    def __init__(self):
        self.type = "QHCC"
        self.sty = "QHSYCC"
        self.stat = 4
        self.mkt = "069001009"
        self.cmd = 8005022 # 中信
        #self.fd = datetime.now().strftime("%Y-%m-%d")
        self.fd = "2020-08-14"
        self.name = 1 # 持仓结构
        self.url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type={}&sty={}&stat={}&mkt={}&cmd={}&fd={}&name={}".format(
                    self.type, self.sty, self.stat, self.mkt, self.cmd, self.fd, self.name)

    def html_table(self):
        self.caption = "{} 中信期货持仓结构".format(self.fd)
        table = HTMLTable(caption=self.caption)
        # table head
        table.append_header_rows((
            ("", "成交情况 (手)", "", "多头持仓 (手)", "", "空头持仓 (手)", "", "净持仓 (手)", ""),
            ("合约", "成交量", "增减", "多单量", "增减", "空单量", "增长", "净多单", "净空单")
        ))
        table[0][1].attr.colspan = 2
        table[0][3].attr.colspan = 2
        table[0][5].attr.colspan = 2
        table[0][7].attr.colspan = 2

        # table row
        response = requests.get(self.url)
        rows = response.text[3:-3].split('\",\"')
        rows_in_table = list()
        for row in rows:
            eles = row.split(',')
            if eles[0][:2] not in ["IC", "IF"]:
                continue
            rows_in_table.append(
                (eles[0], eles[2], eles[3], eles[4], eles[5], eles[6], eles[7], eles[8], eles[9]))
        table.append_data_rows(tuple(rows_in_table))


        table.set_cell_style({
            'text-align': 'center',
            'font-size': '12px',
            'vertical-align': 'inherit',
            'border': '1px solid #95AFC0',
            '#border-right': '1px solid #95AFC0',
            '#border-bottom': '1px solid #95AFC0',
            'border-collapse': 'collapse',
            'padding': '6px',
            'padding-right': '10px',
            'padding-left': '10px'
        })
        table.set_header_cell_style({'text-align': 'center', 'font-size': '12px'})
        table.caption.set_style({'text-align': 'center', 'font-size': '18px'})

        for row in table.iter_data_rows():
            for cell in row[2:-2:2]:
                if int(cell.value) < 0:
                    cell.set_style({'color': 'green'})
                elif int(cell.value) > 0:
                    cell.set_style({'color': 'red'})
            for cell in row[1:]:
                if int(cell.value) == 0:
                    cell.value = ""

        table.set_row_style({
            'border': '1px solid #95AFC0',
            'border-collapse': 'collapse'
        })
        table.set_style({
            'border-spacing': '2px',
            'font-family': 'Arial',
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap'
        })
        self.table = table

        html = table.to_html()
        with open('{}.html'.format(self.caption), 'w') as f:
            f.write(html)

        return 0

def main():
    handler = StockIndexFutureHandler()
    handler.html_table()
    options = {'encoding': 'utf-8'}
    imgkit.from_file('{}.html'.format(handler.caption), '{}.png'.format(handler.caption), options=options)
    image = Image.open('{}.png'.format(handler.caption))
    image = image.crop([0, 0, image.size[0] / 2, image.size[1]])
    image.save('{}.png'.format(handler.caption))

if __name__ == '__main__':
    main()
