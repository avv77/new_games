import sqlite3


conn = sqlite3.connect(r'D:\PyCharmProject\News_Games\db\news.db')
cur = conn.cursor()

table_list = ['bdo', 'crossfire', 'dota2', 'eve_online', 'fall_guys', 'fortnite', 'hearthstone', 'leagueoflegends',
              'rainbow', 'world_of_tanks']

for table in table_list:
    cur.execute(f"DELETE FROM {table}")
    conn.commit()
