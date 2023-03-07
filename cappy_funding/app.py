import sys
from .data.raw_data import scrape_funds
from .clean_and_analyze import analyze_data
from .visualization import scatterplots, stacked_charts, word_cloud

YEARS = ["2016", "2017", "2018", "2019", "2020"]
CLEAN_DATA_DIR = "./cappy_funding/data/clean_data/"
RAW_DATA_DIR = "./cappy_funding/data/raw_data/"

def run_api_download(year_lst):
    """
    Runs the API download and data cleaning functions
    """
    print("Downloading total federal funding by state file...\n")
    scrape_funds.total_funding()
    
    scrape_funds.data_year(year_lst)
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
    pass


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
        year_lst = input("\nPlease input a list of years to download the data (E.g. ['2016', '2017'])\n")
        print("\nStarting API download to /data/raw_data/ directory...\n")
        print("INPUT", year_lst)
        run_api_download(year_lst)

    elif user_input == "3":
        print("\nStarting data cleaning and analysis...\n")
        run_data_clean_and_analyze()

    elif user_input == "4":
        print("\nExiting application now...")
        sys.exit()