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

def funding_word_clouds():
    """
    Create word cloud graphs for each year between 2016 and 2020 based on 
    federal funding by NAICS category.
    """
    
    # load the funding image
    funding_mask = np.array(Image.open("Funding2.png"))

    # Create a Dash app
    app = dash.Dash(__name__)

    # Read the data
    df = pd.read_csv('us_funding_time_series.csv')

    # Define the years
    years = [str(year) for year in range(2016, 2021)]

    # Define the layout
    app.layout = html.Div([
        html.H1('Federal Funding Word Clouds by NAICS Category', style={'textAlign': 'center'}),
        html.Div([
            html.Label('Select Year:'),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in years],
                value='2016'
            ),
        ], style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='wordcloud-graph')
    ])

    @app.callback(Output('wordcloud-graph', 'figure'),
                  Input('year-dropdown', 'value'))
    def update_wordcloud(year):
        # create a dictionary that contains the NAICS category as the key and the funding percentage for the current year as the value
        category_weight = {}
        for _, row in df.iterrows():
            category = row['NAICS Category']
            weight = row[year]
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

        # Convert the Matplotlib figure to a Plotly figure
        fig = px.imshow(wordcloud.to_array())
        fig.update_layout(title=f"Word Cloud of NAICS Category for {year}", title_font_size=20)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)

        return fig

    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)