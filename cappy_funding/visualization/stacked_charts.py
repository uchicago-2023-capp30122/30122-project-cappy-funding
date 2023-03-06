import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def create_stacked_area_chart(filepath):
    """
    Create a stacked area chart showing federal funding percentage by NAICS 
    category over time (2016-2020).
    """

    # Read CSV file
    df = pd.read_csv(filepath + 'us_funding_time_series.csv', index_col=0)

    # Sort the DataFrame in descending order based on the sum of each row
    df = df.loc[df.sum(axis=1).sort_values(ascending=True).index]

    # Reverse the order of the rows
    df = df.iloc[::-1]

    # Generate a list of 19 pretty and distinguishable colors
    colors = px.colors.qualitative.Alphabet[:19][::-1]

    # Plot stacked area chart with the colors and set y-axis limits
    fig, ax = plt.subplots(figsize=(12,8))
    df.T.plot(kind='area', stacked=True, ax=ax, color=colors, ylim=(0, 100))

    # Add title and labels and set margins
    ax.set_title('Federal Funding Percentage by NAICS Category Over Time (2016-2020)', fontsize=20)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Funding Percentage', fontsize=14)
    ax.legend(title='NAICS Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.margins(0.05)

    # Save chart to file
    fig.savefig('data/clean_data/stacked_area_chart.png', bbox_inches='tight')

    # Return chart
    return fig


def top_10_categories_stacked_bar_chart(filepath):
    """
    Create a stacked bar chart using Plotly Express to show the top 10 NAICS 
    categories that received federal funding between 2016 and 2020. 
    The chart displays the funding percentage for each category in each year.
    """

    df = pd.read_csv(filepath + 'us_funding_time_series.csv')

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
    fig = px.bar(df_melt, 
                x='Year', 
                y='Funding Percentage', 
                color='NAICS Category', 
                barmode='stack', 
                category_orders={'NAICS Category': category_order}
                )

    # Update the figure information
    fig.update_xaxes(type='category')
    fig.update_layout(title='Top 10 Categories receiving Federal Funding by Year (2016-2020)')

    # Show chart
    fig.show()

