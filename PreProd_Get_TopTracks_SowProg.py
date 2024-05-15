#ce code récupère le authorization code et le "refresh token" puis à partir de là récupère un refreshed token
#* je choisis un artist avec son id spécifique
#* je récupère ses top tracks
import requests
import os
import base64
import json
from MesFonctions_Spotify import*
from datetime import*
from re import*
from time import sleep
from random import randint

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

#les paramètres de la requête
headers = {
    'Authorization': f'Bearer {access_token}'
}
params = {
    'country': "FR"
}

#le fichier pour récupérer les uri des artistes
h_out=open("liste uri sowprog.txt",'r',encoding="UTF-8")
#le fichier d'output
g_out=open("liste uri tracks sowprog.txt",'w',encoding='UTF-8')
#le fichier de log des erreurs
f_out=open("liste sowprig Error Log.txt",'w',encoding='UTF-8')

dico={}

#définition d'une erreur pour tester les uri
def Test_Erreur_Playlist(n) : 
    if n == [] : 
        raise TypeError('Mauvaise uri')

for ligne in h_out : 
    #on parse le fichier test_tmaster_event_detail_2.txt en 4è position : l'artiste uri [3]
    # en 2è position ([1]) : le nom de l'artiste
    artiste_uri=re.search("(.+) - (.+)",ligne)[2].strip()
    artiste_nom=re.search("(.+) - (.+)",ligne)[1].strip()
    print(artiste_uri)

    url = f"https://api.spotify.com/v1/artists/{artiste_uri}/top-tracks"

    response = requests.get(url=url, headers=headers, params=params)
    data = response.json()
    #! ajouter du code pour gérer les réponses de l'api
    #! important de catcher les erreurs
    try : 
        liste=[i["id"] for i in data["tracks"]]
        Test_Erreur_Playlist(liste)
        dico[artiste_nom] = liste
    #en cas d'erreur on écrit dans le fichier d'error log
    except Exception as e : 
        print(f'''{artiste_uri} pour {artiste_nom} ne marche pas''')
        f_out.write(f'''{artiste_uri} pour {artiste_nom} ne marche pas\r''')


for i in dico.keys() : 
    print('------------------------------')
    print(i)
    temp=dico[i]
    print(temp)
    x=randint(0,len(temp)-1)
    print(x)
    g_out.write(f'spotify:track:{temp[x]}\r')

#*previous code in 'try :'
        # print(data["tracks"][0]["id"])
        # for i in data["tracks"] : 
        #     g_out.write(f'{artiste_nom} - {i["id"]}\r')

f_out.close()
h_out.close()
g_out.close()
