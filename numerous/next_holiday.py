import datetime

import numerous


__author__ = 'Gson'
__date__ = '03-28-2015 08:38'

AUTHORIZATION_KEY = 'nmrs_HRDoaGPyGHXg'
METRIC_ID = '2441999518851690821'

DESC = """
20150405,3,清明节
20150501,3,劳动节
20150208,7,春节
20150620,3,端午节
20150927,3,中秋节
20151001,7,国庆节
"""


def main():
    holidays = build_holidays()
    next_holiday = get_next_holiday(holidays)
    comment = get_detail(next_holiday)
    write_value(next_holiday[0], comment)
    pass


def build_holidays():
    holidays = []
    for day in DESC.strip().split('\n'):
        strs = day.split(',')
        holidays.append([strs[0], int(strs[1]), strs[2]])
    return holidays


def get_next_holiday(holidays):
    index = []
    holidays.sort(key=lambda day: day[0])
    for (i, next_day) in enumerate(holidays):
        date_time = datetime.datetime.strptime(next_day[0], '%Y%m%d')
        if date_time > datetime.datetime.now():
            index.append([datetime.datetime.strptime(next_day[0], '%Y%m%d'), next_day[1], next_day[2]])
    index.sort(key=lambda day: day[0])
    return index[0]


def get_detail(next_holiday):
    date_format = '{d.month}月{d.day}号'
    start = date_format.format(d=next_holiday[0])
    end = date_format.format(d=next_holiday[0] + datetime.timedelta(days=next_holiday[1] - 1))
    return '下一个节日是' + next_holiday[2] + '，' + start + '~' + end + '，假期长' + str(next_holiday[1]) + '天，'


def write_value(until_day, comment):
    nr = numerous.Numerous(apiKey=AUTHORIZATION_KEY)
    metric = nr.metric(METRIC_ID)
    if metric.read() == until_day.timestamp():
        return
    metric.write(until_day.timestamp())
    metric.comment(comment)


if __name__ == "__main__":
    main()