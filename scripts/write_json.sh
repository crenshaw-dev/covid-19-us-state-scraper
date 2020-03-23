#!/usr/bin/env bash

while true
do
  python ../src/scraper.py --format csv,md,json --outdir ../data
  sleep 1h
done
