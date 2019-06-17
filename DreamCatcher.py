from pycookiecheat import chrome_cookies
from Dream import Dream
import requests
from bs4 import BeautifulSoup


# This files handles the scraper and converts dreams objects
class DreamCatcher:

    def __init__(self, url: str, parameter: str):
        self.url = url
        self.page_number = 0
        self.current_dreams = []
        self.current_dream = []
        self.cookies = None
        self.parameter = parameter

        self.set_cookies_for_scraper()

    def set_cookies_for_scraper(self):
        self.cookies = chrome_cookies(self.url)

    def retrieve_page(self, url: str):
        page_response = requests.get(f'{url}{self.parameter}', cookies=self.cookies)
        return BeautifulSoup(page_response.content, "html.parser")

    def get_dreams_per_page(self):
        page_content = self.retrieve_page(self.url)
        return page_content.find('ul', attrs={'class': 'bubblelist'})

    def convert_dreams_to_objects(self):
        dreams = self.get_dreams_per_page()
        dreams_with_data = self.get_meta_data_of_dreams(dreams)
        print()

    def get_meta_data_of_dreams(self, dreams) -> list:
        scraped_dreams = []
        for dream in dreams:
            scraped_dream = Dream(dream, self.cookies, self.url)

            if scraped_dream.meta['category'] == "collection":
                print('Inception')
            else:
                scraped_dreams.append(scraped_dream)

            # TODO finish inception function when coming across a collection
            print()
        return scraped_dreams
