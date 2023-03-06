import sys

from ..data.raw_data import scrape_funds
from ..clean_and_analyze import analyze_data

YEARS = ["2016", "2017", "2018", "2019", "2020"]
CLEAN_DATA_DIR = "..data/clean_data/"
RAW_DATA_DIR = "..data/raw_data/"

def run_api_download_and_clean():
    """
    Runs the API download and data cleaning functions
    """
    # Part that runs API download
    scrape_funds.total_funding()
    scrape_funds.data_year()

    # Part that runs data cleaning and analysis
    analyze_data.clean_and_analyze_all(YEARS, RAW_DATA_DIR, CLEAN_DATA_DIR)


def run_visualization():
    """
    Runs the data vizualisation functions
    """
    pass

def main():
    """
    """
    run_api_download_and_clean()
    run_visualization()

if __name__ == "__main__":
    main()