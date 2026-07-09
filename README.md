<div align="center">

  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-white.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo-black.png">
    <img alt="Project Logo" src="assets/logo-black.png" width="100">
  </picture>

# Floya's Phish Hunter

A python script to filter latest URLs from [PhishStats](https://phishstats.info/), [OpenPhish](https://openphish.com/), [PhishHunt](https://phishunt.io/)

Created for my internship at [Gendigital](https://gendigital.com/)/[Avast](https://www.avast.com/)

</div>

## Usage

```bash
$ python3 all.py
Keyword (leave blank to initiate scan):
```

<div align="center">

![Usage Example](assets/phish.gif)

</div>

### Options:

`-h` or `--help` = Shows information about each option

```bash
$ python3 all.py -h
usage: all.py [-h] [--api {phishstats,openphish,phishunt,all}] [-oh] [-o] [-r]

options:
  -h, --help            show this help message and exit
  --api {phishstats,openphish,phishunt,all}
                        Select one of the provided APIs, instead of all at once.
  -oh, --only-hits      Show only URLs that match your filter.
  -o, --once            Run the process only once, by default there is a 120 second delay between fetches. (Due to
                        API rate limitation)
  -r, --raw             Raw output, only hit URLs, no formatting. Good for parsing into a file.
```

`--api` Use only selected APIs:

```bash
$ python3 all.py -api phishstats
$ python3 all.py -api openphish
$ python3 all.py -api phishhunt
```

`-oh` or `--only-hits` = Only show hits

```
$ python3 all.py -oh
```

`-o` or `--once` = Run only once

```bash
$ python3 all.py -o
```

`-r` or `--raw` = Raw output

```bash
$ python3 all.py -r
```

## Features

- Fetch URLs from PhishStats, OpenPhish, PhishHunt
- Filter URLs based on keywords
- 2 minute delay between scans
- Default keywords
- Configurable (./config.yaml)

## To-do

- [x] Add an option to run once
- [x] Add GIF showcase to `README.md`
- [ ] Add feature to fetch older posts
- [x] Add an option to not show no hits (only hits)
- [ ] Daily report of top targeted brands or keywords
- [x] Add an option to only fetch selected APIs
- [x] Move configurable values to `config.yaml`
- [x] Rich x raw output options
- [ ] Exportable into csv or json
- [x] Add help

## Contribution

This is rather my personal project, that was formerly part of my internship at Gen. Feel free to fork it and improve it. If you want to directly contribute to this repository, hit me up with ideas.
