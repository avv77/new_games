import unittest
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from games.crossfire import crossfire_soup, crossfire_links_date_title, crossfire_now_data, news_text_all_crossfire


class Crossfire(unittest.TestCase):

    def test_crossfire_soup(self):
        self.assertTrue(crossfire_soup())

    def test_crossfire_links_date_title(self):
        url = r'https://cfire.ru/news/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(crossfire_links_date_title(soup))

    def test_crossfire_now_data(self):
        data_now_test = datetime.now()
        data_now_format = data_now_test.strftime("%d.%m.%Y")
        index1 = 6
        data_now_format = data_now_format[:index1] + data_now_format[index1 + 2:]
        test = crossfire_now_data()
        self.assertEqual(data_now_format, test)

    def test_news_text_all_bdo(self):
        index = 0
        title_news = ['Новость']
        links = [r'https://1.ru']
        date = '13.08.2022'
        news_all = ['Хорошие вести']
        news_test = news_text_all_crossfire(title_news, index, news_all, links, date)
        self.assertEqual(news_test, '<b>Cross Fire</b>\n13.08.2022\n<b>Новость</b>\nХорошие вести\nhttps://1.ru')
