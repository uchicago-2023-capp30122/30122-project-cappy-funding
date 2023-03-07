import pandas as pd
from collections import namedtuple
from .clean_census import clean_census_expenditure, \
    clean_census_population, clean_census_poverty
from .clean_funding import clean_funding
from .utils_clean_and_analyze import NAICS_SECTOR_LST

# Stops pandas from printing warnings in the terminal
pd.options.mode.chained_assignment = None

# Namedtupled to store multiple cleaned dataframes
# (used in analyze_expenditure_and_funding function)
CleanedData = namedtuple("CleanedData", ["expenditure_df", "per_capita_df",
 "funding_df_absolute", "funding_df_by_state", "funding_df_within_state"])

def clean_and_analyze_all(starting_year, ending_year, from_filepath, to_filepath):
    """
    Calls on all the helper functions below to clean, analyze and output
    the required files as multiple csv.
    
    Inputs:
        starting_year (str): lower bound of year range to clean data
        ending_year (str): upper bound of year range to clean data
        from_filepath (str): filepath to retrieve raw data files
        to_filepath (str): filepath to store cleaned data files
    
    Returns (none)
    """
    if starting_year == "":
        starting_year = "2016"
    
    if ending_year == "":
        ending_year = "2020"
    
    year_lst = []
    for year in range(int(starting_year), int(ending_year) + 1):
        year_lst.append(str(year))

    cleaned_df_dct = analyze_expenditure_and_funding(year_lst, 
    from_filepath, to_filepath)
    create_funding_time_series_df(year_lst, cleaned_df_dct, to_filepath)
    create_expenditure_time_series_df(year_lst, cleaned_df_dct, to_filepath)
    combine_multiple_years(year_lst, cleaned_df_dct, to_filepath)

    print("\nAll datasets have been cleaned and analysed and saved to /data/clean_data/")


def analyze_expenditure_and_funding(year_lst, from_filepath, to_filepath):
    """
    Cleans poverty csv, population csv, as well as yearly state expenditure 
    csv and yearly funding csv. Computes yearly per_capita expenditure and 
    funding. Output these files as multiple cleaned csv.

    Inputs:
        year_lst (lst of str): list of years to clean
        from_filepath (str): filepath to retrieve raw data files
        to_filepath (str): filepath to store cleaned data files

    Returns:
        cleaned_df_dct (dct): a dictionary that stores each year's cleaned datasets
            key (str): one year
            value (tuple of pandas series): a named tuple that stores
            five datasets
    """
    # Cleans and outputs poverty and population csv
    poverty_df = clean_census_poverty(pd.read_csv(from_filepath 
    + "us_poverty_by_state.csv"))
    poverty_df.to_csv(to_filepath + "us_poverty_cleaned.csv")

    population_df = clean_census_population(pd.read_csv(from_filepath
    + "us_census_population.csv")) 
    population_df.to_csv(to_filepath + "us_population_cleaned.csv")

    # Cleans and outputs datasets for each year
    cleaned_df_dct = {}
    for year in year_lst:

        # Retrieves expenditure and funding csv from raw_data/ directory
        expenditure_csv = from_filepath + year + "_us_state_finances.csv"
        funding_csv = from_filepath + year + "_us_funding.csv" 

        # Cleans expenditure and funding dataset for one year
        expenditure_df = clean_census_expenditure(pd.read_csv(expenditure_csv))
        funding_df_absolute, funding_df_by_state, funding_df_within_state \
             = clean_funding(pd.read_csv(funding_csv), year)
        
        # Calculates expenditure and funding received per capita for one year
        per_capita_df = pd.DataFrame(columns=["Expenditure per Capita (in thousands)",
         "Funding received per Capita (in thousands)"])
    
        per_capita_df["Expenditure per Capita (in thousands)"] = \
            expenditure_df["State Expenditure (in thousands)"] / population_df["Population"]

        per_capita_df["Funding received per Capita (in thousands)"] = \
            funding_df_by_state["Total Funding Received"] / population_df["Population"]

        # Sets dictionary key to the year and stores five datasets 
        # dictionary value in a namedtuple
        cleaned_df_dct[year] = CleanedData(expenditure_df, per_capita_df, 
        funding_df_absolute, funding_df_by_state, funding_df_within_state)

        # Outputs files into the clean_data/ directory
        funding_df_by_state.to_csv(to_filepath + year + 
        "_cleaned_funding_by_state.csv")
        funding_df_within_state.to_csv(to_filepath + year + 
        "_cleaned_funding_within_state.csv")
        funding_df_absolute.to_csv(to_filepath + year + 
        "_cleaned_funding_absolute.csv")
        expenditure_df.to_csv(to_filepath + year + 
        "_cleaned_expenditure.csv")
        per_capita_df.to_csv(to_filepath + year + 
        "_per_capita_analysis.csv")

        # Print statement to let user know that one year of data has been cleaned
        print(year + " data has been cleaned and analyzed")

    return cleaned_df_dct


