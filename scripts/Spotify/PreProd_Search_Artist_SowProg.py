#ce code récupère le authorization code et le "refresh token" puis à partir de là récupère un refreshed token

import requests
import os
import base64
import json
from func import DB
from func.shared import fetch_from_db_lite,DICT_QUERY
from func.spotifyfunc import*
from datetime import*
from re import*
from time import sleep
from openai import OpenAI, api_key

from pydantic import BaseModel

OPENAI_KEY= os.getenv("OPENAI_KEY")
client = OpenAI(api_key=OPENAI_KEY)

class Artist(BaseModel) : 
    name : str
    spot_id : str
    spot_uri : str


#on charge les variable : les clés publiques et privées
load_dotenv()
client_id = os.getenv("SP_PUB_KEY")
client_secret = os.getenv("SP_PRIV_KEY")
refresh_token = os.getenv("REFRESH_TOKEN")

#les urls dont on va avoir besoin (ie les points d'accès des différentes requêtes)
auth_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'

#première étape avoir un access token valide
access_token = get_access_token(refresh_token,client_id,client_secret)

url = "https://api.spotify.com/v1/search"

#je définis une erreur pour les artistes non trouvés
def erreur_artiste(n,artiste) : 
    if n.status_code !=200 : 
        raise TypeError(f'''{artiste} non trouvé''')

#l'artiste que je cherche
# g_out = open('liste artiste sowprg nettoye.txt','r',encoding='UTF-8')
# h_out = open('liste uri sowprog.txt','w',encoding='UTF-8')

base_list = fetch_from_db_lite(DB,DICT_QUERY['query_uri'])

print(base_list[0])

dico={}
for item in base_list : 
    artiste = item[1]
    if REGEX_URI.match(item[2]) : 
        spotify_id = REGEX_URI.match(item[2])
        dico[item[0]] = spotify_id
    else : 

        #TODO : obtenir les éléments de la DB pour feed llm

        sleep(1)
        recherche_artiste=f'''artist:{artiste.strip()}'''

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': recherche_artiste,
        'type': 'artist',
        'limit': 10
    }
    try : 
        response = requests.get(url=url, headers=headers, params=params)
        data = response.json()
        erreur_artiste(response,artiste)
        list_search_artist = []
        for item in data["artists"]["items"] : 
            print(item)
            result = (item["name"],item["id"],item["uri"])
            list_search_artist.append(artiste)

        response = client.responses.parse(
            model="gpt-4.1",
            input =
                f'''based only on the list of artist and spotify uris in {list_search_artist}, find the 
                best match for the artists playing the following event : {event_name}, artist :{event_artist}, date : {event_date},
                venue : {event_venue}, event description : {event_description}.
                output : item in {list_search_artist} best matching the criteria'''
            text_format=Concert
            )

    except Exception as e : 
        print(f'''{e}, {item} non trouvé\n status serveur : {response.status_code}''')

#TODO : écrire les nouveaux résultats dans la DB