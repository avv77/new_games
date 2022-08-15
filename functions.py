import os
from time import sleep
from games_online.FALL_GUYS import fall_guys
from games_online.HEARTHSTONE import hearthstone
from games_online.RAINBOW import rainbow
from games_online.bdo import bdo_online
from games_online.crossfire import crossfire
from games_online.dota2 import dota2
from games_online.eve_online import eve_online
from games_online.fortnite import fortnite
from games_online.leagueoflegends import leagueoflegends
from games_online.worldoftanks import world_of_tanks
from setting import CHANNEL_NAME, db, log1
import schedule
import telebot
import sqlite3
from datetime import datetime
import logging.config

BOT_TOKEN_1 = os.environ.get('BOT_TOKEN_1')

bot = telebot.TeleBot(BOT_TOKEN_1)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

logging.config.dictConfig(log1)
log = logging.getLogger('fuction')

function_list = [crossfire, eve_online, fortnite, dota2, leagueoflegends, rainbow, hearthstone,
                 fall_guys, bdo_online, world_of_tanks]

photo_list = ['/app/img/crossfire.jpg', '/app/img/eve-online.jpg', '/app/img/fortnite.jpg', '/app/img/dota2.jpg',
              '/app/img/league-of-legends.jpg', '/app/img/rainbow.jpg', '/app/img/hearthstone.jpg',
              '/app/img/Fallguys.jpg',
              '/app/img/bdo_online.jpg', '/app/img/wot.jpg']

function_list_name = ['crossfire', 'eve_online', 'fortnite', 'dota2', 'leagueoflegends', 'rainbow', 'hearthstone',
                      'fall_guys', 'bdo_online', 'world_of_tanks']


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def send_news(data_list, photo):
    for news_game in data_list:
        with open(photo, 'rb') as f:
            bot.send_photo(CHANNEL_NAME, f, caption=news_game, parse_mode="HTML")


def run():
    for index in range(len(function_list)):
        try:
            news_data_list = function_list[index]()
            log.info(f'Функция {function_list_name[index]} закончила работу')
            send_news(news_data_list, photo_list[index])
        except Exception as exc:
            data_now = datetime.now()
            data_now_format = data_now.strftime("%Y-%m-%d %H:%M:%S")
            print(f'Время {data_now_format}. Ошибка {exc} в формуле {function_list_name[index]}.')


def table_clear():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    table_list = ['bdo', 'crossfire', 'dota2', 'eve_online', 'fall_guys', 'fortnite', 'hearthstone', 'leagueoflegends',
                  'rainbow', 'world_of_tanks']
    for table in table_list:
        cur.execute(f"DELETE FROM {table}")
        conn.commit()
    log.info(f'База данных очищена')
