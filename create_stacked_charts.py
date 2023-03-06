import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def create_stacked_area_chart(csv_file):
    """
    Create a stacked area chart showing federal funding percentage by NAICS 
    category over time (2016-2020).
    """

    df = pd.read_csv(csv_file, index_col=0)

    # Sort the DataFrame in descending order based on the sum of each row
    df = df.loc[df.sum(axis=1).sort_values(ascending=True).index]

    # Reverse the order of the rows
    df = df.iloc[::-1]

    # Plot stacked area chart with the colors and set y-axis limits
    df.T.plot(kind='area', 
            stacked=True, 
            figsize=(12,8), 
            color=px.colors.qualitative.Alphabet[:19][::-1], 
            ylim=(0, 100)
            )

    # Add title and labels
    plt.title(f'Federal Funding Percentage by NAICS Category Over Time (2016-2020) - {csv_file}', fontsize=20)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Funding Percentage', fontsize=14)
    plt.legend(title='NAICS Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show chart
    plt.show()

# To call: 
# create_stacked_area_chart('us_funding_time_series.csv')
# create_stacked_area_chart('us_expenditure_time_series.csv')



def create_stacked_bar_chart(csv_file, category_column):
    """
    Create a stacked bar chart using Plotly Express to show the top 10 NAICS 
    categories that received federal funding between 2016 and 2020. 
    The chart displays the funding percentage for each category in each year.
    """

    df = pd.read_csv(csv_file)

    # Calculate the mean funding percentage for each category over the 5-year period
    df_mean = df.loc[:, '2016':'2020'].mean(axis=1)
    df_mean.index = df[category_column]
    df_mean = df_mean.reset_index(name='Mean Percentage')

    # Sort the data by the mean funding percentage and select only the top 10 categories
    df_top_10 = df_mean.sort_values(by='Mean Percentage', ascending=False).head(10)
    category_order = df_top_10[category_column].tolist()

    # Filter the original dataframe to include only the top 10 categories
    df_filtered = df[df[category_column].isin(category_order)]

    # Melt the data so that each row represents a single observation
    df_melt = pd.melt(df_filtered, id_vars=[category_column], var_name='Year', value_name='Expenditure Percentage')

    # Create the stacked bar chart using Plotly Express and set the category order
    fig = px.bar(df_melt, 
                x='Year', 
                y='Expenditure Percentage', 
                color=category_column, 
                barmode='stack', 
                category_orders={category_column: category_order}
                )

    # Update the figure information
    fig.update_xaxes(type='category')
    fig.update_layout(title=f'Top 10 {category_column} receiving Federal Funding by Year (2016-2020)')

    # Show chart
    fig.show()

# To call: 
# create_stacked_bar_chart('us_expenditure_time_series.csv', 'Category')
# create_stacked_bar_chart('us_funding_time_series.csv', 'NAICS Category')