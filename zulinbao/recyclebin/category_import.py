from bson import ObjectId
import pymongo

__author__ = 'Gson'
__date__ = '05-01-2015 11:30'

FILE = '/Users/airsen/Downloads/category.html'


def main():
    db = pymongo.MongoClient(host='127.0.0.1')['zulinbao']
    file = open(FILE, 'r')
    content = file.read()
    content = content.replace('\r', '').replace('\n', '')

    offset = 0

    category = None
    while True:

        next_category_index = content.find('class="bigClass">', offset)
        next_sub_category_index = content.find('cityid=330100">', offset)

        if next_category_index == next_sub_category_index == -1:
            db.category.save(category)
            break
        elif next_category_index == -1 or next_category_index > next_sub_category_index:  # 小类目
            element = find_next(offset, content, 'cityid=330100">', '</a>')
            category['sub'].append({'name': element['content'].replace(' ', '').replace('\r', '').replace('\n', ''), '_id': ObjectId()})
            offset = element['index']
        elif next_category_index < next_sub_category_index:  # 大类目
            if category is not None:
                db.category.save(category)
            element = find_next(offset, content, 'class="bigClass">', '</p>')
            category = {'name': element['content'].replace(' ', '').replace('\r', '').replace('\n', ''), '_id': ObjectId(), 'sub': []}
            offset = element['index']


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
