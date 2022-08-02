from functions import schedule_checker, run
from setting import time1, time2, time3, time4, time5, time6, time7, time8, time9
import schedule
from threading import Thread


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
