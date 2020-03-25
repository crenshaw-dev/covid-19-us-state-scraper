# COVID-19 US State Scraper

## Project Overview

This is a Python web scraper to get current case counts by US state.

I'm using the [list of state info pages on this page](http://coronavirusapi.com/) to get data sources.

Output is available as CSV, Markdown, or JSON. Specify `--format` as `csv`, `json`, or `md`.

**Caution**: Be _very_ careful if running this script in a loop. Let's not overload anyone's servers.

## Stats (as of Wednesday, March 25, 2020 1:21:22 PM GMT)

These are the only states I plan to support for now. Others have bot-blockers, client-side rendering, or iframes
loading from arcgis. Any help pulling data from those sources would be greatly appreciated.

state | total_cases | total_tested | deaths
--- | --- | --- | ---
AK | 42 |  | 
AL | 242 | 2321 | 0
AR | 236 |  | 
CA | 2102 |  | 40
CO | 912 | 7701 | 11
FL | 1467 |  | 20
GA | 1097 |  | 38
HI | 90 |  | 1
ID | 1 |  | 0
KS | 98 |  | 
KY | 157 | 3022 | 
MA | 1159 |  | 
ME | 118 | 3132 | 
MI | 1791 |  | 24
MN | 262 | 5812 | 1
MO | 255 |  | 5
NC | 398 | 8502 | 0
NE | 61 | 1365 | 
NH | 108 | 2356 | 1
NJ | 3675 |  | 44
NM | 100 | 6842 | 
NY | 25665 |  | 
OH | 564 |  | 8
OK | 106 | 841 | 3
OR | 209 | 4559 | 
PA | 851 | 9494 | 7
SD | 30 | 820 | 1
TN | 667 |  | 
VT | 95 | 1535 | 7

## Features Needed

### Dynamic Page Support

Some sites are rendered client-side. I'll need either a more full-featured parser than BeautifulSoup or to
dig in and find the apps' data sources.
