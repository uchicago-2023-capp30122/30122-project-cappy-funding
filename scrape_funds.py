import requests
import pandas as pd
import csv


url = "https://api.usaspending.gov"
endpoint = "/api/v2/recipient/state/"
params = {"fips": 57, "year": 2017}
response = requests.get(f"{url}{endpoint}")
data = response.json()
df = pd.DataFrame(data["results"])

# total amound in every state
with open("state_total_data.csv", "w", newline = "") as csvfile:
    writer = csv.writer(csvfile)
    headers = data[0].keys()
    writer.writerow(headers)
    for state in data:
        writer.writerow(state.values())
