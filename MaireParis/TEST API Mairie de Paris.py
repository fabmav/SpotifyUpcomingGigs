#test API Mairie de Paris

import requests
import json
import os
dataset_id ="que-faire-a-paris-"
url = "https://opendata.paris.fr/api/v2"
complement_url = f"/catalog/datasets/{dataset_id}/records"
url_def=url+complement_url

parameters = {
    "dataset_id": dataset_id,
    "q":"trabendo"
}

test = requests.get(url=url_def,params=parameters)
print(test)
reponse=json.loads(test.content)
print(reponse)

f_out = open("test_api_mairiedeparis.txt",'w',encoding='UTF-8')
f_out.write(reponse)
f_out.close