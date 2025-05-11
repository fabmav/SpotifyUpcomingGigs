#ce code récupère le authorization code et le "refresh token" puis à partir de là récupère un refreshed token

import requests
import os
import base64
import json
from MesFonctions_Spotify import*
from datetime import*
from re import*
from time import sleep

#on charge les variable : les clés publiques et privées
load_dotenv()
client_id = os.getenv("SP_PUB_KEY")
client_secret = os.getenv("SP_PRIV_KEY")

#les urls dont on va avoir besoin (ie les points d'accès des différentes requêtes)
auth_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'

#le refresh token
f_out = open("Token_Spotify.txt",'r',encoding='UTF-8')
refresh_token = f_out.readline()

#première étape avoir un access token valide
access_token = get_refresh_token(refresh_token,client_id,client_secret)

url = "https://api.spotify.com/v1/search"

#je définis une erreur pour les artistes non trouvés
def erreur_artiste(n,artiste) : 
    if n.status_code !=200 : 
        raise TypeError(f'''{artiste} non trouvé''')

#l'artiste que je cherche
g_out = open('liste artiste sowprg nettoye.txt','r',encoding='UTF-8')
h_out = open('liste uri sowprog.txt','w',encoding='UTF-8')

dico={}
for artiste in g_out : 
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
        for item in data["artists"]["items"] : 
            if artiste.strip() in [item["name"],
                            item["name"].upper(),
                           item["name"].lower(),
                           item["name"][0].upper()+item["name"][1:].lower()] : 
                print(item["name"])
                compteur=1
                if item["name"] in dico.keys() : 
                    dico[item["name"]+str(compteur)]=item["id"]
                    compteur+=1
                else :
                    dico[item["name"]]=item["id"]
            # else : 
            #     print(f'''{artiste} non trouvé\n {len(artiste)}\n {item["name"][0].upper()+item["name"][1:].lower()}\n''')
    except Exception as e : 
        print(f'''{e}, {item} non trouvé\n status serveur : {response.status_code}''')

for i in dico.keys() : 
    temp=dico[i]
    h_out.write(f'{i} - {temp}\r')

f_out.close()
g_out.close()
h_out.close()