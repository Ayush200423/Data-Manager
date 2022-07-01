import sqlite3

conn = sqlite3.connect('database/usersinfo.db')
c = conn.cursor()