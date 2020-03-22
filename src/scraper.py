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
