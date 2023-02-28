import pandas as pd

STATE_NAMES = ["Alaska", "Alabama", "Arkansas", "Arizona", "California",
"Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia",
"Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana",
"Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi",
"Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey",
"New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
"Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia",
"Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

STATE_NAMES_WITH_UNITED_STATES = STATE_NAMES[:]
STATE_NAMES_WITH_UNITED_STATES.append("United States")


def clean_census_expenditure(input_df):
    """
    ###
    """

    df['Description'] = df['Description'].str.strip()

    # Retains only columns that combines state and local government finances
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Drops rows relating to revenue sources
    df.drop(df.index[0:66], inplace=True)

    social = ["Public welfare", "Hospitals", "Health", "Employment security administration", "Veterans' services"]
    educ = ["Education", "Libraries"]
    govt = ["Financial administration", "Judicial and legal", "General public buildings", "Other governmental administration"]
    transport = ["Highways", "Air transportation (airports)", "Parking facilities", "Sea and inland port facilities"]
    others = ["Utility expenditure", "Expenditure1"]

    # Retains only required rows
    df = df[df["Description"].isin(social + educ + govt + transport + others)]

    # Education (Education + Libraries) - 61
    # Health & Social Services (Public welfare + Hospitals + Health + Security + Employment security administration +  Veterans' services) - 62
    # Government Administration (Financial administration + Judicial and legal + General public buildings + Other governmental administration) - 92
    # Utilities (Utility expenditure) - 22
    # Transportation (Highways, Air transportation (airports), Parking facilities, Sea and inland port facilities) - 48/49

    # Transposes dataframe and rename columns
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    df.reset_index(inplace=True)
    df.rename(columns = {'Expenditure1':'State Expenditure', 
    "index" : "State", "Utility expenditure" : "Utilities"}, inplace = True)

    for col in [col for col in df.columns]:
        if col != "State":
            df[col] = df[col].str.replace(',','')
            df[col] = df[col].astype(int)

    df["Health and Social Services"] = df[social].sum(axis=1)
    df["Education"] = df[educ].sum(axis=1)
    df["Public Administration"] = df[educ].sum(axis=1)
    df["Transportation"] = df[transport].sum(axis=1)
    df.drop(columns = social + educ + govt + transport, inplace=True)

    required_col_names = [col for col in df.columns[1:]]

    for col in [col for col in required_col_names]:
        if col == "State Expenditure":
            col_name = col + " as % of US Expenditure"
        else:
            col_name = col + " (State Expenditure as % of Total US)"

        df[col + " (State Expenditure as % of Total US)"] = \
            df.apply(lambda x : (x[col] / int(df.loc[df["State"] ==
                "United States Total", col])) * 100, axis = 1)
        df[col + " (as % of Total State Expenditure)"] = (df[col] /
        df["State Expenditure"] * 100)

    df.set_index(["State"], inplace = True)

    return df


def clean_census_population(input_df):
    """
    ###
    """
    pop_df = pop_df.iloc[:,0:2]
    pop_df.columns = ["State", "2020 Census Population"]
    pop_df['State'] = pop_df['State'].str.strip()
    pop_df = pop_df[pop_df["State"].isin(STATE_NAMES_WITH_UNITED_STATES)]
    pop_df.set_index("State", inplace=True)

    return pop_df


def clean_census_poverty(input_df):
    """
    ###
    """
    poverty_df = poverty_df.iloc[:,0:2]
    poverty_df.columns = ["State", "3-Year Average Poverty Rate (2018-2020)"]
    poverty_df['State'] = poverty_df['State'].str.strip()
    poverty_df = poverty_df[poverty_df["State"].isin(STATE_NAMES_WITH_UNITED_STATES)]
    poverty_df.set_index("State", inplace=True)

    return poverty_df


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