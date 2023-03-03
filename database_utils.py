import time
import requests
from urllib.parse import urlparse

ALLOWED_DOMAINS = ("https://fconline-foundationcenter-org.proxy.uchicago.edu/fdo-search/results?activity=form&_new_search=1&quicksearch=&subject_match=match_any&subject_area=SM&geographic_focus=&population_match=match_any&population_served=&organization_name=&organization_location=&staff=&government_grantmaker=1&support_strategy=&transaction_type=&organization_type=&amount_min=%240&amount_max=%2410%2C000%2C000%2C000&year_min=2003&year_max=2023&keywords=&ein=",)
REQUEST_DELAY = 0.1


def make_request(url):
    """
    Make a request to `url` and return the raw response.

    This function ensure that the domain matches what is expected and that the rate limit
    is obeyed.
    """
    # check if URL starts with an allowed domain name
    for domain in ALLOWED_DOMAINS:
        if url.startswith(domain):
            break
    else:
        raise ValueError(f"can not fetch {url}, must be in {ALLOWED_DOMAINS}")
    time.sleep(REQUEST_DELAY)
    print(f"Fetching {url}")
    resp = requests.get(url)
    return resp


def make_link_absolute(rel_url, current_url):
    """
    Given a relative URL like "/abc/def" or "?page=2"
    and a complete URL like "https://example.com/1/2/3" this function will
    combine the two yielding a URL like "https://example.com/abc/def"

    Parameters:
        * rel_url:      a URL or fragment
        * current_url:  a complete URL used to make the request that contained a link to rel_url

    Returns:
        A full URL with protocol & domain that refers to rel_url.
    """
    url = urlparse(current_url)
    if rel_url.startswith("/"):
        return f"{url.scheme}://{url.netloc}{rel_url}"
    elif rel_url.startswith("?"):
        return f"{url.scheme}://{url.netloc}{url.path}{rel_url}"
    else:
        return rel_url
