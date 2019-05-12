import requests
from bs4 import BeautifulSoup


def retrieve_page_contents(url: str, cookies):
    page_response = requests.get(url, cookies=cookies)
    return BeautifulSoup(page_response.content, "html.parser")
