from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import sqlite3
from time import sleep
from selenium.webdriver.chrome.options import Options


def eve_online():
    options = Options()
    options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
    driver = webdriver.Chrome(chrome_options=options, executable_path="D:/PyCharmProject/News_Games_2/chromedriver.exe")

    url = 'https://www.eveonline.com/ru/news/archive'
    driver.get(url)
    sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links_no_format = soup.find_all('h3', attrs={'class': 'Typography__DynamicComponent-sc-1bolua0-0 tBRod '
                                                          'Card_title__uBRxe'})
    list_links = []

    for element in links_no_format:
        tlist = element.find('a')
        list_links.append(tlist)

    links = ['https://www.eveonline.com' + link['href'] for link in list_links]
    title_news = [title.text for title in list_links]
    date_news_no_format = [date.text for date in soup.find_all('span', class_='DateAndAuthor_author_date__3y2EY')]
    date_news = []
    for date in date_news_no_format:
        date_format = date[:10]
        date_news.append(date_format)

    data_now = datetime.now()
    data_now_format = data_now.strftime("%Y-%m-%d")
    data_telegram = data_now.strftime("%d.%m.%Y")

    news_data_list_eve_online = []
    for index in range(len(date_news)):
        date = date_news[index]
        if data_now_format == date:
            title = title_news[index]
            link = links[index]
            news_text_all = '<b>Eve online</b>' + '\n' + data_telegram + '\n' + f'<b>{title}</b>' + '\n' + link
            conn = sqlite3.connect(r'D:\PyCharmProject\News_Games\db\news.db')
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM eve_online WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if news_text_all not in news_text_list:
                    news_data_list_eve_online.append(news_text_all)
                    cur.execute(f"INSERT INTO 'eve_online' VALUES('{date}','{news_text_all}')")
                    conn.commit()
            else:
                news_data_list_eve_online.append(news_text_all)
                cur.execute(f"INSERT INTO 'eve_online' VALUES('{date}','{news_text_all}')")
                conn.commit()
    return news_data_list_eve_online
