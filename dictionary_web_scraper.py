# -*- coding: utf-8 -*-
"""Dictionary Web-Scraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nPkPaUjfv4pRYsnNd1mO0JylrK34eU2E
"""

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_def(word):
  return simple_get('https://www.dictionary.com/browse/' + word)

def parse_data(raw_html):
  html = BeautifulSoup(raw_html, 'html.parser')
  return html.find_all("div", {"class": "css-8lgfcg e1iplpfw1"})[0]

def define_word(word):
  html = get_def(word)
  
  try:
    section = parse_data(html)
    definition = section.section.ol.contents[0].span.text[:-1]
    print(definition)
    return ""
  except:
    print("Word does exist!")
