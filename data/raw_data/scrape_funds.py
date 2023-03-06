import requests
import pandas as pd
import csv

# total amound in every state
def total_funding():

    url = "https://api.usaspending.gov"
    endpoint = "/api/v2/recipient/state/"
    response = requests.get(f"{url}{endpoint}")
    data = response.json()

    with open("state_total_data.csv", "w", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        headers = data[0].keys()
        writer.writerow(headers)
        for state in data:
            writer.writerow(state.values())

# get the data from one year: 2016
def get_states():

    total_data = pd.read_csv("state_total_data.csv")
    list_states = total_data["code"]
    
    return list_states

def data_year():

    list_states = get_states()
    url = "https://api.usaspending.gov"
    endpoint = "/api/v2/search/spending_by_category/naics"
    dict = {}

    for year in ['2016', '2017', '2018', '2019', '2020']
        for state in list_states:

            payload = {
                "filters": {
                "place_of_performance_locations": [
                {"country": "USA",
                "state": state}
                
                ],
    
                "time_period": [
                    {"start_date": f"{year}-01-01",
                    "end_date": f"{year}-12-31"}],
                "lower_bound": 0
                }
                ,
                "page": 1,
                "limit": 100,
                "category": "naics"
                }

            results = []
            response = requests.post(f"{url}{endpoint}", json = payload)
            data = response.json()["results"]

            while len(data) == 100:
                response = requests.post(f"{url}{endpoint}", json = payload)
                data = response.json()["results"]
                results.extend(data)
                if len(data) < 100:
                    break
                payload["page"] += 1
            
            dict[state] = results
                    
        with open(f"data/raw_data/{year}_us_funding.csv", "w", newline = "") as csvfile:

            writer = csv.writer(csvfile)
            headers = list(dict[state][0].keys())
            headers.append('State')
            writer.writerow(headers)

            for state, results in dict.items():
                for row in results:
                    row_vals = list(row.values())
                    row_vals.append(state)
                    writer.writerow(row_vals)

    return 