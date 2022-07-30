from time import sleep
import telebot
import logging
from setting import function_list, photo_list, bot, CHANNEL_NAME, time1
import schedule
from threading import Thread

# logger = telebot.logger
# logger.setLevel(logging.DEBUG)


# def schedule_checker():
#     while True:
#         schedule.run_pending()
#         sleep(1)


# def send_news(data_list, photo):
#     for news_game in data_list:
#         with open(photo, 'rb') as f:
#             bot.send_photo(CHANNEL_NAME, f, caption=news_game, parse_mode="HTML")


# def run():
#     for index in range(len(function_list)):
#         try:
#             news_data_list = function_list[index]
#             send_news(news_data_list, photo_list[index])
#         except Exception as exc:
#             print(f'Ошибка {exc} в формуле {function_list[index]}')


# schedule.every().day.at(time1).do(run)

# Thread(target=schedule_checker).start()
