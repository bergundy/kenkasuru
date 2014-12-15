from itertools import repeat
from bs4 import BeautifulSoup
from .common import Torrent, dehumanize_size

import requests
import re


def search(show, season, episode, quality='720p'):
    base_url = 'http://kickass.to/usearch/'
    params = [str(p) for p in (show, season, episode, quality)]
    query = '{} s{:02d}e{:02d} {}'.format(show, season, episode, quality)
    url = '{}{}/'.format(base_url, query)

    r = requests.get(url)

    # check if no torrents found
    if not re.findall(r'Download torrent file', str(r.content)):
        return []
    else:
        soup = BeautifulSoup(r.content)

        # to use by age, seeders, and leechers
        # sample:
        # 700.46 MB
        # 5
        # 2 years
        # 1852
        # 130
        al = [s.get_text() for s in soup.find_all('td', {'class': 'center'})]
        url = [a.get('url') for a in soup.find_all('a', {'title': 'Download torrent file'})]
        hsize = [t.get_text() for t in soup.find_all('td', {'class': 'nobr'})]
        size = [dehumanize_size(each) for each in hsize]
        title = [ti.get_text() for ti in soup.find_all('a', {'class': 'cellMainLink'})]
        title_distance = [sum(w.lower() in each.lower() for w in params) for each in title]
        age = al[2::5]
        seeders = [int(each) for each in al[3::5]]
        leechers = [int(each) for each in al[4::5]]

        return [Torrent(*i) for i in zip(url, hsize, size, title, title_distance,
                                         age, seeders, leechers, repeat(None), repeat(None))]
