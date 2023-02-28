import pandas as pd
from clean_census import clean_census_expenditure, clean_census_population, clean_census_poverty
from clean_funding import clean_funding
from utils_clean_and_analyze import combine_dataframes_by_state

YEARS = ["2016", "2017", "2018", "2019", "2020"]

def clean_and_combine(years):
    """
    ###

    Inputs:
        years (lst of str)

    Returns:
        cleaned_and_combined (dct)
    """

    # Clean poverty data
    poverty_df = clean_census_poverty(pd.read_csv("us_poverty_by_state.csv"))

    # Clean population data
    pop_df = clean_census_population(pd.read_csv("us_census_population.csv"))

    # Clean and combines census data and funding data from each year from 2016 to 2020
    expenditure_file_name = "_us_state_finances.csv"
    funding_file_name = "_us_funding.csv"

    cleaned_and_combined = {}

    for year in years:
        expenditure_csv = year + expenditure_file_name # "2016_us_state_finances.csv"
        funding_csv = year + funding_file_name # "2016_us_funding.csv"

        expenditure_df = pd.read_csv(expenditure_csv)
        funding_df = pd.read_csv(funding_csv)

        if year == "2020":
            cleaned_and_combined[year] = combine_dataframes_by_state(expenditure_df, [(funding_df, []), (pop_df, []), (poverty_df, [])])

        else:
            cleaned_and_combined[year] = combine_dataframes_by_state(expenditure_df, [(funding_df, []), (pop_df, [])])
    
    return cleaned_and_combined