import sys
from .data.raw_data import scrape_funds
from .clean_and_analyze import analyze_data
from .visualization import scatterplots, stacked_charts, word_cloud, graph

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


def run_data_clean_and_analyze(start_year, end_year):
    """
    Runs the data cleaning and analysis functions
    """
    analyze_data.clean_and_analyze_all(start_year, end_year, RAW_DATA_DIR, CLEAN_DATA_DIR)


def run_visualization():
    """
    Runs the data vizualisation functions
    """
    app = graph.app
    app.run_server(debug=False)


def run():
    """
    """
    print("\nWelcome to Cappy Funding!")
    print("To use the application, please input one of the following 4 options into command line:")

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
        print("\nTo download data from the API, a starting and ending year is required to set a year range.")
        start_year = input("\nPlease specify a starting year (inclusive. To use the default starting year of 2016, please press Enter.\n")
        end_year = input("\nPlease specify an ending year (inclusive) To use the default ending year of 2020, please press Enter.\n")
        print("\nStarting API download to /data/raw_data/ directory...\n")
        run_api_download(start_year, end_year)

    elif user_input == "3":
        print("\nTo clean and analyze data, a starting and ending year is required to set a year range.")
        print("Please kindly note that the application currently only stores raw data from 2016 to 2020.")
        print("To clean and analyze raw data outside this year range, please download the data using option 2 (to run the API) first.")
        print("\nIMPORTANT: FOR THE DATA VISUALIZATION TO RUN SUCCESSFULLY, PLEASE USE THE DEFAULT STARTING AND ENDING YEAR.\n")
        start_year = input("\nPlease specify a starting year (inclusive). To use the DEFAULT starting year of 2016, please press ENTER.\n")
        end_year = input("\nPlease specify an ending year (inclusive). To use the DEFAULT ending year of 2020, please press ENTER.\n")
        print("\nStarting data cleaning and analysis...\n")
        run_data_clean_and_analyze(start_year, end_year)

    elif user_input == "4":
        print("\nExiting application now...")
        sys.exit()