from func import dbfunc
from func import sqlite3

conn= sqlite3.connect('database/UpcomingGigs.sqlite')
cursor = conn.cursor()

dbfunc.delete_all(conn, cursor)
