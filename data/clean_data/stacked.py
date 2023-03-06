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
import plotly.tools as tls

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Stacked Area Chart'),
    dcc.Graph(id='stacked-area-chart'),
    html.Div(id='dummy', style={'display': 'none'})
])

@app.callback(
    dash.dependencies.Output('stacked-area-chart', 'figure'),
    [dash.dependencies.Input('dummy', 'children')]
)
def funding_stacked_area_chart(_):
    """
    Create a stacked area chart showing federal funding percentage by NAICS 
    category over time (2016-2020).
    """

    df = pd.read_csv('us_funding_time_series.csv', index_col=0)

    # Sort the DataFrame in descending order based on the sum of each row
    df = df.loc[df.sum(axis=1).sort_values(ascending=True).index]

    # Reverse the order of the rows
    df = df.iloc[::-1]

    # Plot stacked area chart with the colors and set y-axis limits
    ax = df.T.plot(kind='area', 
            stacked=True, 
            figsize=(12,8), 
            color=px.colors.qualitative.Alphabet[:19][::-1], 
            ylim=(0, 100)
            )

    # Add title and labels
    plt.title('Federal Funding Percentage by NAICS Category Over Time (2016-2020)', fontsize=20)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Funding Percentage', fontsize=14)
    plt.legend(title='NAICS Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Convert matplotlib figure to plotly figure
    fig = tls.mpl_to_plotly(ax.get_figure())

    # Return plotly figure object
    return fig

if __name__ == '__main__':
    app.run_server(port = 10101, debug=True)




