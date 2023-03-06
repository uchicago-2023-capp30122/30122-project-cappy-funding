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
from PIL import Image




app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Stacked Bar Chart'),
    dcc.Graph(id='stacked-bar-chart'),
    html.Div(id='dummy', style={'display': 'none'})
])

@app.callback(Output('stacked-bar-chart', 'figure'), [Input('dummy', 'children')])

def create_stacked_bar_chart(_):
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

if __name__ == '__main__':
    app.run_server(debug=True)



