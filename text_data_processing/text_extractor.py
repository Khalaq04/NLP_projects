from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
import requests
from requests.models import MissingSchema
import spacy
import trafilatura

input_df = pd.read_csv("Input.csv")     # Reading the csv input file

urls = input_df.loc[:,"URL"]        # Storing all urls in a list
url_ids = input_df.loc[:,"URL_ID"]  # Storing all url ids in a list

urls_dict = dict(zip(url_ids, urls))

def extract_text(content):
    # Function to extract text from a url
    filtered_text = ""
    bsoup = BeautifulSoup(content, 'html.parser')       # Beautifulsoup object

    try:
        filtered_text = bsoup.find('h1').get_text()        # Finding all the texts with headers(titles)
        filtered_text += "\n"
    except:
        filtered_text += ""
    try:
        for p in bsoup.find_all('p'):       # Finding all texts with paragraph tags(texts)
            filtered_text += p.get_text()
    except:
        filtered_text += ""
    return filtered_text.strip()

for id in urls_dict:
    filename = str(id) + ".txt"      # Setting the filename to <url_id>.txt
    f = open(filename, "w")     # Creating a file with the above name with write permission

    response = requests.get(urls_dict[id])    # Sending and storing a get request to the url
    text = extract_text(response.content)       # Storing text from the url using extract_text function

    f.write(text)       # Writing the text to the file
    f.close()           # Closing the file