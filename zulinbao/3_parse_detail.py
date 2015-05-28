import datetime
import gzip
import re

import pymongo
from bs4 import BeautifulSoup


PATH = '/Users/airsen/Downloads/dump/%s'


def main():
    db = pymongo.MongoClient(host='127.0.0.1')['zulinbao']
    pattem = re.compile('\d+')

    while True:
        item = db.item.find_one({'status': 1})
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
        item['cat1'] = seat.find(id='LinkBig').get_text().replace('出租', '')
        item['cat2'] = seat.find(id='LinkSmall').get_text().replace('出租', '')

        con_left = soup.find(class_='conLeft')
        if con_left.find(id='LblTime') is None:
            db.item.update({'id': item_id}, {'$set': {'status': -1}})
            continue
        item['update_time'] = datetime.datetime.strptime(con_left.find(id='LblTime').get_text(), '%Y-%m-%d %H:%M:%S')
        item['browsed_times'] = int(con_left.find(id='LblTouch').get_text())
        li_tag_list = []
        if con_left.find(class_='conInfoTop') is not None:
            li_tag_list.extend(con_left.find(class_='conInfoTop').find_all('li'))
        if con_left.find(class_='conInfoMid') is not None:
            li_tag_list.extend(con_left.find(class_='conInfoMid').find_all('li'))
        if con_left.find(class_='conInfoBot') is not None:
            li_tag_list.extend(con_left.find(class_='conInfoBot').find_all('li'))
            print('yeah!')
        for li_tag in li_tag_list:
            if li_tag.find('span') is not None:
                label = pretty(li_tag.span.get_text())
                if label == '租金':
                    item[label] = pretty(li_tag.find(class_='money').get_text())
                elif label == '押金':
                    tmp = li_tag.find(class_='money').get_text()
                    if tmp == '面议':
                        item[label] = tmp
                    else:
                        item[label] = int(pattem.findall(tmp)[0])
                else:
                    if len(li_tag.contents) == 2:
                        item[label] = pretty(li_tag.contents[1])
        if con_left.find(id='backman') is not None:
            li_tag_list.clear()
            li_tag_list.extend(con_left.find(id='backman').find_all('li'))
            for li_tag in li_tag_list:
                item[pretty(li_tag.contents[0])] = pretty(li_tag.span.get_text())
        if soup.find(id='Label28') is not None:
            location = pretty(soup.find(id='Label28').get_text()).replace('省', ' ').replace('市', ' ') \
                .replace('广西', '广西 ').replace('黑龙江', '黑龙江 ').replace('新疆', '新疆 ') \
                .replace('宁夏', '宁夏 ').replace('西藏', '西藏 ').replace('内蒙古', '内蒙古 ') \
                .replace('香港','香港 ')\
                .strip().split(' ')
            item['province'] = location[0]
            if len(location) == 2:
                item['city'] = location[1]

        item['author_id'] = item['author_id'].strip()
        item['status'] = 2
        db.item.update({'id': item_id}, {'$set': item})


def build_category_tree(category_tree):
    category_mapping = {}
    for category1 in category_tree:
        category_mapping[category1['name']] = category1['_id']
        for category in category1['sub']:
            category_mapping[category['name']] = category['_id']
    return category_mapping


def pretty(str):
    return str.strip().replace(' ', '').replace('：', '').replace('\u3000', '').replace('\xa0', '')


if __name__ == "__main__":
    main()
