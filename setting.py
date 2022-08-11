CHANNEL_NAME = '@game_online_news'

time0 = "04:30:00"
time1 = "05:00:00"
time2 = "07:00:00"
time3 = "09:00:00"
time4 = "11:00:00"
time5 = "13:00:00"
time6 = "15:00:00"
time7 = "17:00:00"
time8 = "18:00:00"
time9 = "20:35:00"

db = r'/app/db/news.db'

log1 = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "my_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'my_formatter'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
