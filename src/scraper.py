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
    },
    'HI': {
        'url': 'https://health.hawaii.gov/docd/advisories/novel-coronavirus-2019/',
        'getter': lambda soup: int(soup.select_one('.primary-content table tr:nth-of-type(2) td:last-child').text.split()[0])
    },
    'ID': {
        'url': 'https://coronavirus.idaho.gov/',
        'getter': lambda soup: int(soup.select_one('#tablepress-1 .row-10 .column-3').text)
    },
    'IL': {
        'url': 'http://www.dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list/coronavirus',
        'getter': lambda soup: int(soup.select_one('dl dd .NumberHighlight h3').text)
    },
    'KS': {
        'url': 'https://govstatus.egov.com/coronavirus',
        'getter': lambda soup: int(soup.select_one('.container > div:nth-of-type(3) .alert').text.split(': ')[1].split()[0])
    },
    'KY': {
        'url': 'https://govstatus.egov.com/kycovid19',
        'getter': lambda soup: int(re.findall('(?:Positive: )([\d,]+)', soup.select_one('.container > div:nth-of-type(2) .alert').text)[0].replace(',', ''))
    },
    'MA': {
        'url': 'https://www.mass.gov/info-details/covid-19-cases-quarantine-and-monitoring',
        'getter': lambda soup: int(soup.select_one('.page-content table td').text)
    },
    'ME': {
        'url': 'https://www.maine.gov/dhhs/mecdc/infectious-disease/epi/airborne/coronavirus.shtml',
        'getter': lambda soup: int(soup.select_one('table.travelAdvisories tbody tr:last-child td:last-child').text.replace(',', ''))
    },
    'MI': {
        'url': 'https://www.michigan.gov/coronavirus',
        'getter': lambda soup: int(soup.select_one('#comp_114411 table tbody tr:last-child td:nth-of-type(2)').text)
    }
}

formatters = {
    'csv': {
        'get_header': lambda: 'state,total_cases',
        'get_row': lambda state, cases: f'{state},{cases}'
    },
    'md': {
        'get_header': lambda:'state | total_cases\n--- | ---',
        'get_row': lambda state, cases: f'{state} | {cases}'
    }
}


def get_state(url, count_getter):
    try:
        soup = BeautifulSoup(requests.get(url).content, 'html5lib')
        return count_getter(soup)
    except Exception as e:
        print(f'Failed to get stats for {state}. Error: {e}', file=sys.stderr)
        return ''


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--format', help='Output format (default: csv, options: csv)')
    args = parser.parse_args()

    stats_format = args.format or 'csv'
    formatter = formatters[stats_format]
    print(formatter['get_header']())
    for state, info in state_getters.items():
        count = get_state(info['url'], info['getter'])
        print(formatter['get_row'](state, count))
