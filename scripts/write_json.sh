#!/usr/bin/env bash

python ../src/scraper.py --format csv --outdir ../data
python ../src/scraper.py --format md --outdir ../data
python ../src/scraper.py --format json --outdir ../data