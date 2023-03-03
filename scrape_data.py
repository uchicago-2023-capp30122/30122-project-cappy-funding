import pandas as pd
import pathlib

filename = pathlib.Path(__file__).parent / "data/database.csv"
database = pd.read_csv(filename)

database = database[["Grantmaker State", "Total Giving", "Amount Funded", "Grant Count"]]

database[["BorrowerName", "BorrowerCity"]] = database[["BorrowerName", "BorrowerCity"]].applymap(lambda x: x.strip().lower())

