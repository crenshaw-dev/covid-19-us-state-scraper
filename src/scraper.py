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
        'getter': lambda soup: int(soup.select_one('div.row:nth-child(5) > div:nth-child(1) > p:nth-child(1)').text.split(': ')[1].split()[0])
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
    },
    'MN': {
        'url': 'https://www.health.state.mn.us/diseases/coronavirus/situation.html',
        'getter': lambda soup: int(soup.select_one('#body ul li:first-child').text.split(': ')[1])
    },
    'MO': {
        'url': 'https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/',
        'getter': lambda soup: int(soup.select_one('#main-content table tr:last-child td').text)
    },
    'NC': {
        'url': 'https://www.ncdhhs.gov/covid-19-case-count-nc',
        'getter': lambda soup: int(soup.select_one('table tr:last-child td:first-child').text.strip())
    },
    'NE': {
        'url': 'http://dhhs.ne.gov/Pages/Coronavirus.aspx',
        'getter': lambda soup: int(soup.select_one('#ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField > ul li:first-child').text.split()[-1])
    },
    'NH': {
        'url': 'https://www.nh.gov/covid19/',
        'getter': lambda soup: int(soup.select_one('.summary-list table tr:first-child td:last-child').text)
    },
    'NJ': {
        'url': 'https://www.nj.gov/health/',
        'getter': lambda soup: int(soup.select_one('table tr:first-child td:last-child').text)
    },
    'NM': {
        'url': 'https://cv.nmhealth.org/',
        'getter': lambda soup: int(soup.select_one('h2.et_pb_module_header > span:first-child').text)
    },
    'NY': {
        'url': 'https://coronavirus.health.ny.gov/county-county-breakdown-positive-cases',
        'getter': lambda soup: int(soup.select_one('table tr:last-child td:last-child').text.replace(',', ''))
    },
    'OH': {
        'url': 'https://coronavirus.ohio.gov/wps/portal/gov/covid-19/',
        'getter': lambda soup: int(soup.select_one('div.odh-ads__item:first-child > div:first-child > div:first-child').text)
    },
    'OK': {
        'url': 'https://coronavirus.health.ok.gov/',
        'getter': lambda soup: int(soup.select_one('.pane-3 > div:first-child > table:first-child tr:first-child > td:last-child').text)
    },
    'OR': {
        'url': 'https://govstatus.egov.com/OR-OHA-COVID-19',
        'getter': lambda soup: int(soup.select_one('#collapseCases table td.table-warning').text)
    },
    'PA': {
        'url': 'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx',
        'getter': lambda soup: int(soup.select_one('table tr:last-child td:nth-of-type(2)').text.strip())
    },
    'SD': {
        'url': 'https://doh.sd.gov/news/Coronavirus.aspx',
        'getter': lambda soup: int(soup.select_one('div.tableWrapper:nth-child(12) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)').text.strip())
    },
    'TN': {
        'url': 'https://www.tn.gov/health/cedep/ncov.html',
        'getter': lambda soup: int(soup.select_one('.fifth-color table tr:nth-child(4) > td:nth-child(2)').text)
    },
    'TX': {
        'url': 'https://www.dshs.state.tx.us/news/updates.shtm',
        'getter': lambda soup: int(soup.select_one('table.zebraBorder:nth-child(7) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text)
    },
    'VT': {
        'url': 'https://www.healthvermont.gov/response/infectious-disease/2019-novel-coronavirus',
        'getter': lambda soup: int(soup.select_one('.dynamic-height-wrap table:nth-child(7) td:nth-child(2)').text)
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


def get_state(url, count_getter, verify_cert=False):
    try:
        soup = BeautifulSoup(requests.get(url, verify=verify_cert).content, 'html5lib')
        return count_getter(soup)
    except Exception as e:
        print(f'Failed to get stats for {state}. Error: {e}', file=sys.stderr)
        return ''


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--format', help='Output format (default: csv, options: csv, md)')
    args = parser.parse_args()

    stats_format = args.format or 'csv'
    formatter = formatters[stats_format]
    print(formatter['get_header']())
    for state, info in state_getters.items():
        # Don't verify the cert for Texas, because it throws an error.
        count = get_state(info['url'], info['getter'], verify_cert=(state != 'TX'))
        print(formatter['get_row'](state, count))
