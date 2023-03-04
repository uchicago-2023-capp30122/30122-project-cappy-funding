import sys

from .fund_data import scrape_funds
from .clean_and_analyze import analyze_data

YEARS = ["2016", "2017", "2018", "2019", "2020"]

def run_download_and_clean():
    """
    Runs the API download and data cleaning functions
    """
    if len(sys.argv) != 1:
        print(
            f"Usage: python3 {sys.argv[0]}"
        )
        sys.exit(1)

    # Part that runs API download

    # Part that runs data cleaning and analysis
    analyze_data.clean_and_analyze_all(YEARS)


def run_visualize():
    """
    Runs the data vizualisation functions
    """
    pass