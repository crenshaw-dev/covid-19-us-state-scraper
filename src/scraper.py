import os
import re
import sys
import time

import requests

from bs4 import BeautifulSoup
from multiprocessing import Pool

state_getters = {
    'AK': {
        'url': 'http://dhss.alaska.gov/dph/Epi/id/Pages/COVID-19/monitoring.aspx',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.grid2 > table > tbody > tr:last-child > td:last-child').text)
        }
    },
    'AL': {
        'url': 'http://alabamapublichealth.gov/infectiousdiseases/2019-coronavirus.html',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.mainContent > table > tbody > tr:last-child > td:last-child').text),
            'total_tested': lambda soup: int(re.findall('[\d,]+', soup.select_one('div.row:nth-child(3) > p:nth-child(13)').text.split()[2].replace(',', ''))[0]),
            'deaths': lambda soup: int(re.findall('[\d,]+', soup.select_one('div.row:nth-child(3) > p:nth-child(13)').text.split()[3].replace(',', ''))[0])
        }
    },
    'AR': {
        'url': 'https://www.healthy.arkansas.gov/programs-services/topics/novel-coronavirus',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('#contentBody > table:nth-child(9) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)').text),
        }
    },
    'CA': {
        'url': 'https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/nCOV2019.aspx',
        'stats': {
            'total_cases': lambda soup: int(re.findall('(?:total of )([\d,]+)', soup.select_one('#WebPartWPQ2 > .ms-rtestate-field .NewsItemContent').text)[0].replace(',', '')),
            'deaths': lambda soup: int(re.findall('(?:cases and )([\d,]+)', soup.select_one('#WebPartWPQ2 > .ms-rtestate-field .NewsItemContent').text)[0].replace(',', ''))
        }
    },
    'CO': {
        'url': 'https://covid19.colorado.gov/data',
        'stats': {
            'total_cases': lambda soup: int(re.findall('[\d,]+', soup.select_one('article.page .paragraph:first-child .field p:nth-of-type(3)').text)[0]),
            'total_tested': lambda soup: int(soup.select_one('article.page .paragraph:first-child .field p:nth-of-type(3)').text.split('\n')[3].split()[0].replace(',', '')),
            'deaths': lambda soup: int(soup.select_one('article.page .paragraph:first-child .field p:nth-of-type(3)').text.split('\n')[4].split()[0].replace(',', ''))
        }
    },
    'FL': {
        'url': 'https://floridahealthcovid19.gov/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('#latest-stats .stat--box:last-child h2').text),
            'deaths': lambda soup: int(soup.select_one('tbody.row-hover:nth-child(1) > tr:nth-child(2) > td:nth-child(2)').text)
        }
    },
    'GA': {
        'url': 'https://dph.georgia.gov/covid-19-daily-status-report',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.body-content > table td:last-child').text.split()[0]),
            # Commercial plus state labs.
            'total_tests': lambda soup: int(soup.select_one('table.stacked-row-plus:nth-child(13) > tbody:nth-child(3) > tr:nth-child(1) > td:nth-child(3)').text.split()[0]) + int(soup.select_one('table.stacked-row-plus:nth-child(13) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(3)').text.split()[0]),
            'deaths': lambda soup: int(soup.select_one('.body-content > table tr:last-child td:last-child').text.split()[0])
        }
    },
    'HI': {
        'url': 'https://health.hawaii.gov/docd/advisories/novel-coronavirus-2019/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.primary-content table tr:nth-of-type(2) td:last-child').text.split()[0]),
            'deaths': lambda soup: int(soup.select_one('.alignleft > tbody:nth-child(1) > tr:nth-child(10) > td:nth-child(2)').text.split()[0])
        }
    },
    'ID': {
        'url': 'https://coronavirus.idaho.gov/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('#tablepress-1 .row-10 .column-3').text),
            # State plus commercial tests.
            'total_tests': lambda soup: int(soup.select_one('#tablepress-2 > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text) + int(soup.select_one('#tablepress-2 > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)').text),
            'deaths': lambda soup: int(soup.select_one('#tablepress-1 .row-10 .column-4').text),
        }
    },
    'IL': {
        'url': 'http://www.dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list/coronavirus',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('dl dd .NumberHighlight h3').text),
            'deaths': lambda soup: int(soup.select_one('.ckeditor-tabber > dd:nth-child(2) > div:nth-child(3) > div:nth-child(3) > h3:nth-child(2)').text),
            'total_tested': lambda soup: int(soup.select_one('.ckeditor-tabber > dd:nth-child(2) > div:nth-child(3) > div:nth-child(4) > h3:nth-child(2)').text),
        }
    },
    'KS': {
        'url': 'https://govstatus.egov.com/coronavirus',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('div.row:nth-child(5) > div:nth-child(1) > p:nth-child(1)').text.split(': ')[1].split()[0])
        }
    },
    'KY': {
        'url': 'https://govstatus.egov.com/kycovid19',
        'stats': {
            'total_cases': lambda soup: int(re.findall('(?:Positive: )([\d,]+)', soup.select_one('.container > div:nth-of-type(2) .alert').text)[0].replace(',', '')),
            'total_tested': lambda soup: int(re.findall('(?:Number Tested: )([\d,]+)', soup.select_one('.container > div:nth-of-type(2) .alert').text)[0].replace(',', '')),
        }
    },
    'MA': {
        'url': 'https://www.mass.gov/info-details/covid-19-cases-quarantine-and-monitoring',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.page-content table td').text)
        }
    },
    'ME': {
        'url': 'https://www.maine.gov/dhhs/mecdc/infectious-disease/epi/airborne/coronavirus.shtml',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('table.travelAdvisories tbody tr:last-child td:first-child').text.replace(',', '')),
            'total_tested': lambda soup: int(soup.select_one('table.travelAdvisories tbody tr:last-child td:first-child').text.replace(',', '')) + int(soup.select_one('table.travelAdvisories tbody tr:last-child td:last-child').text.replace(',', '')),
        }
    },
    'MI': {
        'url': 'https://www.michigan.gov/coronavirus',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('#comp_114411 table tbody tr:last-child td:nth-of-type(2)').text),
            'deaths': lambda soup: int(soup.select_one('#comp_114411 table tbody tr:last-child td:nth-of-type(3)').text),
        }
    },
    'MN': {
        'url': 'https://www.health.state.mn.us/diseases/coronavirus/situation.html',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('#body ul li:first-child').text.split(': ')[1]),
            'total_tested': lambda soup: int(soup.select_one('#body ul li:nth-of-type(3)').text.split(': ')[1]),
            'deaths': lambda soup: int(soup.select_one('#body ul li:nth-of-type(2)').text.split(': ')[1]),
        }
    },
    'MO': {
        'url': 'https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('#main-content table tr:last-child td').text),
            'deaths': lambda soup: int(soup.select_one('#main-content table tr:first-child td').text.split()[0]),
        }
    },
    'NC': {
        'url': 'https://www.ncdhhs.gov/covid-19-case-count-nc',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('table tr:last-child td:first-child').text.strip().replace(',', '')),
            'total_tested': lambda soup: int(soup.select_one('table tr:last-child td:nth-of-type(3)').text.strip().replace(',', '')),
            'deaths': lambda soup: int(soup.select_one('table tr:last-child td:nth-of-type(2)').text.strip().replace(',', '')),
        }
    },
    'NE': {
        'url': 'http://dhhs.ne.gov/Pages/Coronavirus.aspx',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('#ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField > ul li:first-child').text.split()[-1]),
            # Confirmed plus negative.
            'total_tested': lambda soup: int(soup.select_one('#ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField > ul li:first-child').text.split()[-1]) + int(soup.select_one('#ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField > ul:nth-of-type(2) li').text.split()[-1]),
        }
    },
    'NH': {
        'url': 'https://www.nh.gov/covid19/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.summary-list table tr:first-child td:last-child').text.replace(',', '')),
            'total_tested': lambda soup: int(soup.select_one('.summary-list table tr:nth-of-type(2) td:last-child').text.replace(',', '')),
        }
    },
    'NJ': {
        'url': 'https://www.nj.gov/health/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('table tr:first-child td:last-child').text),
            'deaths': lambda soup: int(soup.select_one('table tr:nth-of-type(2) td:last-child').text),
        }
    },
    'NM': {
        'url': 'https://cv.nmhealth.org/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('h2.et_pb_module_header > span:first-child').text.replace(',', '')),
            'total_tested': lambda soup: int(soup.select_one('.et_pb_text_2 > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text.replace(',', '')),
        }
    },
    'NY': {
        'url': 'https://coronavirus.health.ny.gov/county-county-breakdown-positive-cases',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('table tr:last-child td:last-child').text.replace(',', ''))
        }
    },
    'OH': {
        'url': 'https://coronavirus.ohio.gov/wps/portal/gov/covid-19/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('div.odh-ads__item:first-child > div:first-child > div:first-child').text),
            'deaths': lambda soup: int(soup.select_one('div.odh-ads__item:nth-child(4) > div:nth-child(1) > div:nth-child(1)').text),
        }
    },
    'OK': {
        'url': 'https://coronavirus.health.ok.gov/',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.pane-3 > div:first-child > table:first-child tr:first-child > td:last-child').text),
            # Positive plus negative.
            'total_tested': lambda soup: int(soup.select_one('.pane-3 > div:first-child > table:first-child tr:first-child > td:last-child').text) + int(soup.select_one('.pane-3 > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)').text),
            'deaths': lambda soup: int(soup.select_one('.pane-3 > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(2)').text),
        }
    },
    'OR': {
        'url': 'https://govstatus.egov.com/OR-OHA-COVID-19',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('#collapseCases table td.table-warning').text.replace(',', '')),
            'total_tested': lambda soup: int(soup.select_one('#collapseCases table tr:last-child td:last-child').text.replace(',', '')),
        }
    },
    'PA': {
        'url': 'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('table tr:last-child td:nth-of-type(2)').text.strip())
        }
    },
    'SD': {
        'url': 'https://doh.sd.gov/news/Coronavirus.aspx',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('div.tableWrapper:nth-child(12) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)').text.strip())
        }
    },
    'TN': {
        'url': 'https://www.tn.gov/health/cedep/ncov.html',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.fifth-color table tr:nth-child(4) > td:nth-child(2)').text)
        }
    },
    'TX': {
        'url': 'https://www.dshs.state.tx.us/news/updates.shtm',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('table.zebraBorder:nth-child(7) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text)
        }
    },
    'VT': {
        'url': 'https://www.healthvermont.gov/response/infectious-disease/2019-novel-coronavirus',
        'stats': {
            'total_cases': lambda soup: int(soup.select_one('.dynamic-height-wrap > div:nth-child(1) > table:nth-child(8) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text),
            'total_tested': lambda soup: int(soup.select_one('.dynamic-height-wrap > div:nth-child(1) > table:nth-child(8) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)').text),
            'deaths': lambda soup: int(soup.select_one('.dynamic-height-wrap > div:nth-child(1) > table:nth-child(8) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text),
        }
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
        return json.dumps({stats['state']: stats for stats in stats_list}, sort_keys=True, indent=4, separators=(',', ': '))


def get_state(url, count_getters, verify_cert=False):
    stats = {}

    for stat_name, stat_getter in count_getters.items():
        try:
            soup = BeautifulSoup(requests.get(url, verify=verify_cert).content, 'html5lib')
            stats[stat_name] = stat_getter(soup)
        except Exception as e:
            print(f'Failed to get stats for {url}. Error: {e}', file=sys.stderr)
            stats[stat_name] = ''

    return stats


def get_state_from_info(state):
    # Don't verify the cert for Texas, because it throws an error.
    stats = get_state(state_getters[state]['url'], state_getters[state]['stats'], verify_cert=(state != 'TX'))
    stats['state'] = state
    return stats


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--format', help='Output format (default: csv, options: csv, md, json).')
    parser.add_argument('--outdir', help='Directory to write file. Filename is seconds since epoch.')
    args = parser.parse_args()

    stats_format = args.format or 'csv'
    stats_outdir = args.outdir or None

    if stats_format == 'md':
        formatter = MarkdownFormatter
    elif stats_format == 'json':
        formatter = JsonFormatter
    else:
        formatter = CsvFormatter

    with Pool(len(state_getters)) as pool:
        stats = pool.map(get_state_from_info, state_getters.keys())

    if stats_outdir:
        with open(os.path.join(stats_outdir, f'{int(time.time())}.{stats_format}'), 'w') as text_file:
            print(formatter.format(stats), file=text_file)
    else:
        print(formatter.format(stats))
