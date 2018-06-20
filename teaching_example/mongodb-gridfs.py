import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from pprint import pprint
import os


class Mongo:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host') or '127.0.0.1'
        self.port = kwargs.get('port') or 27017
        self.user = kwargs.get('user') or 'root'
        self.password = kwargs.get('password') or None

    @property
    def mongo_url(self):
        return self.password and f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/' or f'mongodb://{self.host}:{self.port}/'

    def __enter__(self):
        self.result = MongoClient(self.mongo_url)
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.result.close()


if __name__ == '__main__':
    MONGODB_PAYLOAD = {
        'host': '10.5.1.160',
        'port': 32768,
        'user': 'jef',
        'password': 'jeflovespython',
    }
    filename = ''
    gridfs_col = 'jef_fs'

    # write block
    def write_file(name):
        with open(name, 'rb') as f:
            s = f.read()
            fs.put(s, filename=name)


    # read block
    def read_file(name):
        with open(name, 'wb') as pdf:
            s = fs.get_last_version(name).read()
            pdf.write(s)

    try:
        with Mongo(**MONGODB_PAYLOAD) as m:
            db = m['jef_db']
            col = db['weather']
            fs = GridFS(db, gridfs_col)

            write_file(filename)
        print('done!')
    except FileNotFoundError:
        print('file not found!')
