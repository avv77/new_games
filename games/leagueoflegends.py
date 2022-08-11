from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
from time import sleep
from setting import db, log1
import os
import logging.config

logging.config.dictConfig(log1)
log = logging.getLogger('fuction')


def leagueoflegends():
    log.debug(f'Функция "leagueoflegends" начала работу')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    url = r'https://www.leagueoflegends.com/ru-ru/latest-news/'

    driver.get(url)
    sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    date_news_noformat = [date['datetime'] for date in soup.find_all('time', datetime=True)]
    title_news = [title.text for title in soup.find_all('h2')]
    links_noformat = [link['href'] for link in soup.find_all(class_='style__Wrapper-sc-1h41bzo-0', href=True)]
    driver.quit()

    links = []
    for link in links_noformat:
        if len(link) > 0:
            if link[0] == '/':
                link_format = 'https://www.leagueoflegends.com' + link
                links.append(link_format)
            else:
                links.append(link)

    date_news = []
    for date in date_news_noformat:
        date_format = date[:10]
        date_news.append(date_format)

    data_now = datetime.now()
    data_now_format = data_now.strftime("%Y-%m-%d")
    data_telegram = data_now.strftime("%d.%m.%Y")

    news_data_list_leagueoflegends = []
    for index in range(len(date_news)):
        date = date_news[index]
        if data_now_format == date:
            title = title_news[index]
            link = links[index]
            new_text_all = '<b>LEAGUE OF LEGENDS</b>' + '\n' + data_telegram + '\n' + f'<b>{title}</b>' + '\n' + link
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM leagueoflegends WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if new_text_all not in news_text_list:
                    news_data_list_leagueoflegends.append(new_text_all)
                    cur.execute(f"INSERT INTO 'leagueoflegends' VALUES('{date}','{new_text_all}')")
                    conn.commit()
            else:
                news_data_list_leagueoflegends.append(new_text_all)
                cur.execute(f"INSERT INTO 'leagueoflegends' VALUES('{date}','{new_text_all}')")
                conn.commit()
    log.debug(f'Функция "leagueoflegends" закончила работу')
    return news_data_list_leagueoflegends
