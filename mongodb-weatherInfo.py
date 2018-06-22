import requests
import re
from pymongo import MongoClient
import pymongo.errors
from gridfs import GridFS
from functools import wraps
import time


mongo_db = 'jef_db'
mongo_fs = 'weather'
mongodb_payload = {
    'host': '10.5.1.160',
    'port': 32769,
    'user': 'jef',
    'password': 'jeflovespython',
}
mongo_fs_filename = 'filename'
mongo_fs_url = 'url'
mongo_fs_datetime = 'datetime'
mongo_fs_extension = 'extension'
url_base = 'https://www.cwb.gov.tw'
url_images = '/V7/js/HDRadar_TW_3600_n.js'


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        r = f(*args, **kwargs)
        return r, round(time.time() - start_time)
    return wrapper


class MongodbClient:
    def __init__(self, **kwargs):

        self.host = kwargs.get('host', '127.0.0.1')
        self.port = kwargs.get('port', 27017)
        self.user = kwargs.get('user', 'root')
        self.password = kwargs.get('password')

    @property
    def url_mongo(self):
        return self.password and f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/' or f'mongodb://{self.host}:{self.port}/'

    def __enter__(self):
        self.result = MongoClient(self.url_mongo)
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.result.close()


@timer
def get_weather(num=0):
    num = num or -1
    put_counter = 0
    try:
        payload = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        }
        resp = requests.get(url_base + url_images, params=payload)
        if resp.status_code == 200:
            matches = re.finditer(r'"(.*)":"(.*)"', resp.text)
            images = [{
                mongo_fs_url: url_base + x.group(1),
                mongo_fs_datetime: x.group(2),
                mongo_fs_filename: x.group(1).split('/')[-1].split('_')[-1].split('.')[0],
                mongo_fs_extension: x.group(1).split('/')[-1].split('_')[-1].split('.')[-1],
            } for x in matches]

            with MongodbClient(**mongodb_payload) as mc:
                db = mc[mongo_db]
                col = db[f'{mongo_fs}.files']
                fs = GridFS(db, mongo_fs)
                for image in images:
                    if not col.find_one({mongo_fs_filename: image.get(mongo_fs_filename)}, {'_id': 1}):
                        content = requests.get(image.get(mongo_fs_url)).content
                        fs.put(content, **image)
                        put_counter += 1
                        print(f'put {image.get(mongo_fs_filename)} into db.')
        return put_counter

    except requests.exceptions.ConnectionError:
        print('Internet Connection Problem... either you have no internet connection or the URL is illegal.')
        exit(-1)
    except pymongo.errors.ServerSelectionTimeoutError:
        print('Monogo Connection Problem... ')
        exit(-1)


if __name__ == '__main__':
    print(get_weather())
