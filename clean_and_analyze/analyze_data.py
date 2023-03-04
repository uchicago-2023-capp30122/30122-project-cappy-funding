import pandas as pd
from clean_census import clean_census_expenditure, clean_census_population, clean_census_poverty
from clean_funding import clean_funding
from utils_clean_and_analyze import NAICS_SECTOR_LST, CleanedData

YEARS = ["2016", "2017", "2018", "2019", "2020"]

CLEAN_DATA_DIR = "../data/clean_data/"
RAW_DATA_DIR = "../data/raw_data/"

def clean_and_analyze_all(year_lst):
    """
    ###
    """
    cleaned_df_dct = analyze_expenditure_and_funding(year_lst)
    create_funding_time_series_df(year_lst, cleaned_df_dct)
    create_expenditure_time_series_df(year_lst, cleaned_df_dct)
    combine_multiple_years(year_lst, cleaned_df_dct)


def analyze_expenditure_and_funding(years):
    """
    ###

    Inputs:
        years (lst of str)

    Returns:
        cleaned_and_combined (dct)
    """
    # Creates and outputs population and poverty data
    poverty_df = clean_census_poverty(pd.read_csv(RAW_DATA_DIR + "us_poverty_by_state.csv"))
    population_df = clean_census_population(pd.read_csv(RAW_DATA_DIR + "us_census_population.csv")) 

    poverty_df.to_csv(CLEAN_DATA_DIR + "us_poverty_cleaned.csv")
    population_df.to_csv(CLEAN_DATA_DIR + "us_population_cleaned.csv")

    # Clean and combines census data and funding data from each year from 2016 to 2020

    cleaned_df_dct = {}

    for year in years:
        expenditure_csv = RAW_DATA_DIR + year + "_us_state_finances.csv" # "2016_us_state_finances.csv"
        funding_csv = RAW_DATA_DIR + year + "_us_funding.csv" # "2016_us_funding.csv"

        expenditure_df = clean_census_expenditure(pd.read_csv(expenditure_csv))
        funding_df, funding_df_by_state, funding_df_within_state  = clean_funding(pd.read_csv(funding_csv), year)
    
        per_capita_df = pd.DataFrame(columns=["Expenditure per Capita (in thousands)", "Funding received per Capita (in thousands)"])
        per_capita_df["Expenditure per Capita (in thousands)"] = expenditure_df["State Expenditure (in thousands)"] / population_df["Population"]
        per_capita_df["Funding received per Capita (in thousands)"] = funding_df_by_state["Total Funding Received"] / population_df["Population"]

        cleaned_df_dct[year] = CleanedData(expenditure_df, per_capita_df, funding_df, funding_df_by_state, funding_df_within_state)

        # Outputs files into directory
        funding_df_by_state.to_csv(CLEAN_DATA_DIR + year + "_cleaned_funding_by_state.csv")
        funding_df_within_state.to_csv(CLEAN_DATA_DIR + year + "_cleaned_funding_within_state.csv")
        funding_df.to_csv(CLEAN_DATA_DIR + year + "_cleaned_funding_full.csv")
        expenditure_df.to_csv(CLEAN_DATA_DIR + year + "_cleaned_expenditure.csv")
        per_capita_df.to_csv(CLEAN_DATA_DIR + year + "_per_capita_analysis.csv")

    return cleaned_df_dct


def create_funding_time_series_df(year_lst, clean_df_dct):
    """
    ###
    """
    funding_time_series = pd.DataFrame(columns = year_lst)
    for year in year_lst:
        funding_df = clean_df_dct.get(year).funding_df
        us_row_only = funding_df.loc[funding_df.index == "United States"]
        us_row_only = us_row_only[NAICS_SECTOR_LST]
        us_row_only = us_row_only.transpose()
        us_row_only.rename(columns = {'United States':'Amount'}, inplace = True)
        funding_time_series[year] = (us_row_only["Amount"] / us_row_only["Amount"].sum()) * 100

    funding_time_series.index.names = ["NAICS Category"]

    # Outputs file into directory
    funding_time_series.to_csv(CLEAN_DATA_DIR + "us_funding_time_series.csv")

    return funding_time_series


def create_expenditure_time_series_df(year_lst, clean_df_dct):
    """
    ###
    """
    expenditure_time_series = pd.DataFrame(columns = year_lst)
    for year in year_lst:
        expenditure_df = clean_df_dct.get(year).expenditure_df
        us_row_only = expenditure_df.loc[expenditure_df.index == "United States"]
        sum = int(us_row_only.loc[us_row_only.index == "United States", "State Expenditure (in thousands)"])
        us_row_only = us_row_only[["Utilities", "Health and Social Services Expenditure", "Education Related Expenditure", "Public Administration Expenditure", "Transportation Expenditure"]]
        us_row_only = us_row_only.transpose()
        us_row_only.rename(columns = {'United States':'Amount'}, inplace = True)
        us_row_only["Sum"] = sum
        expenditure_time_series[year] = (us_row_only["Amount"] / us_row_only["Sum"]) * 100
    
    expenditure_time_series.index.names = ["Category"]

    # Outputs file into directory
    expenditure_time_series.to_csv(CLEAN_DATA_DIR + "us_expenditure_time_series.csv")
            
    return expenditure_time_series


def combine_multiple_years(year_lst, clean_df_dct):
    """
    ###
    """
    funding_df_lst = []
    for year in year_lst:
        funding_df_lst.append(clean_df_dct.get(year).funding_df_by_state)

    combined_df = pd.concat(funding_df_lst)
    combined_df = combined_df[combined_df.index != "United States"]
    combined_df = combined_df.sort_values(["State", "Year"])

    # Outputs file into directory
    combined_df.to_csv(CLEAN_DATA_DIR + "all_years_funding_by_state.csv")

    return combined_df