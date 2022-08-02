from datetime import datetime
from bs4 import BeautifulSoup
import requests
import sqlite3


def bdo_online():
    url = 'https://www.ru.playblackdesert.com/News/Notice'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = [link['href'] for link in soup.find('div', {'class': 'thumb_nail_area'}).findAll('a')]
    date_news = [date.text for date in soup.find('div', {'class': 'thumb_nail_area'}).findAll(class_='date')]
    title_no_format = [title.text for title in soup.find('div', {'class': 'thumb_nail_area'}).findAll(class_='title')]

    title_news = []
    for i in title_no_format:
        title_now = i.split('    ')
        title_now = title_now[1:]
        del title_now[-1]
        for j in title_now:
            if len(j) != 0:
                j = j[:-4]
                title_news.append(j)

    data_now = datetime.now()
    data_now_format = data_now.strftime("%d/%m/%Y")
    data_telegram = data_now.strftime("%d.%m.%Y")

    news_data_list_bdo_online = []
    for index in range(len(date_news)):
        date = date_news[index]
        if data_now_format == date:
            title = title_news[index]
            link = links[index]
            news_text_all = '<b>Black Desert</b>' + '\n' + data_telegram + '\n' + f'<b>{title}</b>' + '\n' + link
            conn = sqlite3.connect(r'D:\PyCharmProject\News_Games\db\news.db')
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM bdo WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if news_text_all not in news_text_list:
                    news_data_list_bdo_online.append(news_text_all)
                    cur.execute(f"INSERT INTO 'bdo' VALUES('{date}','{news_text_all}')")
                    conn.commit()
            else:
                news_data_list_bdo_online.append(news_text_all)
                cur.execute(f"INSERT INTO 'bdo' VALUES('{date}','{news_text_all}')")
                conn.commit()

    return news_data_list_bdo_online
