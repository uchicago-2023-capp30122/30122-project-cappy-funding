import sys
import json
import lxml.html
from database_utils import make_request, make_link_absolute
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup

def scrape_funding_data():

    import requests
from bs4 import BeautifulSoup

# set the URL of the page to scrape
url = 'https://fconline-foundationcenter-org.proxy.uchicago.edu/search/'

# set the filters to apply
params = {
    'term': 'Education',
    'state': 'IL'
}

# send a GET request to the URL with the filters applied
response = requests.get(url, params=params)

# create a BeautifulSoup object to parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# find the relevant HTML tags that contain the data you want to scrape
results = soup.find_all('div', {'class': 'result-item'})

# extract the desired information from the HTML tags
for result in results:
    name = result.find('a', {'class': 'result-item-title'}).text.strip()
    description = result.find('p', {'class': 'result-item-desc'}).text.strip()
    location = result.find('div', {'class': 'result-item-location'}).text.strip()
    print(f'{name}\n{description}\n{location}\n')


def scrape_park_page(url):
    '''
    driver = webdriver.Firefox()
    driver = driver.get("https://fconline-foundationcenter-org.proxy.uchicago.edu/fdo-search/results?activity=form&_new_search=1&quicksearch=&subject_match=match_any&subject_area=SM&geographic_focus=&population_match=match_any&population_served=&organization_name=&organization_location=&staff=&government_grantmaker=1&support_strategy=&transaction_type=&organization_type=&amount_min=%240&amount_max=%2410%2C000%2C000%2C000&year_min=2003&year_max=2023&keywords=&ein=")
    dropdown = Select(driver.find_element_by_id("accordionundefined"))
    dropdown.select_by_visible_text("Agriculture, fishing and forestry")
    search_button = driver.find_element_by_id("prepared-elastic-input")
    search_button.click()
    data_element = driver.find_element_by_class_name("top-cell")
    data = data_element.text
    print(data)
    driver.quit()
    '''
    response = make_request(url)
    root = lxml.html.fromstring(response.text)
    output = root.xpath('//h2[@class="search-table-title medium-heading"]')
    for item in output:
        text = text.text_content()
    return output

     # url
    dict['url'] = url

     # name
    name = root.xpath("//h2[@class = 'section']")
    for item in name:
        name_text = item.text_content()
    dict['name'] = name_text
    
    # address
    address = root.xpath("//p[@class='address']")
    for item in address:
        address_text = item.text_content()
    dict['address'] = address_text
    
    # description and history
    description = root.xpath("//div[@class='view-content']")
    for elem in description:
        children = elem.getchildren()

        # check if the block title matches either 'Description' or 'History'
        title = children[1].text_content()
        if "Description" in title:
            des_txt =  children[2].text_content()
            dict['description'] = des_txt
        if "History" in title:
            his_txt = children[2].text_content()
            dict['history'] = his_txt
        else:
            dict['history'] = ""
    
    return dict

def get_park_urls(url):
    """
    This function takes a URL to a page of parks and returns a
    list of URLs to each park on that page.

    Parameters:
        * url:  a URL to a page of parks

    Returns:
        A list of URLs to each park on the page.
    """
    response = make_request(url)
    root = lxml.html.fromstring(response.text)
    url_list = []
    current_url = url

    # loop for every park in the page
    url_table = root.xpath('//table[@id="employees"]//tbody')[0].getchildren()
    for url in url_table:
        rel_url = url.xpath(".//td/a/@href")[0]
        full_url = make_link_absolute(rel_url, current_url)
        url_list.append(full_url)

    return url_list

def get_next_page_url(url):
    """
    This function takes a URL to a page of parks and returns a
    URL to the next page of parks if one exists.

    If no next page exists, this function returns None.
    """
    response = make_request(url)
    root = lxml.html.fromstring(response.text)
    current_url = url
    next_page = root.xpath('//div/a[@title = "next page"]/@href')
    if next_page:
        full_url = make_link_absolute(next_page[0], current_url)
        return full_url
    else:
        return None

def crawl(max_parks_to_crawl):
    """
    This function starts at the base URL for the parks site and
    crawls through each page of parks, scraping each park page
    and saving output to a file named "parks.json".

    Parameters:
        * max_parks_to_crawl:  the maximum number of pages to crawl
    """
    list_page_url = "https://scrapple.fly.dev/parks"
    parks = []
    urls_visited = 0
    
    while urls_visited < max_parks_to_crawl:
        parks_url = get_park_urls(list_page_url)

    # get information of every park in one page
        for park in parks_url:

            if urls_visited == max_parks_to_crawl:
                break

            park_info = scrape_park_page(park)
            parks.append(park_info)
            urls_visited += 1

        # check if it needs to turn to the next page
        list_page_url = get_next_page_url(list_page_url)

    print("Writing parks.json")
    with open("parks.json", "w") as f:
        json.dump(parks, f, indent = 1)

if __name__ == "__main__":
    """
    Tip: It can be convenient to add small entrypoints to submodules
         for ease of testing.

    In this file, we call scrape_park_page with a given URL and pretty-print
    the output.

    This allows testing that function from the command line with:

    $ python -m parks.crawler https://scrapple.fly.dev/parks/4

    Feel free to modify/change this if you wish, you won't be graded on this code.
    """
    from pprint import pprint

    if len(sys.argv) != 2:
        print("Usage: python -m parks.crawler <url>")
        sys.exit(1)
    result = scrape_park_page(sys.argv[1])
    print(result)
