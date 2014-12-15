import json
import os
import click

from kenkasuru.index import search
from kenkasuru.sorting import sorted_torrents
from kenkasuru.download import download
from kenkasuru import calendar


__author__ = 'bergundy'


class Config:
    def __init__(self, index, calendar, utorrent):
        self.index = index
        self.calendar = calendar
        self.utorrent = utorrent


@click.group()
@click.pass_context
@click.option('-c', '--config', default='~/.kenkasuru.json')
def cli(ctx, config):
    with open(os.path.expanduser(config)) as f:
        kws = json.load(f)
    ctx.obj = Config(**kws)


def _get(config, show, season, episode):
    torrents = search(config.index, show, season, episode)

    if not torrents:
        return

    torrents = sorted_torrents(torrents)
    for torrent in torrents:
        print('{0: >8.5f}  {1: >10} {2:8} {3} - {4}'.format(
            torrent.score, torrent.hsize, torrent.seeders, torrent.explain, torrent.title))
    download(torrents[0].url, **config.utorrent)


@cli.command()
@click.pass_context
@click.argument('show')
@click.argument('season', type=int)
@click.argument('episode', type=int)
def get(ctx, show, season, episode):
    """Download a single episode"""
    config = ctx.obj
    _get(config, show, season, episode)


@cli.command()
@click.pass_context
def update(ctx):
    """Download all unmarked episodes from calendar"""
    config = ctx.obj
    cookie = calendar.login(**config.calendar)

    for d, ep_id, downloaded, show, season, episode in calendar.list_episodes(cookie):
        print(d, ep_id, downloaded, show, season, episode)
        if not downloaded:
            _get(config, show, season, episode)
            calendar.mark(ep_id, cookie)


if __name__ == '__main__':
    cli()
