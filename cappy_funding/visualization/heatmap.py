import os
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

# Author: Gongzi Chen

app = dash.Dash(__name__)

# Import and clean data
CLEAN_DATA = "data/clean_data/"
file_name = "all_years_funding_by_state.csv"
file_path = os.path.join(CLEAN_DATA, file_name)
df = pd.read_csv(file_path)




# app layout
app.layout = html.Div([

    html.H1("USA States Fund Spending Heat Map", style = {"text-align": "center"}),

    dcc.Dropdown(id = "select_field",
                options=[
                        {"label": "Agriculture, Forestry, Fishing and Hunting", "value": "Agriculture, Forestry, Fishing and Hunting"},
                        {"label": "Mining, Quarrying, and Oil and Gas Extraction", "value": "Mining, Quarrying, and Oil and Gas Extraction"},
                        {"label": "Utilities", "value": "Utilities"},
                        {"label": "Construction", "value": "Construction"},
                        {"label": "Manufacturing", "value": "Manufacturing"},
                        {"label": "Wholesale Trade", "value": "Wholesale Trade"},
                        {"label": "Retail Trade", "value": "Retail Trade"},
                        {"label": "Transportation and Warehousing", "value": "Transportation and Warehousing"},
                        {"label": "Information", "value": "Information"},
                        {"label": "Finance and Insurance", "value": "Finance and Insurance"},
                        {"label": "Real Estate and Rental and Leasing", "value": "Real Estate and Rental and Leasing"},
                        {"label": "Professional, Scientific, and Technical Services", "value": "Professional, Scientific, and Technical Services"},
                        {"label": "Administrative and Support and Waste Management and Remediation Services", "value": "Administrative and Support and Waste Management and Remediation Services"},
                        {"label": "Educational Services", "value": "Educational Services"},
                        {"label": "Health Care and Social Assistance", "value": "Health Care and Social Assistance"},
                        {"label": "Arts, Entertainment, and Recreation", "value": "Arts, Entertainment, and Recreation"},
                        {"label": "Accommodation and Food Services", "value": "Accommodation and Food Services"},
                        {"label": "Other Services (except Public Administration)", "value": "Other Services (except Public Administration)"},
                        {"label": "Public Administration (not covered in economic census)", "value": "Public Administration (not covered in economic census)"}],
                multi = False,
                value = "Agriculture, Forestry, Fishing and Hunting",
                style = {"width": "40%"}
    ),

    dcc.Graph(id = "heat-map", style = {"padding": "40px"}),

    dcc.Slider(
        id = "year_slider",
        min = 2016,
        max = 2020,
        value = 2018,
        marks = {2016: "2016", 2017: "2017", 2018: "2018", 2019: "2019", 2020: "2020"},
        step = 1
        )
])

# app callback
@app.callback(
    Output(component_id = "heat-map", component_property = "figure"),
    [Input(component_id = "select_field", component_property = "value"),
    Input(component_id = "year_slider", component_property = "value")]
)

def generate_graph(option_field, option_year):
    dff = df.copy()
    dff = dff[dff["Year"] == option_year]
    state_code = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', \
                  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', \
                  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',\
                  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI','SC', \
                  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    dff['state_code'] = state_code


    # Create a Choropleth object
    fig = go.Figure(
        go.Choropleth(
            locationmode="USA-states",
            locations=dff["state_code"],
            z=dff[option_field],
            colorscale="Sunset",
            zmin=0,
            zmax=35,
            text=dff["State"],
            hoverinfo="text+z",
            marker_line_color="white",
            colorbar=dict(title="% of Total Funding")
        )
    )

    # Set the layout of the plot
    fig.update_layout(
        title="USA States Fund Spending Heat Map",
        geo_scope="usa",
        template="plotly_dark",
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig


if __name__ == '__main__':
    app.run_server(port = 12346, debug=True)
