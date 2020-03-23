#!/usr/bin/env bash

while true
do
  python ../src/scraper.py --format csv --outdir ../data
  python ../src/scraper.py --format md --outdir ../data
  python ../src/scraper.py --format json --outdir ../data
  sleep 1h
done
