from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
from time import sleep
from setting import db
import os


def hearthstone():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    url = r'https://playhearthstone.com/ru-ru/news#articles'

    driver.get(url)
    sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links_no_format = [link['href'] for link in soup.find_all(class_='NewsListItem__ArticleListItem-g14b0z-0',
                                                              href=True)]
    date_news = [date.text for date in soup.find_all('time')]
    title_news = [title.text for title in soup.find_all('h3')]
    news_all = [news.text for news in soup.find_all(class_='NewsListItem__ArticleSummary-g14b0z-5 gOltLb '
                                                           'ArticleSummary')]

    driver.quit()

    links = []
    for link in links_no_format:
        if link[:5] != 'https':
            link_now = 'https://worldofwarcraft.com' + link
            links.append(link_now)
        else:
            links.append(link)

    title_news.pop(0)

    data_now = datetime.now()
    data_now_format = data_now.strftime("%d.%m.%Y")

    news_data_list_hearthstone = []
    for index in range(len(date_news)):
        date = date_news[index]
        if data_now_format == date:
            title = title_news[index]
            link = links[index]
            news = news_all[index]
            news_text_all = '<b>Hearthstone</b>' + '\n' + date + '\n' + f'<b>{title}</b>' + '\n' + news + '\n' + link
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM hearthstone WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if news_text_all not in news_text_list:
                    news_data_list_hearthstone.append(news_text_all)
                    cur.execute(f"INSERT INTO 'hearthstone' VALUES('{date}','{news_text_all}')")
                    conn.commit()
            else:
                news_data_list_hearthstone.append(news_text_all)
                cur.execute(f"INSERT INTO 'hearthstone' VALUES('{date}','{news_text_all}')")
                conn.commit()
    return news_data_list_hearthstone
