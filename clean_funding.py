import pandas as pd
from utils_clean_and_analyze import STATE_NAMES, STATE_NAMES_AND_UNITED_STATES, US_STATE_CODES, NAICS_SECTOR_CODES


def clean_funding(raw_funding_df):
    """
    ###
    """
    # Creates new dataframe for cleaned data
    naics_sector_lst = [k for k in NAICS_SECTOR_CODES.keys()]
    funding_df = pd.DataFrame(STATE_NAMES_AND_UNITED_STATES, columns=["State"])
    funding_df = pd.concat([funding_df,pd.DataFrame(columns = naics_sector_lst)])

    # Sums funding by category in each state and inputs values into funding_df
    for state_code, state in US_STATE_CODES.items():
        for sector, naics_code_tuple in NAICS_SECTOR_CODES.items():
            if len(naics_code_tuple) == 1:
                subset_df = raw_funding_df[(raw_funding_df["code"].apply(lambda x : x.startswith(naics_code_tuple[0]))) & (raw_funding_df["State"] == state_code)]
                sum_val = subset_df["amount"].sum()
            else:
                sum_val = 0
                for naics_code in naics_code_tuple:
                    subset_df = raw_funding_df[(raw_funding_df["code"].apply(lambda x : x.startswith(naics_code))) & (raw_funding_df["State"] == state_code)]
                    sum_val += subset_df["amount"].sum()
            
            funding_df.loc[funding_df["State"] == state, sector] = int(sum_val)
    
    return funding_df