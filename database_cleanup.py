import json

# words to be ignored in indexing
INDEX_IGNORE = (
    "a",
    "an",
    "and",
    "&",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
    "chicago",
    "park",
    "parks",
)

def normalize_address(address):
    """
    This function takes an address and returns a normalized
    version of the address with extra whitespace removed.

    Parameters:
        * address:  a string representing an address

    Returns:
        A string representing the address with extra whitespace removed.
    """
    rmv_n = address.replace("\n    ","")
    list_chars = " ".join(rmv_n.split())

    return list_chars

def tokenize(park):
    """
    This function takes a dictionary representing a park and returns a
    list of tokens that can be used to search for the park.

    The tokens should be a combination of the park's name, history, and
    description.

    All tokens should be normalized to lowercase, with punctuation removed as
    described in README.md.

    Tokens that match INDEX_IGNORE should be ignored.

    Parameters:
        * park:  a dictionary representing a park

    Returns:
        A list of tokens that can be used to search for the park.
    """
    name = str_to_list(normalize_address(park['name']))
    norm_description = str_to_list(normalize_address(park['description']))
    norm_history = str_to_list(normalize_address(park['history']))
    list_tokens = name + norm_description + norm_history

    return list_tokens

def str_to_list(string):
    """
    This function takes a string and returns a list of tokens that are normalized 
    to lowercase with punctuations removed. 

    Parameters:
        *string: the string needed to be transformed.
    
    Returns:
        A list of tokens after normalization.
    """
    punctuations = ['!', '.', ',', '"', "'", '?', ':']
    low_case = string.lower()
    for punc in punctuations:
        low_case = low_case.replace(punc, "")
    str_list = low_case.split(" ")
    str_list = [token for token in str_list if token not in INDEX_IGNORE]

    return str_list

def clean():
    """
    This function loads the parks.json file and writes a new file
    named normalized_parks.json that contains a normalized version
    of the parks data.
    """
 
    # open original json file and edit it
    with open("parks.json") as f:
        data = json.load(f)
        
    for park in data:
        tokens = tokenize(park)
        park['tokens'] = tokens
        park['address'] = normalize_address(park['address'])
    
    # save the normalized data in new json file 
    with open('normalized_parks.json', 'w') as f:
        json.dump(data, f, indent = 1)
