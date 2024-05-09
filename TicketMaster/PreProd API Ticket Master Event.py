
#* this script gets upcoming gigs in Paris France and its surroundings
#* il sauve dans "test_tmaster_event.txt" la réponse json globale
#* il sauve dans "test_tmaster_event_detail_2.txt" le nom des artistes et l'uri spotify

#import des modules : request pour interragir avec l'api ticketmaser
#dotenv pour récupérer la clé secrète de l'api
#re pour travailler sur les données textuelles

from requests import get
from dotenv import load_dotenv
import os
import json
import re
import sqlite3
import logging

load_dotenv()

logger = logging.getLogger(__name__)

#on récupère les clés
CLIENT_ID = os.getenv("TMASTER_PUBLIC")
#client_secret = os.getenv("TMASTER_PRIV_KEY")

#to get the total page of a request
def get_tmaster_query_total(url) : 
    reponse_tmaster = get(url=url)
    data_tmaster=reponse_tmaster.json()
    nb_page=data_tmaster["page"]["totalPages"]
    logger.info(f'total page number for {url} : {nb_page}')
    return nb_page

#to get a raw extract of tha data in a text file
def get_tmaster_raw(page,url,file) :
    url_query = f'{url}&page={page}'
    #la requête
    tmaster_query = get(url=url_query)
    print(f'Réponse serveur {tmaster_query}')
    data=tmaster_query.json()
    #les résultats brut sont écrits dans le fichier test_tmaster_event.txt
    with open(file,'w') as f_out : 
        f_out.write(json.dumps(data,indent=4))

def get_tmaster_data(page,url) :
    liste=[]
    url_query = f'{url}&page={page}'
    #la requête
    tmaster_query = get(url=url_query)
    print(f'Réponse serveur {tmaster_query}')
    data=tmaster_query.json()
    #on va trouver dans l'output json les champs contenant les infos cherché
    if "_embedded" in data : 
        for embedded in data["_embedded"]["events"] : 
            embedded_stp2=embedded["_embedded"]
            # le nom du groupe
            if "attractions" in embedded_stp2 : 
                b=embedded_stp2["attractions"][0]
                if "name" in b : 
                    e=b["name"]
                else : 
                    e="empty"
                # si il y a un lien spotify
                if "externalLinks" in b : 
                    c=b["externalLinks"]
                    if "spotify" in c : 
                        d=c["spotify"]
                        f=d[0]['url']
                        g=re.search("(.+)artist/(......................)",f)
                        if g !=None : 
                            liste.append(f'{e} - {g[2]}\r')

    return liste

def write_to_file(file) : 
    def decorator(func) : 
        def wrapper(*args,**kwargs) : 
            result = func(*args,**kwargs)
            with open(file,'a',encoding='UTF-8') as file_write : 
                for i in result : 
                    file_write.write(f'{i}\n')
        return wrapper
    return decorator


def write_to_db(db,data) : 
    conn= sqlite3.connect(db)
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
    cursor.executemany(insert_query, data)
    # Commit the changes to the database
    conn.commit()
    # Close the cursor and the connection
    cursor.close()
    conn.close()

#les data dont on a besoin : 
#l'url de base de l'api ticket master
root_url = "https://app.ticketmaster.com/discovery/v2/"
#le end point pour récupérer des infos sur l'event
end_point = "events.json?"
#le texte à ajouter pour ajouter la clé secrète
api_key=f'apikey={CLIENT_ID}'
#la recherche : un point sité dans paris centre : 48.8563763,2.351896
# radius de 12km
search_pre = "&latlong=48.8563763,2.3518962&radius=12&unit=km&countryCode=FR&locale=*&size=200&genreId="

#les fichiers que l'on va utiliser pour enregistrer l'output et faire les recherche
#f_out = open("test_tmaster_event.txt",'w',encoding='UTF-8')
#le fichier dans lequel on va stocker les infos
#g_out = open("test_tmaster_event_detail_2.txt",'w',encoding='UTF-8')
#le fichier contenant l'id des genres que l'on va parser
#h_out = open("tmaster_genre.txt",'r',encoding='UTF-8')

#! voir à quel niveau on écrit le code
def tmaster_main() :
    #step 1 : on choisit l'un des genre dans la liste

    for ligne in h_out : 
        genre=re.search("(.*) - (.+)",ligne)
        search=f'{search_pre}{genre[2]}'

        #step 2 : on complète l'api
        url=root_url+end_point+api_key+search

        #step 3 : on trouve le nombre de page à parser
        compteur = 0
        while True : 
            compteur+=1
            try : 
                nb_page = get_tmaster_query_total(url)
                print(f'nombre de page genre {genre[1]} : {nb_page}')
                break
            except Exception as e : 
                if compteur == 5 : 
                    print("echec obtention nombre de page")
                    break


        #step 4 : on va itérer sur chaque page
        i=1
        while i <= nb_page : 
            #l'url complétée avec le nombre de page
            write_to_file('TicketMaster/test.txt')(get_tmaster_data)(i,url)
            i+=1

#on ferme les fichiers
#f_out.close()
#g_out.close()
#h_out.close()

if __name__ == "__main__" : 
    #on récupère les clés
    CLIENT_ID = os.getenv("TMASTER_PUBLIC")
    #client_secret = os.getenv("TMASTER_PRIV_KEY")
    
    #les data dont on a besoin : 
    #l'url de base de l'api ticket master
    root_url = "https://app.ticketmaster.com/discovery/v2/"
    #le end point pour récupérer des infos sur l'event
    end_point = "events.json?"
    #le texte à ajouter pour ajouter la clé secrète
    api_key=f'apikey={CLIENT_ID}'
    #la recherche : un point sité dans paris centre : 48.8563763,2.351896
    # radius de 12km
    search_pre = "&latlong=48.8563763,2.3518962&radius=12&unit=km&countryCode=FR&locale=*&size=200&genreId="
    print(os.getcwd())
    h_out = open("TicketMaster/tmaster_genre.txt",'r',encoding='UTF-8')

    fichier = "test.txt"

    tmaster_main() 