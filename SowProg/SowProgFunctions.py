#ce programme se connecte à l'API sowprog pour récupérer les concerts à venir 
#sur le périmètre des petites salles parisiennes
#* v2 : update de la requête de recherche sur l'api
import sys
sys.path.append('/SharedFunc')
from SharedFunc.shared import *
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
        event_date = julian_date(item["eventSchedule"]["startDate"])
        event_description = item["event"]["description"]
        event_genre = item["event"]["eventStyle"]["label"]

        #TODO voir pour intégrer cela dans la requête
        if "artist" in item : 
            c = item["artist"]
            for artist in c : 
                event_artist=artist["name"]
                temp=(event_artist,event_artist,event_date,event_salle,event_description,event_genre)
                liste.append(temp)
    return liste



if __name__ == "__main__" :
#les variables sont le fichier .env, il faut les charger
    load_dotenv()
    NAME = os.getenv("SOWPROG_PUBLIC")
    PWD = os.getenv("SOWPROG_PRIV")

    auth_string = NAME+":"+PWD
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    header ={

        "Accept": "application/json",
        "Authorization": "Basic " + auth_base64,
        "Accept": "application/json"
        
    }

    #recherche : event style : Pop Rock Folk ou Metal
    param_style="event.eventStyle.label=Metal&event.eventStyle.label=Pop%20%2F%20Rock%20%2F%20Folk"
    #recherche : localisation : on se base sur les zipcode : Paris et petite couronne nord est
    zipcode=[str(i) for i in range(75001,75021)]+["93100","93200","93400","92100"]
    param_geo=''.join([f"&location.contact.zipCode={code}" for code in zipcode])

    #ça nous permet d'obtenir la chaîne suivante
    url = f"https://agenda.sowprog.com/rest/v1_2/scheduledEvents/search?{param_style}{param_geo}"