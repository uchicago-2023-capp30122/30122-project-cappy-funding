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
from wordcloud import WordCloud
from PIL import Image

app = dash.Dash(__name__)

# Import and clean data

# Data for graphs
df = pd.read_csv("all_years_funding_by_state.csv")

# app layout
app.layout = html.Div([
    html.H1("USA States Funding and Expenditure", style = {"text-align": "center"}),

    html.H2("Scatterplot Graph for Fund Expenditure", style = {"color": "red", "text-align": "center"}),

    dcc.Graph(id = "scatterplot", style = {"padding": "40px"}),

    html.H3("Stacked Area Charts", style = {"color": "blue", "text-align": "center"}),

    dcc.Graph(id = "stacked_area_charts", style = {"padding": "40px"}),

    html.H4("Stacked Bar Charts", style = {"color": "blue", "text-align": "center"}),

    dcc.Graph(id = "stacked_bar_charts", style = {"padding": "40px"}),

    html.H5("Word Cloud for Top Fund Spending Fields", style = {"color": "green", "text-align": "center"}),

    dcc.Graph(id = "wordcloud", style = {"padding": "40px"}),

    html.H6("Heat Map of USA States Fund Spending", style = {"text-align": "center", "padding": "40px"}),

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

# app callbacks
@app.callback(
    [Output(component_id = "scatterplot", component_property = "figure"),
     Output(component_id = "stacked_area_charts", component_property = "figure"),
     Output(component_id = "stacked_bar_charts", component_property = "figure"),
     Output(component_id = "wordcloud", component_property = "figure"),
     Output(component_id = "heat-map", component_property = "figure")],
    [Input(component_id = "select_field", component_property = "value"),
    Input(component_id = "year_slider", component_property = "value")]
)

#scatterplot
def create_scatterplot():
    """
    Create a scatter plot showing expenditure per capita versus population for 
    each state in the United States from 2016 to 2020.
    """

    # Load data for each year
    data = {}
    for year in range(2016, 2021):
        df = pd.read_csv(f"{year}_per_capita_analysis.csv")
        df = df.drop(df[df["State"] == "United States"].index)
        populations = pd.read_csv("us_cleaned_population.csv")
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
def create_stacked_area_chart():
    """
    Create a stacked area chart showing federal funding percentage by NAICS 
    category over time (2016-2020).
    """

    # Read CSV file
    df = pd.read_csv('us_funding_time_series.csv', index_col=0)

    # Sort the DataFrame in descending order based on the sum of each row
    df = df.loc[df.sum(axis=1).sort_values(ascending=True).index]

    # Reverse the order of the rows
    df = df.iloc[::-1]

    # Generate a list of 19 pretty and distinguishable colors
    colors = px.colors.qualitative.Alphabet[:19][::-1]

    # Plot stacked area chart with the colors and set y-axis limits
    fig = df.T.plot(kind='area', stacked=True, figsize=(12,8), color=colors, ylim=(0, 100))

    # Add title and labels
    fig = plt.title('Federal Funding Percentage by NAICS Category Over Time (2016-2020)', fontsize=20)
    fig = plt.xlabel('Year', fontsize=14)
    fig = plt.ylabel('Funding Percentage', fontsize=14)
    fig = plt.legend(title='NAICS Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show chart
    return fig

# stacked bar chart
def create_stacked_bar_chart():
    """
    Create a stacked bar chart using Plotly Express to show the top 10 NAICS 
    categories that received federal funding between 2016 and 2020. 
    The chart displays the funding percentage for each category in each year.
    """

    # Read in the data
    df = pd.read_csv('us_funding_time_series.csv')

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

# wordcould
def create_word_clouds():
    """
    Create word cloud graphs for each year between 2016 and 2020 based on 
    federal funding by NAICS category.
    """

    # read the csv file
    df = pd.read_csv('us_funding_time_series.csv')

    # load the funding image
    funding_mask = np.array(Image.open("Funding2.png"))

    # loop through the years
    for year in range(2016, 2021):
        # create a dictionary that contains the NAICS category as the key and the funding percentage for the current year as the value
        category_weight = {}
        for _, row in df.iterrows():
            category = row['NAICS Category']
            weight = row[str(year)]
            category_weight[category] = weight

        # sort the dictionary by value in descending order and select the top 10 categories
        top_categories = dict(sorted(category_weight.items(), key=lambda item: item[1], reverse=True)[:10])

        # create a word cloud object and generate the word cloud using the dictionary and the funding image as the mask
        wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        min_font_size = 7,
                        max_words = 50,
                        mask = funding_mask, # use the funding image as the mask
                        contour_width=1,
                        contour_color='lightgrey',
                        colormap='tab20',
                        scale=2
                    ).generate_from_frequencies(top_categories)

        # plot the word cloud using matplotlib
        fig = plt.figure(figsize = (10, 10), facecolor = None) 
        fig = plt.imshow(wordcloud, aspect='auto')
        fig = plt.axis("off") 
        fig = plt.tight_layout(pad = 0) 
        fig = plt.title(f"Word Cloud of NAICS Category for {year}", fontsize=20)
        return fig
    
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