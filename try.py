import pandas as pd
data_time = pd.read_csv("us_funding_time_series.csv")
column_list = list(data_time.columns)
for item in data_time['Unnamed: 0']:
    print(item)