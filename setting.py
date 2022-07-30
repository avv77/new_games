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
import telebot


BOT_TOKEN_1 = '5188856877:AAEBjiodczlrQXx1QCxm8bRU8XeFkCS9krs'

function_list = [crossfire(), eve_online(), fortnite(), dota2(), leagueoflegends(), rainbow(), hearthstone(),
                 fall_guys(), bdo_online(), world_of_tanks()]

photo_list = ['img/crossfire.jpg', 'img/eve-online.jpg', 'img/fortnite.jpg', 'img/dota2.jpg',
              'img/league-of-legends.jpg', 'img/rainbow.jpg', 'img/hearthstone.jpg', 'img/Fallguys.jpg',
              'img/bdo_online.jpg', 'img/wot.jpg']

CHANNEL_NAME = '@game_online_news'

bot = telebot.TeleBot(BOT_TOKEN_1)

time1 = "00:42:00"
