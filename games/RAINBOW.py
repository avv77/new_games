from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
from time import sleep
from selenium.webdriver.chrome.options import Options
from setting import db


def rainbow():
    options = Options()
    options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
    driver = webdriver.Chrome(chrome_options=options, executable_path="D:/PyCharmProject/News_Games_2/chromedriver.exe")

    url = r'https://www.ubisoft.com/ru-ru/game/rainbow-six/siege/news-updates'

    driver.get(url)
    sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links = ['https://www.ubisoft.com' + link['href'] for link in soup.find_all(class_='updatesFeed__item', href=True)]
    date_news_no_format = [date.text for date in soup.find_all(class_='date')]
    title_news = [title.text for title in soup.find_all(class_='updatesFeed__item__wrapper__content__title')]
    news_all = [news.text for news in soup.find_all(class_='updatesFeed__item__wrapper__content__abstract')]

    driver.quit()

    date_news_no_month = []
    for date in date_news_no_format:
        if '.' in date[1]:
            date_now = '0' + date
            date_news_no_month.append(date_now)
        else:
            date_news_no_month.append(date)

    date_news = []
    for date in date_news_no_month:
        if '.' in date[4]:
            date_month = date[:3] + '0' + date[3:]
            date_news.append(date_month)
        else:
            date_news.append(date)

    date_news.pop(0)

    data_now = datetime.now()
    data_now_format = data_now.strftime("%d.%m.%Y")

    news_data_list_rainbow = []
    for index in range(len(date_news)):
        date = date_news[index]
        if data_now_format == date:
            title = title_news[index]
            link = links[index]
            news = news_all[index]
            news_text_all = '<b>Rainbow</b>' + '\n' + date + '\n' + f'<b>{title}</b>' + '\n' + news + '\n' + link
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM rainbow WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if news_text_all not in news_text_list:
                    news_data_list_rainbow.append(news_text_all)
                    cur.execute(f"INSERT INTO 'rainbow' VALUES('{date}','{news_text_all}')")
                    conn.commit()
            else:
                news_data_list_rainbow.append(news_text_all)
                cur.execute(f"INSERT INTO 'rainbow' VALUES('{date}','{news_text_all}')")
                conn.commit()
    return news_data_list_rainbow
