import re
import requests

from itertools import chain
from collections import OrderedDict
from datetime import date
from bs4 import BeautifulSoup
from .cache import file_cache

__author__ = 'bergundy'

DOMAIN = 'http://www.pogdesign.co.uk'
BASE_URL = '{}/cat/'.format(DOMAIN)


@file_cache()
def login(username, password):
    r = requests.post(BASE_URL,
                      data=OrderedDict([
                          ('username', username), ('password', password), ('sub_login', 'Account Login')]),
                      allow_redirects=False)
    return r.cookies['CAT_UID']


def list_episodes(cookie):
    today = date.today()
    # TODO: check if logged out

    r = requests.get(BASE_URL, cookies={'CAT_UID': cookie})
    soup = BeautifulSoup(r.content)

    day_els = soup.find_all('td', {'class': 'day'})
    today_els = soup.find_all('td', {'class': 'today'})
    for day_el in chain(day_els, today_els):
        d = date(*reversed(list(map(int, day_el.attrs['id'].split('_')[1:]))))
        if d > today:
            continue
        eps = day_el.find_all('div', {'class': 'ep'})
        for ep in eps:
            a = ep.find_all('a')[-1]
            checkbox = ep.find('input', {'type': 'checkbox'})
            downloaded = bool(checkbox.attrs.get('checked'))
            ep_id = checkbox.attrs['value']
            match = re.search(r'^/cat/([^/]+)/Season-([^/]+)/Episode-([^/]+)$', a.attrs['href'])
            show = match.group(1).replace('-', ' ').lower()
            season, episode = int(match.group(2)), int(match.group(3))
            yield d, ep_id, downloaded, show, season, episode


def mark(ep_id, cookie):
    requests.post(BASE_URL + 'watchhandle', cookies={'CAT_UID': cookie}, data={
        'watched': 'adding',
        'shid': ep_id
    })


def unmark(ep_id, cookie):
    requests.post(BASE_URL + 'watchhandle', cookies={'CAT_UID': cookie}, data={
        'unwatched': 'removing',
        'shid': ep_id
    })
