import re
import sys

import requests

from bs4 import BeautifulSoup

state_getters = {
    'AK': {
        'url': 'http://dhss.alaska.gov/dph/Epi/id/Pages/COVID-19/monitoring.aspx',
        'getter': lambda soup: int(soup.select_one('.grid2 > table > tbody > tr:last-child > td:last-child').text)
    },
    'AL': {
        'url': 'http://alabamapublichealth.gov/infectiousdiseases/2019-coronavirus.html',
        'getter': lambda soup: int(soup.select_one('.mainContent > table > tbody > tr:last-child > td:last-child').text)
    },
    'AR': {
        'url': 'https://www.healthy.arkansas.gov/programs-services/topics/novel-coronavirus',
        'getter': lambda soup: int(soup.select_one('#contentBody > table:nth-of-type(4) tr:first-child > td:last-child').text)
    },
    'CA': {
        'url': 'https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/nCOV2019.aspx',
        'getter': lambda soup: int(re.findall('(?:total of )([\d,]+)', soup.select_one('#WebPartWPQ2 > .ms-rtestate-field .NewsItemContent').text)[0].replace(',', ''))
    },
    'CO': {
        'url': 'https://covid19.colorado.gov/data',
        'getter': lambda soup: int(re.findall('[\d,]+', soup.select_one('article.page .paragraph:first-child .field p:nth-of-type(3)').text)[0])
    },
    'FL': {
        'url': 'https://floridahealthcovid19.gov/',
        'getter': lambda soup: int(soup.select_one('#latest-stats .stat--box:last-child h2').text)
    },
    'GA': {
        'url': 'https://dph.georgia.gov/covid-19-daily-status-report',
        'getter': lambda soup: int(soup.select_one('.body-content > table td:last-child').text.split()[0])
    }
}

print('state,total_cases')
for state, info in state_getters.items():
    try:
        soup = BeautifulSoup(requests.get(info['url']).content, 'html5lib')
        count = info['getter'](soup)
        print(f'{state},{count}')
    except Exception as e:
        print(f'{state},')
        print(f'Failed to get stats for {state}. Error: {e}', file=sys.stderr)
