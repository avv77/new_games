from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
from time import sleep
from setting import db
import os


def fortnite():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    url = r'https://www.epicgames.com/fortnite/ru/news'

    driver.get(url)
    sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links = ['https://www.epicgames.com' + link['href'] for link in soup.select('a[class^="gridItem"]', href=True)]
    quotes_title = [title['title'] for title in soup.select('a[class^="gridItem"]', title=True)]
    date_text = [date.text for date in soup.find_all(class_='date')]

    driver.quit()

    month_dict = {'янв.': '01',
                  'фев.': '02',
                  'мар.': '03',
                  'апр.': '04',
                  'мая': '05',
                  'июн.': '06',
                  'июл.': '07',
                  'авг.': '08',
                  'сен.': '09',
                  'окт.': '10',
                  'ноя.': '11',
                  'дек.': '12'
                  }

    date_fortnite = []
    for date in date_text:
        date_list = date.split()
        date_list_format = date_list[:3]
        date_number = date_list_format[0]
        if len(date_number) == 1:
            date_number = '0' + date_number
        date_month_str = date_list_format[1]
        date_month_value = ''
        if date_month_str in month_dict.keys():
            date_month_value = month_dict[date_month_str]
        date_year = date_list_format[2]
        date_format_new = date_number + '.' + date_month_value + '.' + date_year
        date_fortnite.append(date_format_new)

    data_now = datetime.now()
    data_now_format = data_now.strftime("%d.%m.%Y")

    news_data_list_fortnite = []
    for index in range(len(date_fortnite)):
        date = date_fortnite[index]
        if data_now_format == date:
            title = quotes_title[index]
            link = links[index]
            new_text_all = '<b>Fortnite</b>' + '\n' + date + '\n' + f'<b>{title}</b>' + '\n' + link
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM fortnite WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if new_text_all not in news_text_list:
                    news_data_list_fortnite.append(new_text_all)
                    cur.execute(f"INSERT INTO 'fortnite' VALUES('{date}','{new_text_all}')")
                    conn.commit()
            else:
                news_data_list_fortnite.append(new_text_all)
                cur.execute(f"INSERT INTO 'fortnite' VALUES('{date}','{new_text_all}')")
                conn.commit()
    return news_data_list_fortnite
