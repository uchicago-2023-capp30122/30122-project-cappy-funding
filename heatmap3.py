import os
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# read data
STATE_DATA = "data/clean_data/"
file_name = "all_years_funding_by_state.csv"
file_path = os.path.join(STATE_DATA, file_name)

df = pd.read_csv(file_path)

# define app
app = dash.Dash(__name__)

# define app layout
app.layout = html.Div([
    html.H1("USA States Heat Map", style={"text-align": "center"}),
    dcc.Dropdown(
        id='dropdown',
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
                        {"label": "Other Services", "value": "Other Services"},
                        {"label": "Public Administration", "value": "Public Administration"}
        ],
        value='Utilities',
        style={"width": "40%"}
    ),
    dcc.Graph(id="graph"),
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
])

# define app callback
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value'),
     Input('year-slider', 'value')]
)

def update_figure(selected_value, selected_year):
    state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    print("Selected Value:", selected_value)
    print("Selected Year:", selected_year)
    dff = df[(df['Year'] == selected_year)]
    print("Filtered DF:", dff)
    print("selected_value", dff[selected_value])
    print("states:", dff["State"])

    data = go.Choropleth(
        locations=state_list,
        z=dff[selected_value],
        locationmode='USA-states',
        colorscale='Reds',
        colorbar_title="Funding",
    )
    layout = go.Layout(
        geo_scope='usa'
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

# run app
if __name__ == '__main__':
    app.run_server(debug=True)
