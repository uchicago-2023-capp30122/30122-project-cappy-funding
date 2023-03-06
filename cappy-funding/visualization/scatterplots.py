import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

def expenditurepc_scatterplot(filepath):
    """
    Create a scatter plot showing expenditure per capita versus population for 
    each state in the United States from 2016 to 2020.
    """

    # Load data for each year
    data = {}
    for year in range(2016, 2021):
        df = pd.read_csv(filepath + f"{year}_per_capita_analysis.csv")
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
    fig.add_shape(type="line",
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
    
    # Show the plot
    fig.show()


def expenditurepc_vs_fundingpc_scatterplot(filepath):
    """
    Create a scatter plot showing expenditure per capita versus funding per 
    capita for each state in the United States from 2016 to 2020.
    """

    dfs = []

    # Load data for each year
    for year in range(2016, 2021):
        # Read in the per capita analysis csv for the year
        df = pd.read_csv(filepath + f"{year}_per_capita_analysis.csv")
        df = df.drop(df[df["State"] == "United States"].index)
        df["Year"] = year
        dfs.append(df)

    df = pd.concat(dfs)
    df_pop = pd.read_csv('us_cleaned_population.csv')
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
    fig.show()