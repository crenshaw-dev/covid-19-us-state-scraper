# COVID-19 US State Scraper

## Project Overview

This is a Python web scraper to get current case counts by US state.

I'm using the [list of state info pages on this page](http://coronavirusapi.com/) to get data sources.

Output is available as CSV, Markdown, or JSON. Specify `--format` as `csv`, `json`, or `md`.

## Current Counts (March 22 2020)

These are the only 30 states I plan to support for now. Others have bot-blockers, client-side rendering, or iframes
loading from arcgis. Any help pulling data from those sources would be greatly appreciated.

state | total_cases | total_tested | deaths
--- | --- | --- | ---
AK | 22 |  | 
AL | 157 | 1602 | 0
AR | 165 |  | 
CA | 1468 |  | 27
CO | 591 | 5436 | 6
FL | 1007 |  | 13
GA | 620 |  | 25
HI | 56 |  | 0
ID | 2 |  | 0
IL | 1049 | 8374 | 9
KS | 64 |  | 
KY | 99 | 1571 | 
MA | 646 |  | 
ME | 89 | 2353 | 
MI | 249 |  | 3
MN | 169 | 4680 | 1
MO | 90 |  | 3
NC | 255 | 6438 | 0
NE | 42 | 398 | 
NH | 78 | 889 | 
NJ | 1914 |  | 20
NM | 65 | 5386 | 
NY | 15168 |  | 
OH | 351 |  | 3
OK | 67 | 736 | 2
OR | 161 | 3025 | 
PA | 479 | 5443 | 2
SD | 21 | 761 | 1
TN | 505 |  | 
TX | 334 | 8756 | 5
VT | 52 | 1158 | 2
 
## Features Needed

### Dynamic Page Support

Some sites are rendered client-side. I'll need either a more full-featured parser than BeautifulSoup or to
dig in and find the apps' data sources.
