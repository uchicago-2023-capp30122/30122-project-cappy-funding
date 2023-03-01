import pandas as pd

STATE_NAMES = ["Alaska", "Alabama", "Arkansas", "Arizona", "California",
"Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
"Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana",
"Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi",
"Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey",
"New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
"Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia",
"Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

STATE_NAMES_AND_UNITED_STATES = STATE_NAMES[:]
STATE_NAMES_AND_UNITED_STATES.append("United States")

us_state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

US_STATE_CODES = dict(map(reversed, us_state_abbreviations.items()))

NAICS_SECTOR_CODES = {
    "Agriculture, Forestry, Fishing and Hunting" : ("11",),
    "Mining, Quarrying, and Oil and Gas Extraction" : ("21",),
    "Utilities" : ("22",),
    "Construction" : ("23",),
    "Manufacturing" : ("31", "32", "33",),
    "Wholesale Trade" : ("42",),
    "Retail Trade" : ("44", "45",),
    "Transportation and Warehousing" : ("48", "49",),
    "Information" : ("51",),
    "Finance and Insurance" : ("52",),
    "Real Estate and Rental and Leasing" : ("53",),
    "Professional, Scientific, and Technical Services" : ("54",),
    "Administrative and Support and Waste Management and Remediation Services" : ("56",),
    "Educational Services" : ("61",),
    "Health Care and Social Assistance" : ("62",),
    "Arts, Entertainment, and Recreation" : ("71",),
    "Accommodation and Food Services" : ("72",),
    "Other Services (except Public Administration)" : ("81",),
    "Public Administration (not covered in economic census)" : ("92",)
}


def combine_dataframes_by_state(main_df, df_lst):
    """
    Recursively concatenates multiple panda dataframes (with "State" 
    as the index) with only the required columns
    Inputs:
        df_lst (lst of tuples): (df, [cols to extract])
        ### If extracting all columns, [cols to extract] should be an
        empty list ###
        
    Returns:
        final_df (pandas series): concatenated pandas dataframes
    """
    if len(df_lst) == 0:
        return main_df
    
    other_df, col_lst = df_lst.pop()

    if col_lst != []:
        new_df = main_df.merge(other_df[col_lst], on="State")
    else:
        new_df = main_df.merge(other_df, on="State")
    
    return combine_dataframes_by_state(new_df, df_lst)