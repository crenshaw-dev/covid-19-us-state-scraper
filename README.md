# COVID-19 US State Scraper

## Project Overview

This is a Python web scraper to get current case counts by US state.

I'm using the [list of state info pages on this page](http://coronavirusapi.com/) to get data sources.

Output is available as CSV, Markdown, or JSON. Specify `--format` as `csv`, `json`, or `md`.

**Caution**: Be _very_ careful if running this script in a loop. Let's not overload anyone's servers.

## Stats (as of Tuesday, March 24, 2020 12:26:05 PM GMT)

These are the only 30 states I plan to support for now. Others have bot-blockers, client-side rendering, or iframes
loading from arcgis. Any help pulling data from those sources would be greatly appreciated.

state | total_cases | total_tested | deaths
--- | --- | --- | ---
AK | 36 |  | 
AL | 196 | 1832 | 0
AR | 201 |  | 
CA | 1733 |  | 27
CO | 720 | 6224 | 7
FL | 1227 |  | 17
GA | 800 |  | 26
HI | 77 |  | 4
ID | 2 |  | 0
IL | 1285 | 9868 | 12
KS | 82 |  | 
KY | 124 | 1866 | 
MA | 777 |  | 
ME | 107 | 2898 | 
MI | 293 |  | 7
MN | 235 |  | 1
MO | 183 |  | 3
NC | 297 | 8438 | 0
NE | 52 | 1027 | 
NH | 101 | 869 | 1
NJ | 2844 |  | 27
NM | 83 | 5973 | 
NY | 20875 |  | 
OH | 442 |  | 6
OK | 81 | 775 | 2
OR | 191 | 3840 | 
PA | 644 | 7239 | 6
SD | 28 | 790 | 1
TN | 615 |  | 
TX | 352 | 10055 | 8
VT | 75 | 1173 | 5

## Features Needed

### Dynamic Page Support

Some sites are rendered client-side. I'll need either a more full-featured parser than BeautifulSoup or to
dig in and find the apps' data sources.
