<div align="center">

# Floya's Phish Hunter

A python script to filter URLs from [PhishStats](https://phishstats.info/), [OpenPhish](https://openphish.com/), [PhishHunt](https://phishunt.io/)

Created for my internship at [Gendigital](https://gendigital.com/)/[Avast](https://www.avast.com/)
</div>

## Usage

```bash
$ python3 all.py
Keyword (leave blank to initiate scan): login
Added: login
Keyword (leave blank to initiate scan):
```

## Features

* Fetch URLs from PhishStats, OpenPhish, PhishHunt
* Filter URLs based on keywords
* 2 minute delay between scans
* Default keywords (./keywords.txt)