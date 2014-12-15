import requests

from bs4 import BeautifulSoup
from .common import Torrent, dehumanize_size


def search(show, season, episode, quality):
    url = 'http://oldpiratebay.org/search.php'
    query = '{} s{:02d}e{:02d} {}'.format(show, season, episode, quality)
    words = {w.lower() for w in query.split()}

    r = requests.get(url, params={'q': query})

    soup = BeautifulSoup(r.content)

    torrent_els = soup.select('table.table-torrents tbody tr')
    for el in torrent_els:
        title = el.find('span').get_text()
        hsize = el.find('td', {'class': 'size-row'}).get_text()
        yield Torrent(
            title=title,
            url=el.find('a', {'title': 'MAGNET LINK'}).get('href'),
            hsize=hsize,
            size=dehumanize_size(hsize),
            seeders=int(el.find('td', {'class': 'seeders-row'}).get_text()),
            leechers=int(el.find('td', {'class': 'leechers-row'}).get_text()),
            age=el.find('td', {'class': 'date-row'}).get_text(),
            title_distance=sum(w in words for w in title.lower().split()),
            score=None,
            explain=None
        )
