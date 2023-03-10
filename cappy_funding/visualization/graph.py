import base64
import os
import dash
import numpy as np
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import matplotlib.pyplot as plt

# Author: Gongzi Chen

app = dash.Dash(__name__)

# Import and clean data
CLEAN_DATA_DIR = "./cappy_funding/data/clean_data/"
df = pd.read_csv(CLEAN_DATA_DIR + "all_years_funding_by_state.csv")

# functions for fig
#scatterplot
def create_scatterplot():
    # Load data for each year
    data = {}
    for year in range(2016, 2021):
        df = pd.read_csv(CLEAN_DATA_DIR + f"{year}_per_capita_analysis.csv")
        df = df.drop(df[df["State"] == "United States"].index)
        populations = pd.read_csv(CLEAN_DATA_DIR + "us_population_cleaned.csv")
        populations = populations.drop(populations[populations["State"] == "United States"].index)
        df = pd.merge(df, populations, on="State")
        data[str(year)] = df

    # Create scatter plot
    fig = go.Figure()

    # Add scatter traces for each year
    for year, df in data.items():
        fig.add_trace(go.Scatter(
            x=df["Population"],
            y=df["Expenditure per Capita (in thousands)"],
            mode="markers",
            visible=(year == "2016"),
            name=year,
            marker=dict(
                size=10,
                color=df["Expenditure per Capita (in thousands)"],
                colorscale="Viridis",
                colorbar=dict(title="Expenditure per Capita (in thousands)")
            ),
            text=df["State"]
        ))

    # Calculate mean Expenditure per Capita for the year
    mean_expenditure = df["Expenditure per Capita (in thousands)"].mean()

    # Add mean line
    fig.add_shape(
        type="line",
        x0=df["Population"].min(),
        x1=df["Population"].max(),
        y0=mean_expenditure,
        y1=mean_expenditure,
        line=dict(
            color="red",
            width=2,
        )
    )

    # Add annotation for mean line
    fig.add_annotation(
        x=df["Population"].max(),
        y=mean_expenditure,
        text="Mean",
        showarrow=False,
        font=dict(
            size=12,
            color="red"
        ),
        xanchor="left",
        yanchor="top",
        xshift=10,
        yshift=10,
    )

    # Customize layout
    fig.update_layout(
        title="Expenditure per Capita vs Population",
        xaxis_title="Population",
        yaxis_title="Expenditure per Capita (in thousands)", 
    )

    # Add dropdown menu
    dropdown_menu = []
    for year in range(2016, 2021):
        dropdown_menu.append(
            dict(
                label=str(year),
                method="update",
                args=[
                    {"visible": [y == str(year) for y in data.keys()]},
                    {"title": f"Expenditure per Capita vs Population ({year})"}
                ]
            )
        )
    fig.update_layout(
        updatemenus=[dict(
            type="dropdown",
            active=0,
            buttons=dropdown_menu,
            x=0.1,
            y=1.1,
            xanchor="left",
            yanchor="top"
        )]
    )

    return fig

# stacked area chart
stacked_area_chart_path = os.path.join('cappy_funding', 'visualization', 'stacked_area_chart.png')

with open(stacked_area_chart_path, 'rb') as f:
    encoded_stacked_area_chart = base64.b64encode(f.read()).decode()

# stacked bar chart
def create_stacked_bar_chart():
    """
    Create a stacked bar chart using Plotly Express to show the top 10 NAICS 
    categories that received federal funding between 2016 and 2020. 
    The chart displays the funding percentage for each category in each year.
    """

    # Read in the data
    df = pd.read_csv(CLEAN_DATA_DIR + 'us_funding_time_series.csv')

    # Calculate the mean funding percentage for each category over the 5-year period
    df_mean = df.loc[:, '2016':'2020'].mean(axis=1)
    df_mean.index = df['NAICS Category']
    df_mean = df_mean.reset_index(name='Mean Percentage')

    # Sort the data by the mean funding percentage and select only the top 10 categories
    df_top_10 = df_mean.sort_values(by='Mean Percentage', ascending=False).head(10)
    category_order = df_top_10['NAICS Category'].tolist()

    # Filter the original dataframe to include only the top 10 categories
    df_filtered = df[df['NAICS Category'].isin(category_order)]

    # Melt the data so that each row represents a single observation
    df_melt = pd.melt(df_filtered, id_vars=['NAICS Category'], var_name='Year', value_name='Funding Percentage')

    # Create the stacked bar chart using Plotly Express and set the category order
    fig = px.bar(df_melt, x='Year', y='Funding Percentage', color='NAICS Category', barmode='stack', category_orders={'NAICS Category': category_order})

    # Update the figure information
    fig.update_xaxes(type='category')
    fig.update_layout(title='Top 10 Categories receiving Federal Funding by Year (2016-2020)')

    # Show chart
    return fig

