import sqlite3
import os

#*test de la database
conn= sqlite3.connect('db_concertavenir.sqlite')
cursor = conn.cursor()

cursor.execute('SELECT rowid,* FROM evenements')

print(cursor.fetchall())


# Close the cursor and the connection
cursor.close()
conn.close()


