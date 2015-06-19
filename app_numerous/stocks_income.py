import datetime
from io import StringIO
import json
import time

import numerous
import requests

__author__ = 'Gson'
__date__ = '04-01-2015 15:33'

AUTHORIZATION_KEY = 'nmrs_HRDoaGPyGHXg'
GAIN_METRIC_ID = '7109893350453685640'
TOTAL_METRIC_ID = '7993294341318871002'

LIST = """
SZ000333,46.208,2000
SH600276,60.156,1300
"""
BALANCE = 13730.36  # 余额
COST = 110000  # 成本


def main():
    stocks = build_list()
    am_start = datetime.time(hour=9, minute=30)
    am_end = datetime.time(hour=11, minute=31)
    pm_start = datetime.time(hour=13, minute=0)
    pm_end = datetime.time(hour=15, minute=1)

    while True:
        now_time = datetime.datetime.now().time()
        if am_start <= now_time <= am_end or pm_start <= now_time <= pm_end:
            income = 0
            total_price = 0
            for stock in stocks:
                current_price = get_price(stock[0])
                income += (float(current_price) - stock[1]) * stock[2]
                total_price += float(current_price) * stock[2]
            total = BALANCE + total_price  # 总资产
            write_value(TOTAL_METRIC_ID, round(total, 3))
            income = total - COST  # 总收入
            write_value(GAIN_METRIC_ID, round(income, 3))
            time.sleep(60 - datetime.datetime.now().time().second)
        elif now_time < am_start or now_time > pm_end:
            return
        else:
            time.sleep(1.5 * 60 * 60)


def build_list():
    stocks = []
    for stock in LIST.strip().split('\n'):
        eles = stock.split(',')
        stocks.append([eles[0], float(eles[1]), int(eles[2])])
    return stocks


def get_price(code):
    headers = {
        'Host': 'xueqiu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }
    response = requests.get("http://xueqiu.com", headers=headers)
    cookie_str = ""
    for item in response.cookies.iteritems():
        cookie_str = cookie_str + item[0] + "=" + item[1] + ";"
    headers['Cookie'] = cookie_str
    request_url = "http://xueqiu.com/v4/stock/quote.json?code=%s" % code
    response = requests.get(request_url, headers=headers)
    stocks = json.load(StringIO(response.text))
    return stocks[code]['current']


def write_value(metric_id, value):
    nr = numerous.Numerous(apiKey=AUTHORIZATION_KEY)
    metric = nr.metric(metric_id)
    metric.write(value)
    print(value)


if __name__ == "__main__":
    main()
