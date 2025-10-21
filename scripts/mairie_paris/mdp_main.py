#test API Mairie de Paris

import requests
import json
import os
from func.MarieDeParisFunc import get_mdp_data
import mistralai
from openai import OpenAI, api_key
from dotenv import load_dotenv

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

test = get_mdp_data(URL_DEF,PARAMS)

for count,item in enumerate(test.keys()) : 

    response = client.responses.create(
            model="gpt-4.1",
            input=f'based on the info from {test[item]} find the artists playing in this concert or festival. Then, find the spotify uri of these artists. output : python list with ["artist name","spotify uri"]. No explanations. No extra text, list only'
        )
    print(response.output_text)
    if count>5 :
            break
