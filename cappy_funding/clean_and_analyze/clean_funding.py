import pandas as pd
from .utils_clean_and_analyze import STATE_NAMES_AND_UNITED_STATES, \
    US_STATE_CODES, NAICS_SECTOR_CODES


def clean_funding(raw_funding_df, year):
    """
    Cleans and analyzes a raw file of the federal funding received by each state
    across multiple sectors in one year.

    Inputs:
        raw_funding_df (a pandas series): raw file of the federal funding 
            received by each state
    
    Returns:
        funding_df (a pandas series): funding received by each state for each 
            sector in absolute value
        funding_df_by_state (a pandas series): funding received by each state 
            for each sector as a share of the whole country (in %)
        funding_df_within_state (a pandas series): funding received by each
            state for each sector as a share of the total fudning received by
            the state acorss multiple sectors (in %)

    """
    raw_funding_df["code"] = raw_funding_df["code"].astype(str)

    # Creates a main funding dataframe with a "State" column and a row for 
    # each state and also one for the country
    naics_sector_lst = [k for k in NAICS_SECTOR_CODES.keys()]
    funding_df = pd.DataFrame(STATE_NAMES_AND_UNITED_STATES, columns=["State"])

    # Creates additional columns for each sector (according to NAICS categorisation)
    funding_df = pd.concat([funding_df, pd.DataFrame(columns = naics_sector_lst)])
    
    # Creates two other funding dateframes
    funding_df_within_state = pd.DataFrame(STATE_NAMES_AND_UNITED_STATES, 
    columns=["State"])

    funding_df_by_state = pd.DataFrame(STATE_NAMES_AND_UNITED_STATES, 
    columns=["State"])

    # Stores the three dataframes in a list
    funding_df_lst = [funding_df, funding_df_within_state, funding_df_by_state]

    # Sums up the funding amount by sector for each state

    # US_STATE_CODES is a dictionary where the key is the two letter
    # code for a US state, and the value is the name of the state
    for state_code, state in US_STATE_CODES.items():

        # NAICS_SECTOR_CODES is a dictionary where the key is the name of the 
        # sector, and the value is a tuple of integers associated with each sector
        for sector, naics_code_tuple in NAICS_SECTOR_CODES.items():
            
            # Case where there is only one code associated with a given sector
            if len(naics_code_tuple) == 1:
                subset_df = raw_funding_df[(raw_funding_df["code"].apply(lambda x :
                 x.startswith(naics_code_tuple[0]))) & (raw_funding_df["State"] == 
                state_code) & (raw_funding_df["amount"] >= 0)]
                
                sum_val = subset_df["amount"].sum() / 1000

            # Case where there are two or more codes associated with a given sector
            else:
                sum_val = 0

                for naics_code in naics_code_tuple:
                    subset_df = raw_funding_df[(raw_funding_df["code"].apply(lambda x :
                     x.startswith(naics_code))) & (raw_funding_df["State"] == state_code) 
                     & (raw_funding_df["amount"] >= 0)]
                    
                    sum_val += subset_df["amount"].sum() / 1000
            
            # Inputs the funding amount for one sector in one state 
            # to the main funding dataframe
            funding_df.loc[funding_df["State"] == state, sector] = int(sum_val)

    # Saves the current column names as a list for further iteration below
    required_col_names = [col for col in funding_df.columns[1:]]

    # Creates a new column that sums the total funding received for 
    # each state across multiple sectors
    for df in funding_df_lst:
        df["Total Funding Received"] = funding_df[required_col_names].sum(axis=1)

    # Uses the main funding dataframe to conduct further computation
    for col in required_col_names:
    
        #Calculates total funding for each category at the national level
        funding_df.loc[funding_df["State"] == "United States", col] = \
            funding_df[col].sum()

        # For each sector, calculates the funding received by each state 
        # as a share of the whole country (in %)
        funding_df_by_state[col] = funding_df.apply(lambda x : (x[col] /
         funding_df.loc[funding_df["State"] == "United States", col]) * 100, axis = 1)

        # For each state, calculates the funding received by each state for one sector 
        # as a share of the total fudning received by the state acorss multiple sectors
        funding_df_without_us = funding_df.iloc[0:len(funding_df)-1]
        funding_df_within_state[col] = (funding_df_without_us[col] / 
        funding_df_without_us["Total Funding Received"]) * 100
    
    # Creates a new column to indicate the year in which the funding was received
    for df in funding_df_lst:
        df["Year"] = year
        df.set_index("State", inplace=True)

    # Sets "Year" column as the first row after the "State" column
    funding_df = funding_df[[list(funding_df.columns)[-1]]
     + list(funding_df.columns)[:-1]]

    funding_df_within_state = funding_df_within_state[
        [list(funding_df_within_state.columns)[-1]] + 
        list(funding_df_within_state.columns)[:-1]]

    funding_df_by_state = funding_df_by_state[[
        list(funding_df_by_state.columns)[-1]] +
        list(funding_df_by_state.columns)[:-1]]

    return funding_df, funding_df_by_state, funding_df_within_state