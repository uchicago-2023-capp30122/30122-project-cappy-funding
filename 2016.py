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
                value = "Agriculture, Forestry, Fishing and Hunting",
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

    # Create a Choropleth object
    fig = go.Figure(
        data = [go.Choropleth(
            locationmode="USA-states",
            locations=dff["State"],
            z=dff["Utilities"].astype(float),
            colorscale="Reds",
            zmin=0,
            zmax=50,
            text=dff["State"],
            hoverinfo="text+z",
            marker_line_color="white",
            colorbar=dict(title="% of Total Funding")
        )]
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
    app.run_server(debug=True)
