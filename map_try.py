import plotly.graph_objects as go
import pandas as pd

us_state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

# Define the data for the map
state_2016 = pd.read_csv("2016_cleaned_funding.csv")['State']
num_2016 = pd.read_csv("2016_cleaned_funding.csv")["Agriculture, Forestry, Fishing and Hunting (State as % of US)"]
locations = list(state_2016)
weights = list(num_2016)
map_list = []
num_list = []
for location in locations[:-1]:
    map_list.append(us_state_abbreviations[location])

for weight in weights[:-1]:
    num_list.append(weight)

data = go.Choropleth(
    locations = map_list,
    z=num_list,
    locationmode='USA-states',
    colorscale='Reds',
    colorbar_title="Score"
)

# Define the layout for the map
layout = go.Layout(
    title_text='USA Heat Map',
    geo_scope='usa'
)

# Create the figure with the data and layout
fig = go.Figure(data=data, layout=layout)

# Show the interactive map
fig.show()
