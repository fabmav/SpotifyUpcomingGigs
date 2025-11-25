#test API Mairie de Paris
from func import DB
import requests
import json
import os
from pydantic import BaseModel
from datetime import datetime
from func.MarieDeParisFunc import get_mdp_data
# import mistralai
from openai import OpenAI, api_key
from dotenv import load_dotenv
from func.shared import write_to_db_lite
import re

load_dotenv()

OPENAI_KEY= os.getenv("OPENAI_KEY")
client = OpenAI(api_key=OPENAI_KEY)

DATASET_ID ="que-faire-a-paris-"
URL = "https://opendata.paris.fr/api/explore/v2.1"
COMPLEMENT_URL = f"/catalog/datasets/{DATASET_ID}/exports/json"
URL_DEF=URL+COMPLEMENT_URL

PARAMS = {
    "DATASET_ID": DATASET_ID,
    "where": "qfap_tags like '*Concert*'"
#    "q":"trabendo"
}

class Concert(BaseModel) : 
      event_title : str
      artist_name : str
      venue : str
      event_date : datetime
      spotify_uri : str | None
      genre : str | None
      event_description : str

class Concert_List(BaseModel) : 
      concert : list[Concert]


result = get_mdp_data(URL_DEF,PARAMS)
result_list = []
print(len(result.keys()))
for count,item in enumerate(result.keys()) : 

                # output : one entry for each artist with "event title","artist name","venue","event date",
                # "spotify uri","event description","music genre"

    response = client.responses.parse(
            model="gpt-4.1",
            input =
                f'''based on the info from {result[item]} find artists playing in this concert or festival. 
                Then, find the spotify uri of these artists and find music genre.
                output : an entry for each separate artist with a structure matching a JSON obect with the following fields : "event title","artist name","venue","event date",
                "spotify uri","event description","music genre".
                ''',
            text_format=Concert
            )
    # print(response.output_parsed)
    prompt_result = response.output_parsed
    print(type(response.output_parsed))
    event_name = prompt_result.event_title
    event_artist = prompt_result.artist_name
    event_venue = prompt_result.venue
    event_date = prompt_result.event_date
    event_uri = prompt_result.spotify_uri
    event_desc = prompt_result.event_description
    event_genre = prompt_result.genre
    event = (event_name,event_artist,event_venue,event_date,event_uri,event_desc,event_genre)
    # print(event)
    if count%100 == 0 : 
         print(f'item {count}')
    result_list.append(event)
    # if count >20 : 
    #      break
liste_temp = []
print(len(result_list))
rech =re.compile(r'jazz|world|cuban|afro|classi',re.IGNORECASE)
for item in result_list :
    if item[6] == None : 
         pass
    elif rech.findall(item[6])!=[] : 
        pass
    else : 
         liste_temp.append(item)
result_list = liste_temp[::]
print(len(result_list))

QUERY = '''INSERT INTO evenements (
                nom_evenement,
                artiste,
                salle,
                date,
                uri_artiste,
                description_event,
                genre) VALUES (?,?,?,?,?,?,?);'''

write_to_db_lite(db=DB,query=QUERY,request_output=result_list)