#Program to scrape the flight data website to automatically load the ICAO numbers to streamline the process
import requests
from bs4 import BeautifulSoup
import pandas as pd




def get_icao_numbers(path: str) -> list[str]:
    """
    ICAO scraper
    """
    URL = 'https://samples.adsbexchange.com/traces/2024/06/01/' + path
    try:
        p = requests.get(URL,timeout=None)
    except Exception:
        print("Error")
    soup = BeautifulSoup(p.content, 'html.parser')
    icao_lst = []
    for link in soup.find_all('a'):
        full = link.get('href')
        if len(full) > 0 and full[0] == 't':
            if full[11] == '~':
                icao_num = full[11:18]
            else:
                icao_num = full[11:17]
            icao_lst.append(icao_num)
    return icao_lst


def get_all_files() -> list[str]:
    """
    Retrives all the trace file names
    """
    URL = 'https://samples.adsbexchange.com/traces/2024/06/01/'
    p = requests.get(URL, timeout=None)
    soup = BeautifulSoup(p.content, 'html.parser')
    icao_files = []
    for link in soup.find_all('a'):
        full = link.get('href')
        if len(full) == 3:
            icao_files.append(full)
    return icao_files[1:]









