from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
from time import sleep
from selenium.webdriver.chrome.options import Options


def leagueoflegends():
    options = Options()
    options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
    driver = webdriver.Chrome(chrome_options=options, executable_path="D:/PyCharmProject/News_Games_2/chromedriver.exe")

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

    news_data_list_leagueoflegends = []
    for index in range(len(date_news)):
        date = date_news[index]
        if data_now_format == date:
            title = title_news[index]
            link = links[index]
            new_text_all = '<b>LEAGUE OF LEGENDS</b>' + '\n' + date + '\n' + f'<b>{title}</b>' + '\n' + link
            conn = sqlite3.connect(r'D:\PyCharmProject\News_Games\db\news.db')
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
    return news_data_list_leagueoflegends
