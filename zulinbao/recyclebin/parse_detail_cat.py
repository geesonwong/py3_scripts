import gzip

import pymongo
from bs4 import BeautifulSoup


PATH = '/Users/airsen/Downloads/dump/%s'


def main():
    db = pymongo.MongoClient(host='127.0.0.1')['zulinbao']

    while True:
        item = db.item.find_one({'status': 2,})
        if item is None:
            break
        item_id = item['id']

        file = gzip.open(PATH % (item_id % 999) + '/%s.html' % item_id, 'r')
        print(item_id)

        try:
            soup = BeautifulSoup(file.read().decode('utf8'))
            if soup.body.form['action'] == 'error.aspx':  # 错误页面
                raise Exception
        except Exception:
            db.item.update({'id': item_id}, {'$set': {'status': -1}})
            continue

        seat = soup.find(class_='seat')
        if seat is None:
            db.item.update({'id': item_id}, {'$set': {'status': -1}})
            continue
        item['cat1'] = pretty(seat.find(id='LinkBig').get_text()).replace('出租', '')
        item['cat2'] = pretty(seat.find(id='LinkSmall').get_text()).replace('出租', '')

        item['status'] = 3
        db.item.update({'id': item_id}, {'$set': item})


def pretty(str):
    return str.strip().replace(' ', '').replace('：', '').replace('\u3000', '').replace('\xa0', '')


if __name__ == "__main__":
    main()
