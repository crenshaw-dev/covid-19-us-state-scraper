#!/usr/bin/env bash

while true
do
  python ../src/scraper.py --format csv,md,json --outdir ../data --daemon 60
  sleep 1h
done
