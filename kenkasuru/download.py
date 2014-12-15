__author__ = 'bergundy'

import requests
import re

TOKEN_REGEX = re.compile(r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>')


def download(url, hostname, port, username, password):
    base_url = 'http://{}:{}/gui/'.format(hostname, port)
    token_url = '{}token.html'.format(base_url)

    auth = requests.auth.HTTPBasicAuth(username, password)
    r = requests.get(token_url, auth=auth)
    token = TOKEN_REGEX.search(r.text).group(1)
    guid = r.cookies['GUID']
    cookies = dict(GUID=guid)

    params = {'action': 'add-url', 'token': token, 's': url}
    r = requests.get(url=base_url, auth=auth, cookies=cookies, params=params)
    assert r.status_code == 200, 'Failed to download: {}'.format(r.text)
