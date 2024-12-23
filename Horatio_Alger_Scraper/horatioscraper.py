#Program to scrape the awards website for book proj.
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional






def retrieve_info(path: str) -> tuple[str, str]:
    """
    Goes into each members profile to scrape name, occupation/employer
    """

    link = 'https://horatioalger.org' + path
    p = requests.get(link)
    soup = BeautifulSoup(p.content, 'html.parser')
    main = soup.find("div", class_="split-header__wrap")
    if main is None:
        return ('No person', 'No person')
    name = main.find("h1", class_='person-header__title')
    occupation = main.find("div", class_='person-header__info')

    return (name, occupation)


def format(occupation: str) -> str:
    """
    Makes the string more readable and in a better format
    """
    f = occupation.text.replace('\t', ' ').strip()
    rv = f.splitlines()
    return rv

#Data will be stored in a list of dictionaries, I guess pandas handles this well?
data = []


#Scraping the website, there are lots of pages
URL = 'https://horatioalger.org/members/page/{}/#member-archive-form'

num = 1

while True:
    
    page = requests.get(URL.format(num))
    soup = BeautifulSoup(page.content, 'html.parser')
    div_main = soup.find("div", class_='flex-grid')
    if soup.find("div", class_='card-grid alignwide has-grid-format is-archive has-5-columns').text.strip() == 'There are no members matching your search.':
        break

    members = div_main.find_all('a', class_='card__link')
    for mem in members:
        name, occ = retrieve_info(mem.get('href'))
        if name == 'No person':
            continue
        if occ is None:
            data.append({'Name': name.text.strip().replace('*',''), 'Occupation': ''})
        else:
        
            f = format(occ)
            formatted_occ = ''
            if len(f) > 1:
                for index in range(0, len(f)):
                    if index % 2 == 0:
                        formatted_occ += f[index].strip() + ': '
                    elif index % 2 != 0 and index != len(f) - 1:
                        formatted_occ += f[index].strip() + '; '
                    elif index == len(f) - 1:
                        formatted_occ += f[index].strip()
            else:
                formatted_occ = f[0]
            data.append({'Name': name.text.strip().replace('*', ''), 'Occupation': formatted_occ})
            
    num += 1


#Converting data to an excel sheet
data_frame = pd.DataFrame(data)
data_frame.to_excel('finalhoratioalgermembers.xlsx', index=False)