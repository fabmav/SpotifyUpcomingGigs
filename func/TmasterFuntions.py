
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
from datetime import datetime,timezone

load_dotenv()

logger = logging.getLogger(__name__)

#getting ticket master key. Only the public key is needed for this script
CLIENT_ID = os.getenv("TMASTER_PUB_KEY")
print(CLIENT_ID)

#getting the date
TODAY = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

#getting the genres 
GENRE_FILE = 'functions/TicketMaster/tmaster_genre.txt'
        

#to get the total page of a request
def get_tmaster_query_total(url) : 
    '''this function gets the numer of pages for a request to Ticket Master API url.
    the result can be used in a loop to fetch results of all the pages by adding page number in the query url'''
    reponse_tmaster = get(url=url)
    data_tmaster=reponse_tmaster.json()
    nb_page=data_tmaster["page"]["totalPages"]
    logger.info(f'''total page number for {url} : \nStatus : {reponse_tmaster.status_code}
                \nReason{reponse_tmaster.reason} \nPage number : {nb_page}''')
    return nb_page


#to get a raw extract of tha data in a text file
def get_tmaster_raw(page,url) :
    '''this function outputs the whole query result in a file as indented json'''
    url_query = f'{url}&page={page}'
    #la requête
    tmaster_query = get(url=url_query)
    logger.info(f'''Query tmaster_raw total page number for {url} : \nStatus : {tmaster_query.status_code}
                \nReason{tmaster_query.reason}''')
    print(f'Réponse serveur tmaster_raw : {tmaster_query.status_code,tmaster_query.reason}')
    data=tmaster_query.json()
    return json.dumps(data,indent=4)


def get_tmaster_data_old(page,url) :
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


def get_tmaster_data_full(page,url) :
    liste=[]
    url_query = f'{url}&page={page}'
    #la requête
    tmaster_query = get(url=url_query)
    print(f'Réponse serveur {tmaster_query}')
    data=tmaster_query.json()
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
    return liste


#DECORATORS
def write_to_file(file) : 
    def decorator(func) : 
        def wrapper(*args,**kwargs) : 
            result = func(*args,**kwargs)
            with open(file,'a',encoding='UTF-8') as file_write : 
                for i in result : 
                    file_write.write(f'{i}\n')
        return wrapper
    return decorator


def json_write_to_file(file) : 
    def decorator(func) : 
        def wrapper(*args,**kwargs) : 
            result = func(*args,**kwargs)
            try : 
                logger.info(f'''result json write to file  : {result[0:30]}\n
                            longueur fichier : {len(result)}''')
            except Exception as e : 
                logger.info(f'result : {result, len(result)}')
            with open(file,'a',encoding='UTF-8') as file_write : 
                    file_write.write(result)
        return wrapper
    return decorator

#les data dont on a besoin : 
#l'url de base de l'api ticket master
ROOT_URL = "https://app.ticketmaster.com/discovery/v2/"
#le end point pour récupérer des infos sur l'event
END_POINT = "events.json?"
#le texte à ajouter pour ajouter la clé secrète
API_KEY=f'apikey={CLIENT_ID}'
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
def tmaster_main(baseUrl,genreFile, funcQuery) :
    '''this function retrieves genres stored in a text file,executes a query to get total number of page from Ticket Master, 
    then executes the desired query (the url) and generate an outputs in the desired format
    url : query url
    genreFile : the file where genres are stored
    funcDeco : the decorator generating the output
    funcQuery : the function parsing the json output'''
    #step 1 : on choisit l'un des genre dans la liste

    liste =[]

    #TODO à encapsuler dans une fonction spécifique à ticket master
    for ligne in genreFile : 
        genre=re.search("(.*) - (.+)",ligne)
        search=f'{search_pre}{genre[2]}'
        logger.info(f'genre : {genre[1]}, id : {genre[2]}')

        #step 2 : on complète l'api
        query_url=baseUrl+search
        logger.info(f'url query : {query_url}')

        #step 3 : on trouve le nombre de page à parser
        compteur = 0
        while True : 
            compteur+=1
            try : 
                nb_page = get_tmaster_query_total(query_url)
                print(f'nombre de page genre {genre[1]} : {nb_page}')
                logger.info(f'nombre de page genre {genre[1]} : {nb_page}')
                break
            except Exception as e : 
                if compteur == 5 : 
                    print("echec obtention nombre de page")
                    nb_page = 0
                    break
        print(nb_page)

        #step 4 : on va itérer sur chaque page
        #! à craquer : soit il y a 0 pages et j'ai une réponse de 325 caractères donc 1 page
        #! soit il y a 1,2 ou n pages et de la page 0 à la page n-1 j'ai ce qui m'intéresse
        #! et la page n est une sorte de wrap up de 885 / 886 caractères
        i=0
        while i <= nb_page : 
            #l'url complétée avec le nombre de page
            liste_temp = funcQuery(i,query_url)
            liste.extend(liste_temp)
            i+=1
    return liste

#on ferme les fichiers
#f_out.close()
#g_out.close()
#h_out.close()

if __name__ == "__main__" : 
    None