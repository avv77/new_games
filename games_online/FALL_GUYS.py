from datetime import datetime
from bs4 import BeautifulSoup
import requests
import sqlite3
from setting import db


def fall_guys():
    url = r'https://www.fallguys.com/ru/news'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links_no_format = ['https://www.fallguys.com' + a.get('href') for a in soup.find_all('a') if a.get('href') and
                       a.get('href').startswith('/ru/news/')]
    links = list(dict.fromkeys(links_no_format))

    date_title_news = [date.text for date in soup.find_all(class_='RichTextSpan__RichTextSpanWrap-sc-ovn0ao-0 gPzNkg'
                                                                  ' ue-rich-text typography-rich-text loc-ru')]
    title_news = []
    date_news_no_format = []

    for i in date_title_news:
        if date_title_news.index(i) % 2 == 0:
            title_news.append(i)
        else:
            date_news_no_format.append(i)

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

    date_news = []
    for date in date_news_no_format:
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
        date_news.append(date_format_new)

    data_now = datetime.now()
    data_now_format = data_now.strftime("%d.%m.%Y")

    news_data_list_fall_guys = []
    for index in range(len(date_news)):
        date = date_news[index]
        if data_now_format == date:
            title = title_news[index]
            link = links[index]
            news_text_all = '<b>Fall Guys</b>' + '\n' + date + '\n' + f'<b>{title}</b>' + '\n' + link
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(f"SELECT Text FROM fall_guys WHERE Date = '{date}'")
            results = cur.fetchall()
            news_text_list = []
            if len(results) > 0:
                for text in results:
                    text_list = list(text)
                    for j in text_list:
                        news_text_list.append(j)
                if news_text_all not in news_text_list:
                    news_data_list_fall_guys.append(news_text_all)
                    cur.execute(f"INSERT INTO 'fall_guys' VALUES('{date}','{news_text_all}')")
                    conn.commit()
            else:
                news_data_list_fall_guys.append(news_text_all)
                cur.execute(f"INSERT INTO 'fall_guys' VALUES('{date}','{news_text_all}')")
                conn.commit()
    return news_data_list_fall_guys
