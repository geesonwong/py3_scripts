import gzip
import os

import pymongo
import requests

__author__ = 'Gson'
__date__ = '04-29-2015 07:50'

PAGE_URL = 'http://www.zulinbao.com/Product%d.html'
PATH = '/Users/airsen/Downloads/dump/%s'


def main():
    db = pymongo.MongoClient(host='127.0.0.1')['zulinbao']

    while True:
        item = db.item.find_one({'status': 0})
        if item is None:
            print('结束')
            return
        item_id = item['id']
        p = item_id % 999

        if not os.path.exists(PATH % p):
            os.makedirs(PATH % p)

        response = None
        while response is None:
            response = requests.get(PAGE_URL % item_id).text

        file = gzip.open(PATH % p + '/%s.html' % item_id, 'wb')
        file.write(bytes(response.replace('  ', ''), 'utf8'))

        file.close()
        db.item.update({'id': item_id, 'status': 0}, {'$set': {'status': 1}})
        print(item_id)


if __name__ == "__main__":
    main()
