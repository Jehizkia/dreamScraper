import requests
import helper
from database import Dream as dbDream


class Dream:

    def __init__(self, dream_preview, cookies, url):
        self.dream_preview = dream_preview
        self.cookies = cookies
        self.url = url
        self.dream_page = None
        self.meta = {}

        self.get_initial_meta_data()
        self.retrieve_dream_page()
        self.extract_dream_info()
        self.save_dream()

    def get_initial_meta_data(self):
        page_href = self.dream_preview.find('div', attrs={'class': 'bc__link'}).contents[0]
        split_href_url = page_href['href'].split('/')

        self.meta['id'] = split_href_url[2]
        self.meta['category'] = split_href_url[1]

    def retrieve_dream_page(self):
        dream_url = f"{self.url}/{self.meta['category']}/{self.meta['id'] }"
        self.dream_page = helper.retrieve_page_contents(dream_url, self.cookies)
        print(f'retrieved page: {dream_url}')

    def extract_title(self):
        title_tag = self.dream_preview.find('h4', attrs={'class': 'bm__title'})
        self.meta['title'] = title_tag.get_text()
        print(f"extracted title: {self.meta['title']}")

    def extract_description(self):
        description_tag = self.dream_page.find('h2', attrs={'class': 'profile__subtitle'})
        if description_tag is not None:
            self.meta['description'] = description_tag.get_text()
        else:
            self.meta['description'] = ''
            print(f"extracted description: {self.meta['description']}")

    def extract_tags(self):
        pass

    def extract_played_times(self):
        stats_tag = self.dream_page.find('ul', attrs={'class': 'profile__stats'})
        stat_tag = stats_tag.contents[0]
        played_text = stat_tag.span.get_text()

        # Remove text from string
        played_text = played_text.replace('Played ', '')
        played_text = played_text.replace('times by ', '')
        played_text = played_text.replace('dreamers', '')
        played_final_stat = played_text.split(' ')

        self.meta['played_times'] = int(played_final_stat[0].replace(',', ''))
        self.meta['played_times_by'] = int(played_final_stat[1].replace(',', ''))
        print(f"extracted played up: {self.meta['played_times']}")

    def extract_thumbs_up(self):
        stats_tag = self.dream_page.find('ul', attrs={'class': 'profile__stats'})
        stat_tag = stats_tag.contents[2]
        thumbs_up_text = stat_tag.span.get_text()

        # Remove text from string
        thumbs_up_text = thumbs_up_text.replace('thumbs up', '')
        self.meta['thumbs_up'] = int(thumbs_up_text.replace(',', ''))
        print(f"extracted thumbs up: {self.meta['thumbs_up']}")

    def extract_date_time(self):
        pass

    def extract_author(self):
        author_tag = self.dream_page.find('h2', attrs={'class': 'profile__author'})
        self.meta['author'] = author_tag.get_text()
        print(f"extracted author: {self.meta['author']}")

    def extract_dream_info(self):
        self.extract_title()
        self.extract_author()
        self.extract_description()
        self.extract_played_times()
        self.extract_thumbs_up()

    def save_dream(self):
        new_db_dream = dbDream(
            title=self.meta['title'],
            description=self.meta['description'],
            author=self.meta['author'],
            played_time=self.meta['played_times'],
            played_times_by=self.meta['played_times_by'],
            thumbs_up=self.meta['thumbs_up'],
            category=self.meta['category']
        )

        new_db_dream.save()
        print(f"Dream {self.meta['title']} saved to db")
