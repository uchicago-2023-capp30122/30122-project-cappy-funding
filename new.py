import os
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(__name__)

# Import and clean data
STATE_DATA = "data/clean_data/"
file_name = "all_years_funding_by_state.csv"
file_path = os.path.join(STATE_DATA, file_name)

df = pd.read_csv(file_path)




# app layout
app.layout = html.Div([

    html.H1("USA States Fund Spending Heat Map", style = {"text-align": "center"}),

    dcc.Dropdown(id = "select_year",
                options=[
                        {"label": "2016", "value": 2016},
                        {"label": "2017", "value": 2017},
                        {"label": "2018", "value": 2018},
                        {"label": "2019", "value": 2019},
                        {"label": "2020", "value": 2020}],

                multi = False,
                value = 2016,
                style = {"width": "40%"}
                ),

    dcc.Graph(id = "heat-map")

])

# app callback
@app.callback(
    Output(component_id = "heat-map", component_property = "figure"),
    [Input(component_id = "select_year", component_property = "value")]
)

def generate_graph(option_year):

    dff = df.copy()
    dff = dff[dff["Year"] == option_year]
    state_code = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', \
                  'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', \
                    'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', \
                        'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', \
                            'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    dff['state_code'] = state_code

    # Create a Choropleth object
    fig = px.choropleth(
        data_frame = dff,
        locationmode="USA-states",
        locations="state_code",
        scope="usa",
        color="Construction",
        hover_data=["State", "Construction"],
        labels={"Construction": "% of Construction  Funding"},
        color_continuous_scale="YlOrRd"
    )


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
