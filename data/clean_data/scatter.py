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
    html.H1('Scatterplot Chart'),
    dcc.Graph(id='scatter'),
    html.Div(id='dummy', style={'display': 'none'})
])

@app.callback(Output('scatter', 'figure'), [Input('dummy', 'children')])

def create_scatterplot(_):
    # Load data for each year
    data = {}
    for year in range(2016, 2021):
        df = pd.read_csv(f"{year}_per_capita_analysis.csv")
        df = df.drop(df[df["State"] == "United States"].index)
        populations = pd.read_csv("us_population_cleaned.csv")
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

if __name__ == '__main__':
    app.run_server(debug=True)



