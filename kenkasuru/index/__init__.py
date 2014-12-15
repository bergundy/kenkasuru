import importlib
import json

from ..cache import file_cache
from .common import Torrent


@file_cache(
    reader=lambda f: [Torrent(*t) for t in json.load(f)],
    writer=json.dump)
def search(index, show, season, episode, quality='720p'):
    index = importlib.import_module('kenkasuru.index.{}'.format(index))
    torrents = index.search(show, season, episode, quality)
    return list(torrents)
