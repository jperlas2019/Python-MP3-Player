import sqlite3

conn = sqlite3.connect('student_db.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE collection
          ''')

conn.commit()
conn.close()
