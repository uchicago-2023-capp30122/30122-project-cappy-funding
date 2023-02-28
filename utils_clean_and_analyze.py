import pandas as pd

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