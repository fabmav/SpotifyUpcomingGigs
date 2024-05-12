import sqlite3
import os

#*création et administration high level de la database des concerts à venir
conn= sqlite3.connect('db_concertavenir.sqlite')
cursor = conn.cursor()

conn.execute("""CREATE TABLE evenements (
		nom_evenement text,
		artiste text,
		date text,
        salle text,
        uri_artiste text,
        image_artiste blob,
        description_artiste text,
        description_event text,
        genre text
	)""")

conn.commit()

# Fermer le curseur et la connexion
cursor.close()
conn.close()


