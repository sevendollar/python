from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import functools
import time


class Mongo:
    def __init__(self, url, port='27017', user=None, password=None):
        self.URL = url
        self.PORT = port or None
        self.MONGO_USER = user or None
        self.MONGO_PASS = password or None

    def __enter__(self):
        self.mc = MongoClient(f'mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.URL}:{self.PORT}/') if self.MONGO_USER else MongoClient(f'mongodb://{self.URL}:{self.PORT}/')
        return self.mc

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mc.close()
        pass


def timer(f):
    @functools.wraps(f)
    def wraper(*args, **kwargs):
        start = time.time()
        r = f(*args, **kwargs)
        print(f'time spent: {round(time.time() - start)} seconds.')
        return r
    return wraper


@timer
def m(query_string):
    user = 'jef'
    pas = 'jeflovespython'
    ip_mongo = '10.5.1.160'
    port_mongo = '32772'
    url = 'https://en.wikipedia.org/wiki/List_of_capitals_in_the_United_States'

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    payload = [{'state': tr.find_all('td')[0].text or None,
                'abr': tr.find_all('td')[1].text or None,
                'state_hood': tr.find_all('td')[2].text or None,
                'capital': tr.find_all('td')[3].text or None,
                'capital_since': tr.find_all('td')[4].text and int(tr.find_all('td')[4].text) or None,
                'area': tr.find_all('td')[5].text and float(tr.find_all('td')[5].text.replace(',', '.')) or None,
                'municipal': tr.find_all('td')[6].text and tr.find_all('td')[6].text.replace(',', '.') or None,
                'metropolitan': tr.find_all('td')[7].text and tr.find_all('td')[7].text.replace(',', '.') or None,
                'rank_in_state': tr.find_all('td')[8].text and int(tr.find_all('td')[8].text) or None,
                'rank_in_us': tr.find_all('td')[9].text and int(tr.find_all('td')[9].text) or None,
                'notes': tr.find_all('td')[10].text or None,
                } for tr in soup.find('table', {'class': 'wikitable'}).find_all('tr')[2:]]

    with Mongo(ip_mongo, port_mongo, user, pas) as mc:
        db = mc.jef_db
        col = db.us_capitals
        col.delete_many({})
        col.insert_many(payload).inserted_ids
        return [x for x in col.find(query_string)]


if __name__ == '__main__':
    [print(x.get('state')) for x in m({'area': {'$gte': 500}})]
