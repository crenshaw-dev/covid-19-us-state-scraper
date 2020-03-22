import re
import sys

import requests

from bs4 import BeautifulSoup
from multiprocessing import Pool

state_getters = {
    'AK': {
        'url': 'http://dhss.alaska.gov/dph/Epi/id/Pages/COVID-19/monitoring.aspx',
        'total_cases': lambda soup: int(soup.select_one('.grid2 > table > tbody > tr:last-child > td:last-child').text)
    },
    'AL': {
        'url': 'http://alabamapublichealth.gov/infectiousdiseases/2019-coronavirus.html',
        'total_cases': lambda soup: int(soup.select_one('.mainContent > table > tbody > tr:last-child > td:last-child').text)
    },
    'AR': {
        'url': 'https://www.healthy.arkansas.gov/programs-services/topics/novel-coronavirus',
        'total_cases': lambda soup: int(soup.select_one('#contentBody > table:nth-of-type(4) tr:first-child > td:last-child').text)
    },
    'CA': {
        'url': 'https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/nCOV2019.aspx',
        'total_cases': lambda soup: int(re.findall('(?:total of )([\d,]+)', soup.select_one('#WebPartWPQ2 > .ms-rtestate-field .NewsItemContent').text)[0].replace(',', ''))
    },
    'CO': {
        'url': 'https://covid19.colorado.gov/data',
        'total_cases': lambda soup: int(re.findall('[\d,]+', soup.select_one('article.page .paragraph:first-child .field p:nth-of-type(3)').text)[0])
    },
    'FL': {
        'url': 'https://floridahealthcovid19.gov/',
        'total_cases': lambda soup: int(soup.select_one('#latest-stats .stat--box:last-child h2').text)
    },
    'GA': {
        'url': 'https://dph.georgia.gov/covid-19-daily-status-report',
        'total_cases': lambda soup: int(soup.select_one('.body-content > table td:last-child').text.split()[0])
    },
    'HI': {
        'url': 'https://health.hawaii.gov/docd/advisories/novel-coronavirus-2019/',
        'total_cases': lambda soup: int(soup.select_one('.primary-content table tr:nth-of-type(2) td:last-child').text.split()[0])
    },
    'ID': {
        'url': 'https://coronavirus.idaho.gov/',
        'total_cases': lambda soup: int(soup.select_one('#tablepress-1 .row-10 .column-3').text)
    },
    'IL': {
        'url': 'http://www.dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list/coronavirus',
        'total_cases': lambda soup: int(soup.select_one('dl dd .NumberHighlight h3').text)
    },
    'KS': {
        'url': 'https://govstatus.egov.com/coronavirus',
        'total_cases': lambda soup: int(soup.select_one('div.row:nth-child(5) > div:nth-child(1) > p:nth-child(1)').text.split(': ')[1].split()[0])
    },
    'KY': {
        'url': 'https://govstatus.egov.com/kycovid19',
        'total_cases': lambda soup: int(re.findall('(?:Positive: )([\d,]+)', soup.select_one('.container > div:nth-of-type(2) .alert').text)[0].replace(',', ''))
    },
    'MA': {
        'url': 'https://www.mass.gov/info-details/covid-19-cases-quarantine-and-monitoring',
        'total_cases': lambda soup: int(soup.select_one('.page-content table td').text)
    },
    'ME': {
        'url': 'https://www.maine.gov/dhhs/mecdc/infectious-disease/epi/airborne/coronavirus.shtml',
        'total_cases': lambda soup: int(soup.select_one('table.travelAdvisories tbody tr:last-child td:last-child').text.replace(',', ''))
    },
    'MI': {
        'url': 'https://www.michigan.gov/coronavirus',
        'total_cases': lambda soup: int(soup.select_one('#comp_114411 table tbody tr:last-child td:nth-of-type(2)').text)
    },
    'MN': {
        'url': 'https://www.health.state.mn.us/diseases/coronavirus/situation.html',
        'total_cases': lambda soup: int(soup.select_one('#body ul li:first-child').text.split(': ')[1])
    },
    'MO': {
        'url': 'https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/',
        'total_cases': lambda soup: int(soup.select_one('#main-content table tr:last-child td').text)
    },
    'NC': {
        'url': 'https://www.ncdhhs.gov/covid-19-case-count-nc',
        'total_cases': lambda soup: int(soup.select_one('table tr:last-child td:first-child').text.strip())
    },
    'NE': {
        'url': 'http://dhhs.ne.gov/Pages/Coronavirus.aspx',
        'total_cases': lambda soup: int(soup.select_one('#ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField > ul li:first-child').text.split()[-1])
    },
    'NH': {
        'url': 'https://www.nh.gov/covid19/',
        'total_cases': lambda soup: int(soup.select_one('.summary-list table tr:first-child td:last-child').text)
    },
    'NJ': {
        'url': 'https://www.nj.gov/health/',
        'total_cases': lambda soup: int(soup.select_one('table tr:first-child td:last-child').text)
    },
    'NM': {
        'url': 'https://cv.nmhealth.org/',
        'total_cases': lambda soup: int(soup.select_one('h2.et_pb_module_header > span:first-child').text)
    },
    'NY': {
        'url': 'https://coronavirus.health.ny.gov/county-county-breakdown-positive-cases',
        'total_cases': lambda soup: int(soup.select_one('table tr:last-child td:last-child').text.replace(',', ''))
    },
    'OH': {
        'url': 'https://coronavirus.ohio.gov/wps/portal/gov/covid-19/',
        'total_cases': lambda soup: int(soup.select_one('div.odh-ads__item:first-child > div:first-child > div:first-child').text)
    },
    'OK': {
        'url': 'https://coronavirus.health.ok.gov/',
        'total_cases': lambda soup: int(soup.select_one('.pane-3 > div:first-child > table:first-child tr:first-child > td:last-child').text)
    },
    'OR': {
        'url': 'https://govstatus.egov.com/OR-OHA-COVID-19',
        'total_cases': lambda soup: int(soup.select_one('#collapseCases table td.table-warning').text)
    },
    'PA': {
        'url': 'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx',
        'total_cases': lambda soup: int(soup.select_one('table tr:last-child td:nth-of-type(2)').text.strip())
    },
    'SD': {
        'url': 'https://doh.sd.gov/news/Coronavirus.aspx',
        'total_cases': lambda soup: int(soup.select_one('div.tableWrapper:nth-child(12) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)').text.strip())
    },
    'TN': {
        'url': 'https://www.tn.gov/health/cedep/ncov.html',
        'total_cases': lambda soup: int(soup.select_one('.fifth-color table tr:nth-child(4) > td:nth-child(2)').text)
    },
    'TX': {
        'url': 'https://www.dshs.state.tx.us/news/updates.shtm',
        'total_cases': lambda soup: int(soup.select_one('table.zebraBorder:nth-child(7) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text)
    },
    'VT': {
        'url': 'https://www.healthvermont.gov/response/infectious-disease/2019-novel-coronavirus',
        'total_cases': lambda soup: int(soup.select_one('.dynamic-height-wrap table:nth-child(7) td:nth-child(2)').text)
    }
}


class CsvFormatter:
    @staticmethod
    def format(stats_list: list) -> str:
        csv = 'state,total_cases\n'
        for stats in stats_list:
            csv += f'{stats["state"]},{stats["total_cases"]}\n'
        return csv


class MarkdownFormatter:
    @staticmethod
    def format(stats_list: list) -> str:
        md = 'state | total_cases\n--- | ---\n'
        for stats in stats_list:
            md += f'{stats["state"]} | {stats["total_cases"]}\n'
        return md


class JsonFormatter:
    @staticmethod
    def format(stats_list: list) -> str:
        import json
        # TODO: remove 'state' from object.
        return json.dumps({stats['state']: stats for stats in stats_list})


def get_state(url, count_getter, verify_cert=False):
    try:
        soup = BeautifulSoup(requests.get(url, verify=verify_cert).content, 'html5lib')
        return count_getter(soup)
    except Exception as e:
        print(f'Failed to get stats for {url}. Error: {e}', file=sys.stderr)
        return ''


def get_state_from_info(state):
    # Don't verify the cert for Texas, because it throws an error.
    count = get_state(state_getters[state]['url'], state_getters[state]['total_cases'], verify_cert=(state != 'TX'))
    return {'state': state, 'total_cases': count}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--format', help='Output format (default: csv, options: csv, md, json)')
    args = parser.parse_args()

    stats_format = args.format or 'csv'
    if stats_format == 'md':
        formatter = MarkdownFormatter
    elif stats_format == 'json':
        formatter = JsonFormatter
    else:
        formatter = CsvFormatter

    with Pool(len(state_getters)) as pool:
        stats = pool.map(get_state_from_info, state_getters.keys())

    print(formatter.format(stats))
