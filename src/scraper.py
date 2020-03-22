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
    }
}

print('state,total_cases')
for state, info in state_getters.items():
    soup = BeautifulSoup(requests.get(info['url']).content, 'html5lib')
    count = info['getter'](soup)
    print(f'{state},{count}')
