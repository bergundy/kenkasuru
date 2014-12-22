kenkasuru
=========

*kenkasuru* is a cli tool for downloading TV show torrents.

It attempts to select the right torrent for you by searching your preferred index (currently oldpiratebay.org and kickass.to implemented) and ranking the search results.

It also automatically downloads new episodes for shows you follow in http://www.pogdesign.co.uk/cat/.

Currently uses uTorrent for downloads.

## Installation
```
git clone https://github.com/bergundy/kenkasuru.git
cd kenkasuru
virtualenv .pyenv # must be virtualenv for python 3
source .pyenv/bin/activate
pip install -r requirements.txt
```

## Running
In an activated virtualenv, run:
```
python cli.py --help
```

## Configuration
Copy the sample config file into ~/.kenkasuru.json, fill in your details.
calendar is required in order to run "update".
```
{
    "index": "oldpiratebay|kickass",
    "calendar": {
        "username": "<my email at http://www.pogdesign.co.uk/cat/>",
        "password": "<my password at http://www.pogdesign.co.uk/cat/>"
    },
    "utorrent": {
        "username": "<my utorrent remote>",
        "password": "<my utorrent password>",
        "hostname": "x.x.x.x",
        "port": 8080
    }
}
```

## Setup uTorrent
http://lifehacker.com/260393/remote-control-your-torrents-with-utorrents-webui
