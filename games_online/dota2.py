from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver
from setting import db, log1
import os
import logging.config

logging.config.dictConfig(log1)
log = logging.getLogger('fuction')


def dota2():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    url = r'https://www.dota2.com/news'

    driver.get(url)
    sleep(20)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links = ['https://www.dota2.com' + link['href'] for link in soup.find_all(class_='blogcapsule_BlogCapsule_3OBoG',
                                                                              href=True)]
    title_news = [title.text for title in soup.find_all(class_='blogcapsule_Title_39UGs')]
    news_all = [news.text for news in soup.find_all(class_='blogcapsule_Desc_471NM')]
    date_news = [date.text for date in soup.find_all(class_='blogcapsule_Date_3kp_O')]

    driver.quit()

    month_dict = {'января': '01',
                  'февраля': '02',
                  'марта': '03',
                  'апреля': '04',
                  'мая': '05',
                  'июня': '06',
                  'июля': '07',
                  'августа': '08',
                  'сентября': '09',
                  'октября': '10',
                  'ноября': '11',
                  'декабря': '12'
                  }

    date_dota2 = []
    for date in date_news:
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
        date_dota2.append(date_format_new)

    data_now = datetime.now()
    data_now_format = data_now.strftime("%d.%m.%Y")

    news_data_list_dota2 = []
    for index in range(len(date_dota2)):
        date = date_dota2[index]
        if data_now_format == date:
            title = title_news[index]
            link = links[index]
            news = news_all[index]
            new_text_all = '<b>Dota2</b>' + '\n' + date + '\n' + f'<b>{title}</b>' + '\n' + news + '\n' + link
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM dota2 WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if new_text_all not in news_text_list:
                    news_data_list_dota2.append(new_text_all)
                    cur.execute(f"INSERT INTO 'dota2' VALUES('{date}','{new_text_all}')")
                    conn.commit()
            else:
                news_data_list_dota2.append(new_text_all)
                cur.execute(f"INSERT INTO 'dota2' VALUES('{date}','{new_text_all}')")
                conn.commit()
    log.info(f'{news_data_list_dota2}')
    return news_data_list_dota2
