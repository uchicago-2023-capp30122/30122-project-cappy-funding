### All the functions below were written by Foo Suon Chuang (Bryan)

import pandas as pd
from .utils_clean_and_analyze import STATE_NAMES_AND_UNITED_STATES

def clean_census_expenditure(df):
    """
    Cleans and analyzes a raw file of the government expenditure for one year

    Inputs:
        df (a pandas series): government expenditure by state
    
    Returns:
        df (a pandas series): a cleaned and analyzed expenditure dataframe
    """

    df['Description'] = df['Description'].str.strip()
    df.rename(columns = {'United States Total':'United States'}, inplace = True)

    # Retains only columns of state and local combined government expenditure
    df = df[["Description"] + STATE_NAMES_AND_UNITED_STATES]

    # Drops rows relating to state revenue sources
    df.drop(df.index[0:66], inplace=True)

    # Retains only specific expenditure categories
    social = ["Public welfare", "Hospitals", "Health", 
    "Employment security administration", "Veterans' services"]
    
    educ = ["Education", "Libraries"]
    govt = ["Financial administration", "Judicial and legal", 
    "General public buildings", "Other governmental administration"]
    transport = ["Highways", "Air transportation (airports)", 
    "Parking facilities", "Sea and inland port facilities"]
    others = ["Utility expenditure", "Expenditure1"]

    df = df[df["Description"].isin(social + educ + govt + transport + others)]

    # Transposes dataframe and sets new column names
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    df.reset_index(inplace=True)
    df.rename(columns = {'Expenditure1':'State Expenditure (in thousands)', 
    "index" : "State", "Utility expenditure" : "Utilities"}, inplace = True)

    # Converts specific columns in to integers
    for col in [col for col in df.columns]:
        if col != "State":
            df[col] = df[col].str.replace(',','')
            df[col] = df[col].astype(int)
    
    # Sums individual expenditure categories into four main categories
    df["Health and Social Services Expenditure"] = df[social].sum(axis=1)
    df["Education Related Expenditure"] = df[educ].sum(axis=1)
    df["Public Administration Expenditure"] = df[educ].sum(axis=1)
    df["Transportation Expenditure"] = df[transport].sum(axis=1)
    df.drop(columns = social + educ + govt + transport, inplace=True)

    required_col_names = [col for col in df.columns[1:]]

    for col in required_col_names:

        # Calculates state expenditure in one cateogry as a proportion
        # of total US expenditure for this category
        if col == "State Expenditure (in thousands)":
            df["State Total as % of US Total"] = \
                df.apply(lambda x : (x[col] / int(df.loc[df["State"] ==
                    "United States", col])) * 100, axis = 1)

        # Calculates the state expenditure in one category as a proportion
        # of total state expenditure across all cateogries
        else:
            df[col + " (State as % of US)"] = \
                df.apply(lambda x : (x[col] / int(df.loc[df["State"] ==
                    "United States", col])) * 100, axis = 1)

            df[col + " (% of Total Expenditure)"] = (df[col] /
            df["State Expenditure (in thousands)"] * 100)

    # Sets "State" column as index of dataframe
    df.set_index(["State"], inplace = True)

    return df


def clean_census_population(pop_df):
    """
    Cleans and analyzes a raw file of the country's population size

    Inputs:
        pop_df (a pandas series): population size by state
    
    Returns:
        pop_df (a pandas series): a cleaned and analyzed population dataframe
    """

    # Retains only the first two columns of the dataframe
    pop_df = pop_df.iloc[:,0:2]
    pop_df.columns = ["State", "Population"]
    pop_df['State'] = pop_df['State'].str.strip()

    # Retains only rows for states and country total (drops territories)
    pop_df = pop_df[pop_df["State"].isin(STATE_NAMES_AND_UNITED_STATES)]

    # Converts row values into integers
    pop_df["Population"] = pop_df["Population"].str.replace(',','')
    pop_df["Population"] = pop_df["Population"].astype(int)

    pop_df.set_index("State", inplace=True)

    return pop_df


def clean_census_poverty(poverty_df):
    """
    Cleans and analyzes a raw file of the country's poverty rate

    Inputs:
        poverty_df (a pandas series): poverty rate by state
    
    Returns:
        poverty_df (a pandas series): a cleaned and analyzed poverty rate dataframe
    """
    # Retains only the first two columns of the dataframe
    poverty_df = poverty_df.iloc[:,0:2]
    poverty_df.columns = ["State", "3-Year Average Poverty Rate (2018-2020)"]
    poverty_df['State'] = poverty_df['State'].str.strip()

    # Retains only rows for states and country total (drops territories)
    poverty_df = poverty_df[poverty_df["State"].isin(STATE_NAMES_AND_UNITED_STATES)]

    poverty_df.set_index("State", inplace=True)

    return poverty_df
