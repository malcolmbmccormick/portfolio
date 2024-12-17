#Extension of flight data program
import pandas as pd
from geopy.geocoders import Nominatim
from flightdata import *
from scraper import *
from requests.exceptions import Timeout, RequestException



# List of coastal states in the US
coastal_states = [
    'Alabama', 'Alaska', 'California', 'Connecticut', 'Delaware', 'Florida', 
    'Georgia', 'Hawaii', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 
    'Mississippi', 'New Hampshire', 'New Jersey', 'New York', 'North Carolina', 
    'Oregon', 'Rhode Island', 'South Carolina', 'Texas', 'Virginia', 'Washington'
]
coastal_states = set(coastal_states)
# List of all US states
us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", 
    "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", 
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", 
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", 
    "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
us_states = set(us_states)

geolocator = Nominatim(user_agent='coastal_flight')

def is_coastal(coordinates) -> bool:
    """
    Function that determines whether a set of coordinate pairs is located in a coastal state or not
    """
    # Retrieves the state the coordinate is in and returns True if this is a coastal state and False otherwise.
    lat, long = coordinates
    location = geolocator.reverse(f'{lat}, {long}',timeout=None)
    if location is None:
        return False
    full = location.address.split(",")
    for place in full:
        if place.lstrip() in coastal_states:
            return True
    return False
    

def in_US(coordinates) -> bool:
    """
    Determines if a latitude/longitude coordinate pair is in the United States.
    """
    #Returns True if this coordinate is located in the United States
    lat, long = coordinates
    location = geolocator.reverse(f'{lat}, {long}',timeout=None)
    if location is None:
        return False
    full = location.address.split(",")
    for place in full:
        if place.lstrip() in us_states:
            return True
    return False
    
 

def calculate_percentages(path: str) -> tuple[float, float, float, float, int]:
    count = 0
    URL = f'https://samples.adsbexchange.com/traces/2024/06/01/{path}/'
    icao_numbers = get_icao_numbers(URL)
    # Scrapes all ICAO numbers from the specified file
    total_landings = 0
    total_takeoffs = 0
    count_takeoffs_coastal = 0
    count_landings_coastal = 0
    for icao_num in icao_numbers:
        URL = f'https://samples.adsbexchange.com/traces/2024/06/01/{path}/trace_full_{icao_num}.json'
        response = requests.get(URL, timeout=None)
        flight_data = response.json()
        if not 'noRegData' in flight_data.keys():
            # Only considers ICAO's with properly registered data
            data = retrieve(flight_data)
            if len(data) == 1:
                count += 1
                    # Restricts to only ICAO's with one flight on 06/01/2024 to identify private planes
                for tup in data:
                    takeoff, landing, unix = tup
                    if in_US(takeoff):
                        # If the takeoff is in the US, add one to count
                        total_takeoffs += 1
                        if is_coastal(takeoff):
                                # If the takeoff is coastal, add one to count
                            count_takeoffs_coastal += 1
                    if in_US(landing):
                            # If the landing is in the US, add one to count
                        total_landings += 1
                        if is_coastal(landing):
                                # If the takeoff is coastal, add one to count
                            count_landings_coastal += 1
    
    return (total_takeoffs, count_takeoffs_coastal, total_landings, count_landings_coastal, count)
    


def find_percentages(file_map, icaos_lst) -> tuple[float, float]:
    """
    Calculates percentages of landings/takeoffs that are coastal
    """
    takeoffs_coastal = 0
    landings_coastal = 0
    takeoffs_total = 0
    landings_total = 0
    for icao in icaos_lst:
        if icao in file_map.keys():
            f = file_map[icao]
            URL = f'https://samples.adsbexchange.com/traces/2024/06/01/{f}trace_full_{icao}.json'
            response = requests.get(URL, timeout=None)
            data = response.json()
            flight_data = retrieve(data)
            for flight in flight_data:
                takeoff, landing, unix = flight
                if in_US(takeoff):
                    takeoffs_total += 1
                    if is_coastal(takeoff):
                        takeoffs_coastal += 1
                if in_US(landing):
                    landings_total += 1
                    if is_coastal(landing):
                        landings_coastal += 1
    takeoff_percent = (100 * takeoffs_coastal) / takeoffs_total
    landing_percent = (100 * landings_coastal) / landings_total
    return (takeoff_percent, landing_percent)


def calculate_percentages_full_sample(path: str) -> tuple[float, float, float, float, int]:
    count = 0
    URL = f'https://samples.adsbexchange.com/traces/2024/06/01/{path}/'
    icao_numbers = get_icao_numbers(URL)
    # Scrapes all ICAO numbers from the specified file
    total_landings = 0
    total_takeoffs = 0
    count_takeoffs_coastal = 0
    count_landings_coastal = 0
    for icao_num in icao_numbers:
        URL = f'https://samples.adsbexchange.com/traces/2024/06/01/{path}/trace_full_{icao_num}.json'
        try:
            response = requests.get(URL, timeout=None)
        except Exception:
            print("The request timed out after waiting for a long time")
            continue
        flight_data = response.json()
        if not 'noRegData' in flight_data.keys():
            # Only considers ICAO's with properly registered data
            data = retrieve(flight_data)
            if len(data) > 0:
                    count += 1
                    # No restrictions on flights, this is full sample
                    for tup in data:
                        takeoff, landing, unix = tup
                        if in_US(takeoff):
                            # If the takeoff is in the US, add one to count
                            total_takeoffs += 1
                            if is_coastal(takeoff):
                                # If the takeoff is coastal, add one to count
                                count_takeoffs_coastal += 1
                                print(takeoff)
                        if in_US(landing):
                            # If the landing is in the US, add one to count
                            total_landings += 1
                            if is_coastal(landing):
                                # If the takeoff is coastal, add one to count
                                count_landings_coastal += 1
    
    return (total_takeoffs, count_takeoffs_coastal, total_landings, count_landings_coastal, count)





""" rv = []
total_icao = 0
coastal_landings_full = 0
coastal_takeoffs_full = 0
dictionary_full = {}
dictionary_full['Type'] = 'Only 1 Flight Sample'
dictionary_full['# Departures'] = 0
dictionary_full['# Landings'] = 0
for path in ['50', '51', '52', '53', '54', '55']: 
  if dictionary_full['# Departures'] > 120:
      break
  a, b, c, d, e = calculate_percentages(path)
  total_icao += e
  dictionary_full['# Departures'] += a
  dictionary_full['# Landings'] += c
  coastal_takeoffs_full += b
  coastal_landings_full += d
 
print(dictionary_full['# Departures'])
print(dictionary_full['# Landings'])
print(coastal_takeoffs_full)
print(coastal_landings_full) """