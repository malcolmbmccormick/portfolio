import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import json

#Grabbed this list from flight data work so can easily identify members states
us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", 
    "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", 
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", 
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", 
    "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

def get_elements(input: str) -> tuple[str, str, str, str]:
    """
    This function returns the age, state, company, and philanthropy score of a member.
    """
    age = ""
    state_good = ""
    company = ""
    score = ""
    age += input[0:2]
    if input[-1].isdigit():
        thres = len(input) - 1
        score += input[-1]
    else:
        thres = len(input)
        score = 'None'
    
    state_and_company = input[2:thres]
    state = ''
    for index in range(0, len(state_and_company)):
        if state in us_states:
            state_good = state
            company = state_and_company[index:]
            break
        else:
            state += state_and_company[index]

    if state not in us_states:
        company = state_and_company

    return age, state_good, company, score
    
   
#Storing output data in a list of dictionaries
forbes_members = []

driver = webdriver.Chrome()
driver.get('https://www.forbes.com/forbes-400/')
time.sleep(5)

counter = 0
#Getting industries for each member. A dictionary that maps each member to their specific industry.
#Had to manually get the XPaths for this. Quite annoying.
html = driver.page_source
soup = BeautifulSoup(html)
names_industries = {}
ind = {}
ind['AUTOMOTIVE'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[2]'
ind['CONSTRUCTION & ENGINEERING'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[3]'
ind['DIVERSIFIED'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[4]'
ind['ENERGY'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[5]'
ind['FASHION & RETAIL'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[6]'
ind['FINANCE & INVESTMENTS'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[7]'
ind['FOOD & BEVERAGE'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[8]'
ind['GAMBLING & CASINOS'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[9]'
ind['HEALTHCARE'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[10]'
ind['LOGISTICS'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[11]'
ind['MANUFACTURING'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[12]'
ind['MEDIA & ENTERTAINMENT'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[13]'
ind['REAL ESTATE'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[14]'
ind['SERVICE'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[15]'
ind['SPORTS'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[16]'
ind['TECHNOLOGY'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[17]'
ind['TELECOM'] = '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div/ul/li[18]'

for industry in ind.keys():
    y = driver.find_element(By.CLASS_NAME, 'Table_dropdownValue__5YvrN')
    time.sleep(1)
    y.click()
    indus = driver.find_element(By.XPATH, ind[industry])
    time.sleep(1)
    indus.click()
    html = driver.page_source
    soup = BeautifulSoup(html)
    for tag in soup.find_all('div', class_='Table_tableRow__x3HMS'):
        name = tag.find("div", class_='Table_personName__TFdLv').text
        if name not in names_industries:
            names_industries[name] = industry
        else:
            pass
driver.quit()


driver = webdriver.Chrome()
driver.get('https://www.forbes.com/forbes-400/')


def get_industry(name: str) -> str:
    """
    Returns the industry of the specified Forbes 400 member
    """
    if name in names_industries:
        return names_industries[name]
    return "None"

#List of ids or links to fullprofile web pages so can scrape their personal stats and wealth history
full_profile_ids = []

#Looping through all pages of the website
for idx in range(3):
    
    html = driver.page_source
    soup = BeautifulSoup(html)
    for tag in soup.find_all('div', class_='Table_tableRow__x3HMS'):
        full = tag.text
        period_index = full.index(".")
        person_rank = full[0:period_index]
        person = {}
        person['RANK'] = person_rank
        person['NAME'] = tag.find("div", class_='Table_personName__TFdLv').text
        person['NET WORTH'] = tag.find("div", class_='Table_finalWorth__ltFaS').text
        last4 = tag.text[tag.text.index(person['NET WORTH']) + len(person['NET WORTH']):]
        x = get_elements(last4)
        person['AGE'] = x[0]
        person['STATE'] = x[1]
        person['SOURCE'] = x[2]
        person['PHILANTHROPY SCORE'] = x[3]
        person["INDUSTRY"] = get_industry(person['NAME'])
        person['Self-Made Score'] = ''
        person['Source of Wealth'] = ''
        person['Residence'] = ''
        person['Citizenship'] = ''
        person['Marital Status'] = ''
        person['Children'] = ''
        person['Education'] = ''
        forbes_members.append(person)
    panel = driver.find_elements(By.CLASS_NAME, 'Table_tableRow__x3HMS')
    time.sleep(1)
    #This fills the fullprofile list up so we can access their personal profile pages
    full_profile_ids.extend([element.get_attribute('id') for element in panel])
   
    #This 'clicks' on the next page button so we can access the next 2 pages
    if idx == 2:
        break
    if idx == 0:
        nxt = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[2]/div/div[2]/div[21]/div[17]/div[1]/nav/div/button[3]')
    if idx == 1:
        nxt = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div/div[3]/div[2]/div[2]/div/div[2]/div[21]/div[17]/div[1]/nav/div/button[4]')
    if nxt:
        nxt.click()
    idx += 1
    
driver.quit()

#Grabbing personal stats here: Current Age, Residence, Self_Made score, etc. 
driver = webdriver.Chrome()
counter = 0
for full_profile in full_profile_ids:
    driver.get(f'https://www.forbes.com/profile/{full_profile}/?list=forbes-400')
    html = driver.page_source
    soup = BeautifulSoup(driver.page_source)
    for prof in soup.find_all("dl", class_='listuser-block__item'):
        title = prof.find("dt", class_='profile-stats__title').text
        val = prof.find("dd", class_='profile-stats__text').text
        forbes_members[counter][title] = val
    
    #Grabbing wealth history here. In the website, it is an interactive chart but in the code is a list of dictionaries
    soup = BeautifulSoup(html)
    chart_element = soup.find("canvas", class_='person-networth-chart')
    time.sleep(1)
    if chart_element is None:
        counter += 1
        continue
    chart_data_json = chart_element['data-chart']
    chart_data = json.loads(chart_data_json)
    wealth_history = ''
    for entry in chart_data:
        wealth_history += f"{entry['worth']} : {entry['date']}" + '\n'
    forbes_members[counter]['Wealth History'] = wealth_history
    
    counter += 1
        

#Converting list of dictionaries to a DataFrame and then to a .csv file
tester_csv = pd.DataFrame(forbes_members)
tester_csv.to_csv('finaltester2.csv', index=False)





