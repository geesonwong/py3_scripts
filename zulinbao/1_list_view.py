import datetime

from bson import ObjectId
import pymongo
import requests
from bs4 import BeautifulSoup

__author__ = 'Gson'
__date__ = '04-27-2015 22:50'

PAGE_URL = 'http://www.zulinbao.com/rentout%d.html'


def main():
    db = pymongo.MongoClient(host='127.0.0.1')['zulinbao']

    while True:
        record = db.record.find_one({'_id': ObjectId("553ee8f235a9279112f4ddcb")})['cursor']
        db.record.update({'_id': ObjectId("553ee8f235a9279112f4ddcb")}, {'$inc': {'cursor': 1}})
        print(record)

        response = None
        while response is None or response.find('n_pro_list') == -1:
            response = requests.get(PAGE_URL % record).text

        soup = BeautifulSoup(response)
        element_set = soup.find_all(class_='n_pro_list')
        count = 0

        for element in element_set:
            item = {'id': int(element.find(class_='goodTxt').find('a').attrs['href'][7:-5]), 'title': element.find(class_='goodTxt').find('a').attrs['title'].strip(),
                    'location': element.find(class_='dd_pro_con').next.strip(),
                    'post_time': datetime.datetime.strptime(element.find(class_='dd_pro_con').find(class_='grayColor').get_text().strip(), '%Y-%m-%d'), 'status': 0}
            tmp = element.find(class_='ddcon').find(class_='lineColor').find('a')
            if tmp is None:
                item['author_id'] = element.find(class_='ddcon').find(class_='lineColor').get_text().strip()
            else:
                item['author_id'] = tmp.get_text().strip() + ':' + tmp.attrs['href'][7:tmp.attrs['href'].index('.zulinbao')]

            count += 1
            db.item.update_one({'id': item['id']}, {'$set': item}, upsert=True)

        print('个数：' + str(count))


def find_next(start, string, start_keyword, end_keyword):
    original_start = start
    try:
        length = len(start_keyword)
        start = string.index(start_keyword, start) + length
        end = string.index(end_keyword, start)
    except Exception:
        return {'content': '', 'index': original_start}
    return {'content': string[start:end], 'index': end}


if __name__ == "__main__":
    main()
