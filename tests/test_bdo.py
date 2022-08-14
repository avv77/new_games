import unittest
from datetime import datetime
from games.bdo import bdo_soup, bdo_links_date_title, bdo_now_data, news_text_all_bdo
import requests
from bs4 import BeautifulSoup


class Bdo(unittest.TestCase):

    def test_bdo_soup(self):
        self.assertTrue(bdo_soup())

    def test_bdo_links_date_title(self):
        url = 'https://www.ru.playblackdesert.com/News/Notice'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(bdo_links_date_title(soup))

    def test_bdo_now_data(self):
        data_now_test = datetime.now()
        data_now_format = data_now_test.strftime("%d/%m/%Y")
        test = bdo_now_data()
        self.assertEqual(data_now_format, test[0])

    def test_news_text_all_bdo(self):
        index = 0
        title_news = ['Новость']
        links = [r'https://1.ru']
        data_telegram = '13.08.2022'
        news_test = news_text_all_bdo(index, title_news, links, data_telegram)
        self.assertEqual(news_test, '<b>Black Desert</b>\n13.08.2022\n<b>Новость</b>\nhttps://1.ru')


if __name__ == '__main__':
    unittest.main()
