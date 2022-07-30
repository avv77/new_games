from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
from time import sleep
from selenium.webdriver.chrome.options import Options


def world_of_tanks():
    options = Options()
    options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
    driver = webdriver.Chrome(chrome_options=options, executable_path="D:/PyCharmProject/News_Games/chromedriver.exe")

    url = 'https://worldoftanks.ru/ru/news/'
    driver.get(url)
    sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links_no_format = ['https://worldoftanks.ru' + link['href'] for link in soup.find_all(class_='preview_link',
                                                                                          href=True)]
    links = links_no_format[::2]
    date_news = [date.text for date in soup.find_all('span', class_='preview_time')]
    title_news = [title.text for title in soup.find_all('h2', class_='preview_title')]

    news_data_list_worldoftanks = []
    for index in range(len(date_news)):
        date = date_news[index]
        if date == 'сегодня':
            title = title_news[index]
            link = links[index]
            news_text_all = "<b>World of Tanks</b>" + '\n' + date + '\n' + f"<b>{title}</b>" + '\n' + link
            conn = sqlite3.connect(r'D:\PyCharmProject\News_Games\db\news.db')
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM world_of_tanks WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if news_text_all not in news_text_list:
                    news_data_list_worldoftanks.append(news_text_all)
                    cur.execute(f"INSERT INTO 'world_of_tanks' VALUES('{date}','{news_text_all}')")
                    conn.commit()
            else:
                news_data_list_worldoftanks.append(news_text_all)
                cur.execute(f"INSERT INTO 'world_of_tanks' VALUES('{date}','{news_text_all}')")
                conn.commit()
    return news_data_list_worldoftanks
