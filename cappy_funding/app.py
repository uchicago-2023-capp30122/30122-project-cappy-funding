import sys
from .cappy_funding.data.raw_data import scrape_funds
from .cappy_funding.clean_and_analyze import analyze_data

YEARS = ["2016", "2017", "2018", "2019", "2020"]
CLEAN_DATA_DIR = "data/clean_data/"
RAW_DATA_DIR = "data/raw_data/"

def run_api_download():
    """
    Runs the API download and data cleaning functions
    """
    scrape_funds.total_funding()
    # scrape_funds.data_year()


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


def main():
    """
    """
    print("Welcome! Please select one of the four options below:\n")
    user_input = input(
        "\n1: Run data visualisation\n"
        "2: Run API download\n"
        "3: Run data cleaning and analysis\n"
        "4: Exit application\n"
    )

    if user_input == 1:
        run_visualization()

    elif user_input == 2:
        run_api_download()

    elif user_input == 3:
        run_data_clean_and_analyze()

    elif user_input == 4:
        sys.exit()


# if __name__ == "__main__":
#     main()