from math import sqrt, ceil
from operator import attrgetter, itemgetter
from kenkasuru.index.common import Torrent

__author__ = 'bergundy'


normalize = lambda v: sqrt(sum(each ** 2 for each in v))
identity = lambda x: x
average = lambda v, key=identity: sum(key(each) for each in v) / len(v)
percentile = lambda v, p, key=identity: sorted(key(each) for each in v)[min(ceil(len(v) * p), len(v) - 1)]
median = lambda v, key=identity: percentile(v, 0.5, key)
intermediate = lambda torrent, vectors: \
    [mapper(getattr(torrent, field), info) * multiplier for field, multiplier, info, mapper in vectors]


def torrent_score(*args):
    return sum(intermediate(*args))


torrent_explain = lambda torrent, vectors: dict(zip(map(itemgetter(0), vectors), intermediate(torrent, vectors)))


title_distance_score = lambda x, i: x ** 3 / i['max'] ** 3
size_score = lambda x, i: 1 - abs(x - i['p70']) / max(i['max'] - i['p70'], i['p70'] - i['min'])
seeders_score = lambda x, i: (x - i['min']) / (i['max'] - i['min'])


def sorted_torrents(torrents):
    vectors = [
        ('title_distance', 3, title_distance_score),
        ('size', 2, size_score),
        ('seeders', 5, seeders_score),
    ]
    fields, multipliers, mappers = list(zip(*vectors))
    info = [dict(
        average=average(torrents, attrgetter(field)),
        median=median(torrents, attrgetter(field)),
        p70=percentile(torrents, 0.7, attrgetter(field)),
        min=min(getattr(t, field) for t in torrents),
        max=max(getattr(t, field) for t in torrents)
    ) for field in fields]
    vectors = list(zip(fields, multipliers, info, mappers))

    torrents = (Torrent(*(each[:-2] + (torrent_score(each, vectors),
                                       torrent_explain(each, vectors))))
                for each in torrents)

    return sorted(torrents, key=attrgetter('score'), reverse=True)
