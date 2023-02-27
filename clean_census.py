import pandas as pd

def clean_census(input_filename, output_filename):
    """
    Cleans census data and retains necessarsy columns

    Inputs:
        input_filename (str): name of the file with the original data
        output_filename (str): name of the file with the cleaned data
    
    Returns:
        output_file (csv): file with cleaned census data
    """

    df = pd.read_csv(input_filename)
    df['Description'] = df['Description'].str.strip()

    # Retains only columns that combines state and local government finances
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Retains only required rows
    df = df[df["Description"].isin(["Expenditure1", "Assistance and subsidies", 
    "Public welfare"])]

    # Transposes dataframe and rename columns
    df = df.transpose()
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df.reset_index(inplace=True)
    df.rename(columns = {'Expenditure1':'State and Local Government Total Expenditure',
     "index" : "State", "Assistance and subsidies":"Expenditure on Assistance and Subsidies",
      "Public welfare":"Expenditure on Public Welfare"}, inplace = True)

    # Removes first row with total US state and local government expenditure
    df.drop(index=df.index[0], axis=0, inplace=True)
    output_file = df.to_csv(output_filename, index = False)

    return output_file


def combine_dataframes_by_state(main_df, df_lst):
    """
    Recursively concatenates multiple panda dataframes (with "State" 
    as the index) with only the required columns

    Inputs:
        df_lst (lst of tuples): (df, [cols to extract])
        
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