import requests
import pandas as pd
import csv

# total amound in every state

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

# get all NAICS code

endpoint = "/api/v2/references/naics/"
response = requests.get(f"{url}{endpoint}")
data = response.json()

with open("naics.csv", "w", newline = "") as csvfile:
    writer = csv.writer(csvfile)
    headers = data['results'][0].keys()
    writer.writerow(headers)
    for state in data['results']:
        writer.writerow(state.values())

naics_data = pd.read_csv("naics.csv")

# get the data from one year: 2016

total_data = pd.read_csv("state_total_data.csv")
list_states = total_data["code"]

def data_year(list_states):
        
    url = "https://api.usaspending.gov"
    endpoint = "/api/v2/search/spending_by_category/naics"
    dict = {}

    for state in list_states:

        payload = {
            "filters": {
            "recipient_locations": [
            {"country": "USA",
             "state": state}
            
            ],
 
            "time_period": [
                {"start_date": "2020-01-01",
                "end_date": "2020-12-31"}],
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
                
    with open("2020_final.csv", "w", newline = "") as csvfile:

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

data_2016 = pd.read_csv("2016.csv")
data_2016 = data_2016.drop(columns = ['id'], axis = 1)
data_2016.to_csv("2016_data.csv", index = False)


