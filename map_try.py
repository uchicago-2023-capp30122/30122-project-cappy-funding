import plotly.graph_objects as go
import pandas as pd

# Define the data for the map
state_2016 = pd.read_csv("2016_cleaned_funding.csv")['State']

data = go.Choropleth(
    locations=list(state_2016),
    z=[50, 30, 10, 20, 15, 25, 5, 2, 45, 35, 5, 10, 30, 20, 15, 20, 25, 10,
       5, 15, 10, 20, 25, 15, 30, 5, 10, 15, 20, 25, 30, 40, 20, 25, 15,
       10, 25, 30, 20, 25, 10, 5, 25, 15, 10, 20, 30, 20, 25, 10, 30, 15],
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
