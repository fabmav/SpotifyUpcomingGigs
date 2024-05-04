
#* ce script récupère les event ticket master.
#* il sauve dans "test_tmaster_event.txt" la réponse json globale
#* il sauve dans "test_tmaster_event_detail_2.txt" le nom des artistes et l'uri spotify

#import des modules : request pour interragir avec l'api ticketmaser
#dotenv pour récupérer la clé secrète de l'api
#os : pas utilisé mais doit permettre de choisir où stocker les output
#fonctions ticket master
#re pour travailler sur les donnéesuelles

import sqlite3
from requests import get
from dotenv import load_dotenv
import os
import json
from MesFonctionsTicketMaster import*
import re

load_dotenv()

#on récupère les clés
CLIENT_ID = os.getenv("TMASTER_PUB_KEY")
CLIENT_SECRET = os.getenv("TMASTER_PRIV_KEY")

def get_Tmaster_Query_total(url) : 
    reponse_tmaster = get(url=url)
    data_tmaster=reponse_tmaster.json()
    nb_page=data_tmaster["page"]["totalPages"]
    return nb_page

#les data dont on a besoin : 
#l'url de base de l'api ticket master
root_url = "https://app.ticketmaster.com/discovery/v2/"
#le end point pour récupérer des infos sur l'event
end_point = "events.json?"
#lee à ajouter pour ajouter la clé secrète
api_key=f'apikey={CLIENT_ID}'
#la recherche : un point sité dans paris centre : 48.8563763,2.351896
# radius de 12km
#? recerche locale et size : à préciser 
search_pre = "&latlong=48.8563763,2.3518962&radius=12&unit=km&countryCode=FR&locale=*&size=200&genreId="

#les fichiers que l'on va utiliser pour enregistrer l'output et faire les recherche
f_out = open("test_tmaster_event.txt",'w',encoding='UTF-8')

#le fichier dans lequel on va stocker les infos
#! on arrête d'écrire dans ce fichier
# g_out = open("test_tmaster_event_detail_2.txt",'w',encoding='UTF-8')

#le fichier contenant l'id des genres que l'on va parser
#TODO : remplacer par une query dans la table genre de la db
h_out = open("prod_tmaster_music_genre.txt",'r',encoding='UTF-8')

#la liste dans laquelle on va stocker les données à mettre dans la db
liste=[]

#step 1 : on choisit l'un des genre dans la liste

for ligne in h_out : 
    a=re.search("(.*) - (.+)",ligne)
    search=f'{search_pre}{a[2]}'

    #step 2 : on complète l'api
    url=root_url+end_point+api_key+search

    #step 3 : on trouve le nombre de page à parser
    x=0
    while x!=1 : 
        try :   
            nb_page = get_Tmaster_Query_total(url)
            print(f'nombre de page genre {a[1]} : {nb_page}')
            x=1
        except Exception as e :
            x=0



    #step 4 : on va itérer sur chaque page
    i=0
    while i <= nb_page : 
        #l'url complétée avec le nombre de page
        url_2 = f'{url}&page={i}'
        #la requête
        tmaster_query = get(url=url_2)
        print(f'Réponse serveur {tmaster_query}')
        data=tmaster_query.json()
        #les résultats brut sont écrits dans le fichier test_tmaster_event.txt
        f_out.write(json.dumps(data,indent=4))
        #on va trouver dans l'output json les champs contenant les infos cherché
        if "_embedded" in data : 
            for embedded in data["_embedded"]["events"] : 
                #récupérer la date
                try : 
                    event_date = embedded["dates"]["start"]["localDate"]
                except Exception as e : 
                    event_date=""
                event_genre = embedded["classifications"][0]["genre"]["name"]
                event_subgenre = embedded["classifications"][0]["subGenre"]["name"]
                a=embedded["_embedded"]
                # le nom de la salle  : 
                if "venues" in a : 
                    event_venue=a["venues"][0]["name"]
                # le nom du groupe
                if "attractions" in a : 
                    event_artist=a["attractions"][0]["name"]
                    # si il y a un lien spotify
                    if "externalLinks" in a["attractions"][0] : 
                        c=a["attractions"][0]["externalLinks"]
                        if "spotify" in c : 
                            d=c["spotify"]
                            artist_spotify_url=d[0]['url']
                            artist_spotify_uri=re.search("(.+)artist/(......................)",artist_spotify_url)
                            if artist_spotify_uri != None :
                                temp=(event_artist,event_artist,event_date,event_venue,artist_spotify_uri[2],event_genre)
                                liste.append(temp)
        i+=1

conn= sqlite3.connect('db_concertavenir.sqlite')
cursor = conn.cursor()
# Define the SQL statement to insert data into the table
insert_query = '''INSERT INTO evenements (
		nom_evenement,
		artiste,
		date,
        salle,
        uri_artiste,
        genre) VALUES (?,?,?,?,?,?);'''
# Execute the SQL statement to insert multiple rows of data
cursor.executemany(insert_query, liste)
# Commit the changes to the database
conn.commit()
# Close the cursor and the connection
cursor.close()
conn.close()



#on ferme les fichiers
f_out.close()
# g_out.close()
h_out.close()