#word cloud
word_cloud_paths = [
    os.path.join('cappy_funding', 'visualization', 'word_cloud_2016.png'),
    os.path.join('cappy_funding', 'visualization', 'word_cloud_2017.png'),
    os.path.join('cappy_funding', 'visualization', 'word_cloud_2018.png'),
    os.path.join('cappy_funding', 'visualization', 'word_cloud_2019.png'),
    os.path.join('cappy_funding', 'visualization', 'word_cloud_2020.png')
]

encoded_word_clouds = [base64.b64encode(open(image_path, 'rb').read()) for image_path in word_cloud_paths]

def expenditurepc_vs_fundingpc_scatterplot():
    """
    Create a scatter plot showing expenditure per capita versus funding per 
    capita for each state in the United States from 2016 to 2020.
    """

    dfs = []

    # Load data for each year
    for year in range(2016, 2021):
        # Read in the per capita analysis csv for the year
        df = pd.read_csv(CLEAN_DATA_DIR + f"{year}_per_capita_analysis.csv")
        df = df.drop(df[df["State"] == "United States"].index)
        df["Year"] = year
        dfs.append(df)

    df = pd.concat(dfs)
    df_pop = pd.read_csv(CLEAN_DATA_DIR + 'us_population_cleaned.csv')
    df_merge = pd.merge(df, df_pop, on='State', how='left')

    # Calculate the total expenditure and funding for each state for each year
    df_grouped = df_merge.groupby(['Year', 'State', 'Population'], as_index=False).sum()

    # Remove the United States from the data
    df_grouped = df_grouped[df_grouped['State'] != 'United States']

    # Create a scatter plot of expenditure per capita vs funding per capita
    fig = px.scatter(df_grouped, 
                    x='Funding received per Capita (in thousands)', 
                    y='Expenditure per Capita (in thousands)', 
                    color='State', 
                    hover_name='State', 
                    size='Population', 
                    animation_frame='Year', 
                    color_discrete_sequence=px.colors.qualitative.Alphabet
                    )

    fig.update_layout(title='Expenditure per Capita vs Funding received per Capita (2016-2020)')

    # Show the plot
    return fig



# app layout
app.layout = html.Div([
    html.H1("USA States Funding and Expenditure", style = {"text-align": "center"}),

    html.H2("Scatterplot Graph for Fund Expenditure", style = {"color": "red", "text-align": "center"}),

    dcc.Graph(id = "scatterplot", style = {"padding": "40px"}),

    html.H2("Stacked Area Chart for Funding", style = {"color": "brown", "text-align": "center"}),

    html.Img(src='data:image/png;base64,{}'.format(encoded_stacked_area_chart), style = {"padding": "40px", 'width': '100%'}),

    html.H2("Stacked Bar Charts", style = {"color": "green", "text-align": "center"}),

    dcc.Graph(id = "stacked_bar_charts", style = {"padding": "40px"}),

    html.H2("Word Cloud", style = {"color": "pink", "text-align": "center"}),

    dcc.Dropdown(id='year-dropdown', 
            options=[
                    {'label': '2016', 'value': 0},
                    {'label': '2017', 'value': 1},
                    {'label': '2018', 'value': 2},
                    {'label': '2019', 'value': 3},
                    {'label': '2020', 'value': 4}], 
            value=0,
            style = {"width": "50%", "margin": "auto"}
    ),

    html.Img(id='image', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '50%'}),

    html.H2("Expenditure VS Funding Scatterplot", style = {"color": "blue", "text-align": "center"}),

    dcc.Graph(id = "scatterplot2", style = {"padding": "40px"}),

    html.H2("Heat Map of USA States Fund Spending", style = {"text-align": "center", "padding": "40px"}),

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
            style = {"width": "50%", "margin": "auto"}
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

# app callbacks
# Define callback to update image based on dropdown selection
@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_image_src(value):
    return 'data:image/png;base64,{}'.format(encoded_word_clouds[value].decode())

@app.callback(
    [Output(component_id = "scatterplot", component_property = "figure"),
     Output(component_id = "stacked_bar_charts", component_property = "figure"),
     Output(component_id = "scatterplot2", component_property = "figure"),
     Output(component_id = "heat-map", component_property = "figure")],
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

    fig1 = create_scatterplot()
    fig2 = create_stacked_bar_chart()
    fig3 = expenditurepc_vs_fundingpc_scatterplot()

    return fig1, fig2, fig3, fig

if __name__ == '__main__':
    app.run_server(debug=True)