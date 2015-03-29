from io import StringIO
import json
import sys

import numerous
import requests


__author__ = 'Gson'
__date__ = '03-19-2015 21:41'

AUTHORIZATION_KEY = 'nmrs_HRDoaGPyGHXg'

PM25_TOKEN = '5j1znBVAsnSf5xQyNQyq'


def main():
    metric_id = sys.argv[1]
    city = sys.argv[2]
    quality = get_air_quality_v2(city)
    write_value(metric_id, quality['value'], quality['suggest'])
    pass


def get_air_quality(city):
    request_url = 'http://www.pm25.in/api/querys/pm2_5.json?city=%s&token=%s' % (city, PM25_TOKEN)
    result = requests.get(request_url)
    position_list = json.load(StringIO(result.text))
    for position in position_list:
        if position['position_name'] is None:
            return position['aqi']


def get_air_quality_v2(city):
    request_url = 'http://www.tianqi.com/air/%s.html' % city
    response_text = requests.get(request_url).text.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    value_anchor = '<divclass="num"><span>'
    start = response_text.index(value_anchor) + len(value_anchor)
    end = response_text.index('<', start)
    value = response_text[start:end]

    suggest_anchor = '空气质量分析：</h4><h5>'
    start = response_text.index(suggest_anchor) + len(suggest_anchor)
    end = response_text.index('<', start)
    suggest = '质量分析：' + response_text[start:end]

    suggest_anchor = '温馨提示：</h6><h5>'
    start = response_text.index(suggest_anchor) + len(suggest_anchor)
    end = response_text.index('<', start)
    suggest = suggest + '\n' + '温馨提示：' + response_text[start:end]

    return {'value': value, 'suggest': suggest}


def write_value(metric_id, value, comment=None):
    nr = numerous.Numerous(apiKey=AUTHORIZATION_KEY)
    metric = nr.metric(metric_id)
    metric.write(value)
    if int(value) > 175 and comment:
        metric.comment(comment)


if __name__ == "__main__":
    main()