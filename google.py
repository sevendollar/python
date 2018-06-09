import requests
from bs4 import BeautifulSoup
import random
import webbrowser

base_url = 'https://google.com'
query = f'/search?q={(lambda x: x)(input("search keyword? "))}'
soup = BeautifulSoup(requests.get(base_url + query).text, 'lxml')
links = [ (e.find('a').text, e.find('a').get('href')) for e in soup.find_all('', {'class': 'r'}) ]
open_num = min(10, len(links))
try:
    webbrowser.open(random.choice([ f'{base_url}{links[i][1]}' for i in range(open_num) ]))
except IndexError:
    print('nothing to search for...')
