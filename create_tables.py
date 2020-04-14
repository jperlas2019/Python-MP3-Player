import sqlite3

conn = sqlite3.connect('song_db.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE collection
          (title TEXT PRIMARY KEY,
           artist TEXT,
           album TEXT,
           duration TEXT NOT NULL,
           genre TEXT,
           rating TEXT,
           pathname TEXT NOT NULL)
          ''')

conn.commit()
conn.close()
