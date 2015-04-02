import datetime
from io import StringIO

import json

import numerous
import requests


__author__ = 'Gson'
__date__ = '04-02-2015 12:52'

AUTHORIZATION_KEY = 'nmrs_HRDoaGPyGHXg'
METRIC_ID = '2441999518851690821'


def main():
    next_holiday = get_next_holiday()
    value = get_value(next_holiday)
    comment = get_comment(next_holiday)
    write_value(value, comment)
    pass


def get_next_holiday():
    now_datetime = datetime.datetime.now()
    next_holiday_datetime = get_next_holiday_datetime(now_datetime.year)
    if next_holiday_datetime is None:
        next_holiday_datetime = get_next_holiday_datetime(now_datetime.year + 1)

    result = json.load(StringIO(requests.get('https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6018&query=' + next_holiday_datetime.strftime('%Y.%m.%d')).text))
    return result['data'][0]['holiday'][0]


def get_next_holiday_datetime(year):
    result = json.load(StringIO(requests.get('https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6018&query=' + str(year)).text))
    holiday_list = result['data'][0]['holidaylist']
    now = datetime.datetime.now()
    for day in holiday_list:
        if datetime.datetime.strptime(day['startday'], '%Y-%m-%d') > now:
            return datetime.datetime.strptime(day['startday'], '%Y-%m-%d')


def get_value(next_holiday):
    return datetime.datetime.strptime(next_holiday['list'][0]['date'], '%Y-%m-%d')


def get_comment(next_holiday):
    date_format = '{d.month}月{d.day}号'
    start = date_format.format(d=datetime.datetime.strptime(next_holiday['list'][0]['date'], '%Y-%m-%d'))
    end = date_format.format(d=datetime.datetime.strptime(next_holiday['list'][-1]['date'], '%Y-%m-%d'))
    return '下一个节日是' + next_holiday['name'] + '，' + start + '~' + end + '，假期长' + str(len(next_holiday['list'])) + '天。其中，' + next_holiday['desc']


def write_value(until_day, comment):
    nr = numerous.Numerous(apiKey=AUTHORIZATION_KEY)
    metric = nr.metric(METRIC_ID)
    if metric.read() == until_day.timestamp():
        return
    metric.write(until_day.timestamp())
    metric.comment(comment)


if __name__ == "__main__":
    main()