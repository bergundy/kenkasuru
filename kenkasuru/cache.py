import os

from functools import wraps
from itertools import chain
from tempfile import gettempdir
from hashlib import md5


__author__ = 'bergundy'


class Cache:
    _path = os.path.join(gettempdir(), '__kenkasuru__')
    if not os.path.isdir(_path):
        os.mkdir(_path, mode=0o775)

    default_reader = lambda f: f.read()
    default_writer = lambda data, f: f.write(data)

    @classmethod
    def temp_file(cls, name):
        return os.path.join(cls._path, name)

    @classmethod
    def get(cls, path, reader=default_reader):
        with open(cls.temp_file(path), mode='r', encoding='utf-8') as f:
            return reader(f)

    @classmethod
    def put(cls, path, data, *, writer=default_writer):
        with open(cls.temp_file(path), mode='w', encoding='utf-8') as f:
            writer(data, f)


def make_key(fn, *args, **kwargs):
    chained_args = args + tuple(chain.from_iterable(sorted(kwargs.items())))
    hash_key = md5(str(chained_args).encode()).hexdigest()[:8]
    return '{}:{}:{}.cache'.format(fn.__module__, fn.__name__, hash_key)


def file_cache(reader=Cache.default_reader, writer=Cache.default_writer):
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            path = make_key(fn, *args, **kwargs)
            # noinspection PyBroadException
            try:
                return Cache.get(path, reader=reader)
            except Exception:
                value = fn(*args, **kwargs)
                Cache.put(path, value, writer=writer)
                return value
        return wrapper
    return inner
