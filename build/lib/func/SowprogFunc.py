#ce programme se connecte à l'API sowprog pour récupérer les concerts à venir 
#sur le périmètre des petites salles parisiennes
#* v2 : update de la requête de recherche sur l'api

import os
from func import shared
import os
import requests
import json
import base64
import re
from dotenv import load_dotenv

def get_sowprog_raw(url,header) : 
    test = requests.get(url=url,headers=header)
    print(f'''{test}''')
    reponse=json.loads(test.content)
    return json.dumps(reponse, indent=4)

def get_sowprog_lite(url,header) :
    liste=[] 
    test = requests.get(url=url,headers=header)
    print(f'''{test}''')
    reponse=json.loads(test.content)

    for item in reponse["eventDescription"] : 

        event_salle = item["location"]["name"]
        event_date = item["eventSchedule"]["startDate"]

        #TODO voir pour intégrer cela dans la requête
        if "artist" in item : 
            c = item["artist"]
            for artist in c : 
                event_artiste=artist["name"]
                liste.append(f'{event_salle} - {event_date} - {event_artiste}\r')
    return liste

def get_sowprog_full(url,header) :
    liste=[] 
    test = requests.get(url=url,headers=header)
    print(f'''{test}''')
    reponse=json.loads(test.content)

    for item in reponse["eventDescription"] : 

        event_salle = item["location"]["name"]
        event_date = shared.julian_date(item["eventSchedule"]["startDate"])
        event_description = item["event"]["description"]
        event_genre = item["event"]["eventStyle"]["label"]

        #TODO voir pour intégrer cela dans la requête
        if "artist" in item : 
            c = item["artist"]
            for artist in c : 
                event_artist=artist["name"]
                #! à revoir, respecter l'ordre des colonnes de la database
                temp=(event_artist,event_artist,event_date,event_salle,event_description,event_genre)
                liste.append(temp)
    return liste

if __name__ == "__main__" :
    None