from collections import namedtuple

Torrent = namedtuple('Torrent', 'url hsize size title title_distance age seeders leechers score explain')


def dehumanize_size(size):
    value, modifier = size.split()
    multiplier = 1 + ['bytes', 'KB', 'MB', 'GB', 'TB'].index(modifier)
    return float(value) * 1024 ** multiplier
