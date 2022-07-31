from time import sleep
import logging
from games.FALL_GUYS import fall_guys
from games.HEARTHSTONE import hearthstone
from games.RAINBOW import rainbow
from games.bdo import bdo_online
from games.crossfire import crossfire
from games.dota2 import dota2
from games.eve_online import eve_online
from games.fortnite import fortnite
from games.leagueoflegends import leagueoflegends
from games.worldoftanks import world_of_tanks
from setting import CHANNEL_NAME, time1, BOT_TOKEN_1, time2, time3, time4, time5, time6, time7, time8, time9
import schedule
from threading import Thread
import telebot

bot = telebot.TeleBot(BOT_TOKEN_1)

logger = telebot.logger
logger.setLevel(logging.DEBUG)

function_list = [crossfire, eve_online, fortnite, dota2, leagueoflegends, rainbow, hearthstone,
                 fall_guys, bdo_online, world_of_tanks]

photo_list = ['img/crossfire.jpg', 'img/eve-online.jpg', 'img/fortnite.jpg', 'img/dota2.jpg',
              'img/league-of-legends.jpg', 'img/rainbow.jpg', 'img/hearthstone.jpg', 'img/Fallguys.jpg',
              'img/bdo_online.jpg', 'img/wot.jpg']


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
            send_news(news_data_list, photo_list[index])
        except Exception as exc:
            print(f'Ошибка {exc} в формуле {function_list[index]}')


schedule.every().day.at(time1).do(run)
schedule.every().day.at(time2).do(run)
schedule.every().day.at(time3).do(run)
schedule.every().day.at(time4).do(run)
schedule.every().day.at(time5).do(run)
schedule.every().day.at(time6).do(run)
schedule.every().day.at(time7).do(run)
schedule.every().day.at(time8).do(run)
schedule.every().day.at(time9).do(run)

Thread(target=schedule_checker).start()
