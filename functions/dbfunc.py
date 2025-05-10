import sqlite3
import os
from datetime import timezone,datetime

#*création et administration high level de la database des concerts à venir

DB = 'database/UpcomingGigs.sqlite'
TODAY = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

def open_db(func) : 
    def wrapper(*args,**kwargs) : 
        conn= sqlite3.connect(DB)
        cursor = conn.cursor()
        result = func(conn, cursor,*args,**kwargs) 
        cursor.close()
        conn.close()
        return result
    return wrapper

@open_db
def select_all(conn, cursor) : 
    cursor.execute('SELECT rowid,* FROM evenements')
    data = cursor.fetchall()
    return data

@open_db
def select_artist_null_uri(conn, cursor) : 
    cursor.execute('SELECT rowid, artiste FROM evenements WHERE uri_artiste = ""')
    data = cursor.fetchall()
    return data

@open_db
def delete_all(conn,cursor) : 
    conn.execute("""DELETE FROM evenements""")
    conn.commit()

#! gérer le today : probablement qu'il faut le calculer en paralèlle et le passer en julian date
@open_db
def delete_past_event(conn,cursor) : 
    conn.execute(f"""DELETE FROM evenements WHERE date<{TODAY}""")
    conn.commit()


if __name__ == "__main__" : 
    None