def create_funding_time_series_df(year_lst, clean_df_dct, to_filepath):
    """

    Creates and outputs a timeseries csv that shows the percentage of funding
    awarded for each category at the national level across smultiple years. 
    Outputs the timeseries as a csv.
    
    Inputs:
        year_lst (lst of str): list of years to construct time series
        cleaned_df_dct (dct): a dictionary that stores each year's cleaned datasets
            key (str): one year
            value (tuple): a named tuple that stores five datasets
        to_filepath (str): filepath to store cleaned data files
    
    Returns:
        funding_time_series (pandas series): timeseries dataframe
    """
    # Creates new dataset with one year as one column
    funding_time_series = pd.DataFrame(columns = year_lst)

    for year in year_lst:

        # Retrieves funding dataset for one year
        funding_df_absolute = clean_df_dct.get(year).funding_df_absolute

        # Obtains total funding for the whole country in one year
        us_row_only = funding_df_absolute.loc[funding_df_absolute.index\
             == "United States"]
        us_row_only = us_row_only[NAICS_SECTOR_LST]

        # Tranposes dataset such that the rows are the categories and the 
        # column is the funding amount for each cateogry
        us_row_only = us_row_only.transpose()
        us_row_only.rename(columns = {'United States':'Amount'}, inplace = True)

        # Computes the percentage for each category out of the total funding
        funding_time_series[year] = (us_row_only["Amount"] / 
        us_row_only["Amount"].sum()) * 100

    funding_time_series.index.names = ["NAICS Category"]

    # Outputs file into the clean_data/ directory
    funding_time_series.to_csv(to_filepath + "us_funding_time_series.csv")

    # Print statement to let user know that time series data has been created
    print("Funding time series data data has been created")

    return funding_time_series


def create_expenditure_time_series_df(year_lst, clean_df_dct, to_filepath):
    """
    Creates and outputs a timeseries csv that shows the percentage of 
    expenditure for each category at the national level across multiple years.
    Outputs the timeseries as a csv.

    Inputs:
        year_lst (lst of str): list of years to construct time series
        cleaned_df_dct (dct): a dictionary that stores each year's cleaned datasets
            key (str): one year
            value (tuple): a named tuple that stores five datasets
        to_filepath (str): filepath to store cleaned data files
    
    Returns:
        expenditure_time_series (pandas series): timeseries dataframe
    """
    # Creates new dataset with one year as one column
    expenditure_time_series = pd.DataFrame(columns = year_lst)

    for year in year_lst:

        # Retrieves expenditure dataset for one year
        expenditure_df = clean_df_dct.get(year).expenditure_df

        # Obtains total expenditure for the whole country in one year
        us_row_only = expenditure_df.loc[expenditure_df.index == "United States"]
        sum = int(us_row_only.loc[us_row_only.index == "United States", 
        "State Expenditure (in thousands)"])

        # Retains only the five main expenditure categories
        us_row_only = us_row_only[["Utilities",
        "Health and Social Services Expenditure", "Education Related Expenditure",
        "Public Administration Expenditure", "Transportation Expenditure"]]

        # Tranposes dataset such that the rows are the categories and the 
        # column is the amount for each cateogry
        us_row_only = us_row_only.transpose()
        us_row_only.rename(columns = {'United States':'Amount'}, inplace = True)

        # Creates column with each row as the total expenditure
        us_row_only["Sum"] = sum

        # Computes the percentage for each category out of the total expenditure
        expenditure_time_series[year] = (us_row_only["Amount"] / 
        us_row_only["Sum"]) * 100
    
    expenditure_time_series.index.names = ["Category"]

    # Outputs file into the clean_data/ directory
    expenditure_time_series.to_csv(to_filepath + "us_expenditure_time_series.csv")

    # Print statement to let user know that time series data has been created
    print("Expenditure time series data data has been created")
            
    return expenditure_time_series


def combine_multiple_years(year_lst, clean_df_dct, to_filepath):
    """
    Concatenates multiple funding_df_by_state pandas series into one
    pandas series and sorts the new concatenated dataframe. Outputs the
    concatenated dataframe as a csv.

    Inputs:
        year_lst (lst of str): list of years to construct time series
        cleaned_df_dct (dct): a dictionary that stores each year's cleaned datasets
            key (str): one year
            value (tuple): a named tuple that stores five datasets
        to_filepath (str): filepath to store cleaned data files
    
    Returns:
        expenditure_time_series (pandas series): concatenated dataframe
    """
    # Creates a list that stores funding_df_by_state over five years
    funding_df_lst = []
    for year in year_lst:
        funding_df_lst.append(clean_df_dct.get(year).funding_df_by_state)

    # Concatenates the five datasets into one
    combined_df = pd.concat(funding_df_lst)

    # Retains only rows that store state-level information
    combined_df = combined_df[combined_df.index != "United States"]

    # Sorts the dataset by state (alphabetical order) and year (numerical order)
    combined_df = combined_df.sort_values(["State", "Year"])

    # Outputs file into the clean_data/ directory
    combined_df.to_csv(to_filepath + "all_years_funding_by_state.csv")

    # Print statement to let user know that time series data has been created
    print("Funding by state (all years) data data has been created")

    return combined_df