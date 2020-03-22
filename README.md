# COVID-19 US State Scraper

## Project Overview

This is a Python web scraper to get current case counts by US state.

I'm using the [list of state info pages on this page](http://coronavirusapi.com/) to get data sources.

## Current States Supported

 * Alaska
 * Alabama
 * Arkansas
 * California
 * Colorado
 * Florida
 * Georgia
 * Hawaii
 * Idaho
 * Illinois
 
 ## Features Needed
 
 ### Dynamic Page Support
 
 Some sites are rendered client-side. I'll need either a more full-featured parser than BeautifulSoup or to
 dig in and find the apps' data sources.
 
 ### Parallel Requests
 
 Running all the requests sequentially is slow. I'd love to parallelize this.
 