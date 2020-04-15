import sqlite3

conn = sqlite3.connect('song_db.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE collection
          (id INTEGER PRIMARY KEY,
           title TEXT NOT NULL,
           artist TEXT,
           album TEXT,
           runtime TEXT NOT NULL,
           genre TEXT,
           rating TEXT,
           pathname TEXT NOT NULL,
           date_added TEXT NOT NULL,
           last_played TEXT)
          ''')

conn.commit()
conn.close()
