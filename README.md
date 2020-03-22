# COVID-19 US State Scraper

## Project Overview

This is a Python web scraper to get current case counts by US state.

I'm using the [list of state info pages on this page](http://coronavirusapi.com/) to get data sources.

## Current Counts (March 22 2020)

(Many states are not currently supported.)

state | total_cases
--- | ---
AK | 14
AL | 138
AR | 165
CA | 1224
CO | 475
FL | 830
GA | 600
HI | 48
ID | 42
IL | 753
KS | 55
 
 ## Features Needed
 
 ### Dynamic Page Support
 
 Some sites are rendered client-side. I'll need either a more full-featured parser than BeautifulSoup or to
 dig in and find the apps' data sources.
 
 ### Parallel Requests
 
 Running all the requests sequentially is slow. I'd love to parallelize this.
 