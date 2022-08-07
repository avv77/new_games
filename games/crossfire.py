from datetime import datetime
from bs4 import BeautifulSoup
import sqlite3
from setting import db
import requests


def crossfire():

    url = r'https://cfire.ru/news/'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    quotes = soup.find_all(class_='news_title')
    quotes1 = soup.find_all(class_='preview')
    quotes2 = soup.find_all(class_='date')

    links = ['https://cfire.ru' + link['href'] for link in soup.find_all(class_='news_title', href=True)]
    title_news = [title.text for title in quotes]
    news_all = [news.text for news in quotes1]
    date_news = [date.text for date in quotes2]

    data_now = datetime.now()
    data_now_format = data_now.strftime("%d.%m.%Y")
    index1 = 6
    data_now_format = data_now_format[:index1] + data_now_format[index1 + 2:]

    news_data_list_crossfire = []
    for index in range(len(date_news)):
        date = date_news[index]
        if data_now_format == date:
            title = title_news[index]
            news = news_all[index]
            link = links[index]
            new_text_all = "<b>Cross Fire</b>" + '\n' + date + '\n' + f"<b>{title}</b>" + '\n' + news + '\n' + link
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM crossfire WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if new_text_all not in news_text_list:
                    news_data_list_crossfire.append(new_text_all)
                    cur.execute(f"INSERT INTO 'crossfire' VALUES('{date}','{new_text_all}')")
                    conn.commit()
            else:
                news_data_list_crossfire.append(new_text_all)
                cur.execute(f"INSERT INTO 'crossfire' VALUES('{date}','{new_text_all}')")
                conn.commit()

    return news_data_list_crossfire
