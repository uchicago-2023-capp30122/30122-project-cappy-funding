import sys
from .data.raw_data import scrape_funds
from .clean_and_analyze import analyze_data
from .visualization import stacked_charts, word_cloud, graph

# Author: Foo Suon Chuang (Bryan), Yujie Jiang, Gongzi Chen and Ziyang Chen

CLEAN_DATA_DIR = "./cappy_funding/data/clean_data/"
RAW_DATA_DIR = "./cappy_funding/data/raw_data/"

def run_api_download(start_year, end_year):
    """
    Runs the API download and data cleaning functions
    Written by: Yujie Jiang
    """
    print("Downloading total federal funding by state file...\n")
    scrape_funds.total_funding()
    
    scrape_funds.data_year(start_year, end_year)
    print("\nAll years downloaded from USA Spending API...")


def run_data_clean_and_analyze(start_year, end_year):
    """
    Runs the data cleaning and analysis functions
    Written by: Foo Suon Chuang (Bryan)
    """
    analyze_data.clean_and_analyze_all(start_year, end_year, RAW_DATA_DIR, CLEAN_DATA_DIR)


def run_visualization():
    """
    Runs the data vizualisation functions
    Written by: Ziyang Chen, Gongzi Chen
    """
    print("\nCreating funding time series stacked chart...")
    stacked_charts.create_stacked_area_chart(CLEAN_DATA_DIR)
    print("Funding time series stacked chart saved to visualization/")

    print("\nCreating funding word cloud for each year...")
    word_cloud.funding_word_clouds(CLEAN_DATA_DIR)
    print("All years funding word cloud saved to visualization/...")

    print("\nOpening data visualization dashboard...")
    app = graph.app
    app.run_server(port=12345, debug=False)


def run():
    """
    Runs the application's main user interface
    Written by: Foo Suon Chuang (Bryan)
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
        run_visualization()

    elif user_input == "2":
        print("\nTo download data from the API, a starting and ending year is required to set a year range.")
        start_year = input("\nPlease specify a starting year (inclusive). To use the default starting year of 2016, please press Enter.\n")
        end_year = input("\nPlease specify an ending year (inclusive) To use the default ending year of 2020, please press Enter.\n")
        
        if start_year == "":
            start_year = "2016"
        if end_year == "":
            end_year = "2020"

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

        if start_year == "":
            start_year = "2016"
        if end_year == "":
            end_year = "2020"

        run_data_clean_and_analyze(start_year, end_year)

    elif user_input == "4":
        print("\nExiting application now...")
        sys.exit()
