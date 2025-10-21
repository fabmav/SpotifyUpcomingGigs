# function dedicated to Mairie de Paris API

import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

def get_mdp_data(api_url,parameters) : 
    '''this functions queries Maire de Paris API to extract a list of concert
    input : mairie de paris API url and connexion parameters to filter concerts
    output : dictionnary with event id, url, text, date, location'''
    dico = {}
    result = requests.get(url=api_url,params=parameters)
    reponse=json.loads(result.content)

    for item in reponse : 
        mdp_id = item["id"]
        event_url = item["url"]
        event_lead_text = item["lead_text"]
        event_title = item["title"]
        event_desc = item["description"]
        event_date = item["date_start"]
        event_place = item["address_name"]
        dico[mdp_id] = [mdp_id,event_url,event_lead_text,event_title,event_desc,event_date,event_place]


    return dico

if __name__ =="__main__" : 
    None