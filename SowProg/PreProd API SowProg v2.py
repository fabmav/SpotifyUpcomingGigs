#ce programme se connecte à l'API sowprog pour récupérer les concerts à venir 
#sur le périmètre des petites salles parisiennes
#* v2 : update de la requête de recherche sur l'api
import os
import requests
import json
import base64
import re
from dotenv import load_dotenv

#les variables sont le fichier .env, il faut les charger
load_dotenv()
nom = os.getenv("nom_sowprog")
mdp = os.getenv("mdp_sowprog")

auth_string = nom+":"+mdp
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

test = requests.get(url=url,headers=header)
print(f'''{test}''')
reponse=json.loads(test.content)

reponse_format = json.dumps(reponse, indent=4)

f_out = open("test_sowprog_scheduledEvent.txt",'w',encoding='UTF-8')
f_out.write(reponse_format)
f_out.close

f_out_2 = open("test_sowprog_scheduledEvent_location_artist.txt",'w',encoding='UTF-8')
for item in reponse["eventDescription"] : 

    event_salle = item["location"]["name"]
    event_date = item["eventSchedule"]["startDate"]

    #TODO voir pour intégrer cela dans la requête
    if "artist" in item : 
        c = item["artist"]
        for artist in c : 
            event_artiste=artist["name"]
            f_out_2.write(f'{event_salle} - {event_date} - {event_artiste}\r')

f_out_2.close()
