import sys
from .data.raw_data import scrape_funds
from .clean_and_analyze import analyze_data
from .visualization import scatterplots, stacked_charts, word_cloud, graph

YEARS = ["2016", "2017", "2018", "2019", "2020"]
CLEAN_DATA_DIR = "./cappy_funding/data/clean_data/"
RAW_DATA_DIR = "./cappy_funding/data/raw_data/"

def run_api_download(start_year, end_year):
    """
    Runs the API download and data cleaning functions
    """
    print("Downloading total federal funding by state file...\n")
    scrape_funds.total_funding()
    
    scrape_funds.data_year(start_year, end_year)
    print("\nAll years downloaded from USA Spending API...")


def run_data_clean_and_analyze():
    """
    Runs the data cleaning and analysis functions
    """
    analyze_data.clean_and_analyze_all(YEARS, RAW_DATA_DIR, CLEAN_DATA_DIR)


def run_visualization():
    """
    Runs the data vizualisation functions
    """
    import visualization.graph


def run():
    """
    """
    print("\nWelcome to Cappy Funding!")
    print("To use the interface, please input one of the following 4 options into command line:")

    user_input = input(
        "\n1: Open data visualization dashboard\n"
        "2: Run API and download files\n"
        "3: Run data cleaning and analysis\n"
        "4: Exit application\n"
    )

    if user_input == "1":
        print("\nOpening data visualization dashboard...")
        run_visualization()

    elif user_input == "2":
        print("To download data from the API, a year range is required")
        start_year = input("\nPlease specify a starting year (inclusive)\n")
        end_year = input("\nPlease specify an ending year (inclusive)\n")
        print("\nStarting API download to /data/raw_data/ directory...\n")
        run_api_download(start_year, end_year)

    elif user_input == "3":
        print("\nStarting data cleaning and analysis...\n")
        run_data_clean_and_analyze()

    elif user_input == "4":
        print("\nExiting application now...")
        sys.exit()