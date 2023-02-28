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

# the amount in every state of every sector

total_data = pd.read_csv("state_total_data.csv")
url = "https://api.usaspending.gov"
endpoint = "/api/v2/search/spending_by_category/naics"

for year in [2016]:
    dict = {}
    for state in total_data["code"]:

        payload = {
"filters": {
    "recipient_location": [
        {
            "country": "USA",
            "state": f"{state}",
            "county": "",
            "city": "",
            "zip": "",
            "congressional_district": ""
        }
    ],
    "time_period": [
        {"start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31"}]
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
        
        dict[f'{state}'] = results
            
    with open(f"{year}.csv", "w", newline = "") as csvfile:

        writer = csv.writer(csvfile)
        headers = list(dict[0].values()[0].keys())
        headers.append('State')
        writer.writerow(headers)

        for state, results in dict.items():
            for row in results:
                row_vals = list(row.values())
                row_vals.append(f'{state}')
                writer.writerow(row_vals)

# disparse the loop into one year: 2016

total_data = pd.read_csv("state_total_data.csv")
list_states = total_data["code"]

def data_year(list_states):
        
    url = "https://api.usaspending.gov"
    endpoint = "/api/v2/search/spending_by_category/naics"
    dict = {}

    for state in list_states:

        payload = {
            "filters": {
            "recipient_location": [
                {
                    "country": "USA",
                    "state": state,
                    "county": "",
                    "city": "",
                    "zip": "",
                    "congressional_district": ""
                }
            ],
            "time_period": [
                {"start_date": "2016-01-01",
                "end_date": "2016-12-31"}]
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
                
    with open("2016.csv", "w", newline = "") as csvfile:

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


# try
payload = {
    "filters": {
        "recipient_location": [
            {
                "country": "USA",
                "state": "AK",
                "county": "",
                "city": "",
                "zip": "",
                "congressional_district": ""
            }
        ],
        "time_period": [
            {"start_date": "2017-01-01",
            "end_date": "2017-12-31"}]
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

print(results[:20])

with open("2017.csv", "w", newline = "") as csvfile:
    writer = csv.writer(csvfile)
    headers = list(results[0].keys())
    headers.append('State')
    writer.writerow(headers)
    for state in results:
        values = list(state.values())
        values.append('Alaska')
        writer.writerow(values)

data_2016 = pd.read_csv("2016.csv")
data_2016 = data_2016.drop(columns = ['id'], axis = 1)
data_2016.to_csv("2016_data.csv", index = False)

# They are returning the same thing 

