import pandas as pd
from .utils_clean_and_analyze import STATE_NAMES_AND_UNITED_STATES, US_STATE_CODES, NAICS_SECTOR_CODES


def clean_funding(raw_funding_df, year):
    """
    ###
    """
    raw_funding_df["code"] = raw_funding_df["code"].astype(str)

    # Creates structure for funding dataframe
    naics_sector_lst = [k for k in NAICS_SECTOR_CODES.keys()]
    funding_df = pd.DataFrame(STATE_NAMES_AND_UNITED_STATES, columns=["State"])
    funding_df = pd.concat([funding_df,pd.DataFrame(columns = naics_sector_lst)])
    
    funding_df_within_state = pd.DataFrame(STATE_NAMES_AND_UNITED_STATES, columns=["State"]) # Within State
    funding_df_by_state = pd.DataFrame(STATE_NAMES_AND_UNITED_STATES, columns=["State"]) # By State

    funding_df_lst = [funding_df, funding_df_within_state, funding_df_by_state]

    # Calculates funding for each category in each state and inputs values into funding_df
    for state_code, state in US_STATE_CODES.items():
        for sector, naics_code_tuple in NAICS_SECTOR_CODES.items():
            if len(naics_code_tuple) == 1:
                subset_df = raw_funding_df[(raw_funding_df["code"].apply(lambda x : x.startswith(naics_code_tuple[0]))) & (raw_funding_df["State"] == state_code) & (raw_funding_df["amount"] >= 0)]
                sum_val = subset_df["amount"].sum() / 1000
            else:
                sum_val = 0
                for naics_code in naics_code_tuple:
                    subset_df = raw_funding_df[(raw_funding_df["code"].apply(lambda x : x.startswith(naics_code))) & (raw_funding_df["State"] == state_code) & (raw_funding_df["amount"] >= 0)]
                    sum_val += subset_df["amount"].sum() / 1000
            
            funding_df.loc[funding_df["State"] == state, sector] = int(sum_val)

    required_col_names = [col for col in funding_df.columns[1:]]

    # Calculates total funding across categories for each state
    for df in funding_df_lst:
        df["Total Funding Received"] = funding_df[required_col_names].sum(axis=1)

    for col in required_col_names:
        #Calculates total funding for each category at the national level
        funding_df.loc[funding_df["State"] == "United States", col] = funding_df[col].sum()

        # Calculates funding for each state as a share of US by category
        funding_df_by_state[col] = funding_df.apply(lambda x : (x[col] / funding_df.loc[funding_df["State"] == "United States", col]) * 100, axis = 1)

        # Calculates funding for each category as a share of the total funding received by a state
        funding_df_without_us = funding_df.iloc[0:len(funding_df)-1]
        funding_df_within_state[col] = (funding_df_without_us[col] / funding_df_without_us["Total Funding Received"]) * 100
    
    for df in funding_df_lst:
        df["Year"] = year
        df.set_index("State", inplace=True)

    funding_df = funding_df[[list(funding_df.columns)[-1]] + list(funding_df.columns)[:-1]]
    funding_df_within_state = funding_df_within_state[[list(funding_df_within_state.columns)[-1]] + list(funding_df_within_state.columns)[:-1]]
    funding_df_by_state = funding_df_by_state[[list(funding_df_by_state.columns)[-1]] + list(funding_df_by_state.columns)[:-1]]


    return funding_df, funding_df_by_state, funding_df_within_state
