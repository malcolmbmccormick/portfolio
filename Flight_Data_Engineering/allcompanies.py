#
import requests
import csv
import pandas as pd
#from flightdata import *
#from coastal import *
from scraper import *
from flightdata import *
from coastal import *


def get_location(coordinates) -> str:
    """
    Returns County, State from a latitude/longitude pair
    """
    lat, long = coordinates
    location = geolocator.reverse(f'{lat}, {long}',timeout=None)
    if location is None:
        return False
    full = location.address.split(",")
    print(full)
    if len(full) <= 1:
        return f'{full[0]}'
    for i in range(0, len(full) - 1):
        if full[i+1].lstrip() in us_states:
            return f'{full[i].lstrip()}, {full[i+1].lstrip()}'
    return f'{full[-1]}'
    
    





# In the ADS-B trace data, mapping each ICAO to its corresponding file and storing it in dictionary: file_map
file_map = {}
files = get_all_files()
for file in files:
    for icao_num in get_icao_numbers(file):
        file_map[icao_num] = file

# Reading in the ~440 firm dataset
csvfile = pd.read_csv('/Users/malcolmmccormick/Desktop/Walker/allcompaniesicao.csv')
company_icaos = csvfile['icao_hex'] 


# For each ICAO in the imported csv file, will grab a list of flights in County, State format
# Information is stored in 'results' dictionary, mapping each icao number to a list of initial takeoff and landing locations
results = {}
count = 0
for icao in company_icaos:
    if icao in file_map.keys():
        rv = {}
        count += 1
        f = file_map[icao]
        URL = f'https://samples.adsbexchange.com/traces/2024/06/01/{f}trace_full_{icao}.json'
        response = requests.get(URL, timeout=None)
        data = response.json()
        flight_data = retrieve(data)
        full_locations = []
        n = 0
        for flight in flight_data:
            if flight is not None:
                takeoff, landing, _ = flight
                takeoff_loc = get_location(takeoff)
                landing_loc = get_location(landing)
                if n == 0:
                    full_locations.append(takeoff_loc.lstrip())
                    full_locations.append(landing_loc.lstrip())
                else:
                    full_locations.append(landing_loc)
                n += 1
        

        
        results[icao] = full_locations



# Wasn't quite sure how to format the columns, so just made as many columns as the business with highest number of landings
tester_file = csvfile
# Cutting out unecessary columns
columns_to_keep = ['JN_comp_name', 'JN_comp_zipcode', 'comp_state', 'JN_principal_name', 'NETS_SIC_code', 'NETS_sales', 'est_valuation']
tester_file = csvfile[columns_to_keep].copy()
#Not sure if I can make the following easier, seems unecessary though, will try a loop later, but won't anticipate needing many more columns
tester_file['Initial Takeoff'] = [results[icao_num][0] if icao_num in file_map.keys() and len(results[icao_num]) > 0 else '' for icao_num in company_icaos]
tester_file['First Destination'] = [results[icao_num][1] if icao_num in file_map.keys() and len(results[icao_num]) > 1 else '' for icao_num in company_icaos]
tester_file['Second Location'] = [results[icao_num][2] if icao_num in file_map.keys() and len(results[icao_num]) > 2 else '' for icao_num in company_icaos]
tester_file['Third Location'] = [results[icao_num][3] if icao_num in file_map.keys() and len(results[icao_num]) > 3 else '' for icao_num in company_icaos]
tester_file['Fourth Location'] = [results[icao_num][4] if icao_num in file_map.keys() and len(results[icao_num]) > 4 else '' for icao_num in company_icaos]
tester_file['Fifth Location'] = [results[icao_num][5] if icao_num in file_map.keys() and len(results[icao_num]) > 5 else '' for icao_num in company_icaos]
tester_file['Sixth Location'] = [results[icao_num][6] if icao_num in file_map.keys() and len(results[icao_num]) > 6 else '' for icao_num in company_icaos]
tester_file['Seventh Location'] = [results[icao_num][7] if icao_num in file_map.keys() and len(results[icao_num]) > 7 else '' for icao_num in company_icaos]
tester_file['Eight Location'] = [results[icao_num][8] if icao_num in file_map.keys() and len(results[icao_num]) > 8 else '' for icao_num in company_icaos]

# Calculating the percentages of takeoffs and landings that are in coastal US states
t, l = find_percentages(file_map, company_icaos)
tester_file['% Takeoffs Coastal'] = [t if icao == 'a42686' else '' for icao in company_icaos]
tester_file['% Landings Coastal'] = [l if icao == 'a42686' else '' for icao in company_icaos]
#for n in range(0, 8 + 1):
    #tester_file See if it is possible to do this automatically



tester_csv = pd.DataFrame(tester_file)
tester_csv.to_csv('jetflights.csv', index=False)





    





