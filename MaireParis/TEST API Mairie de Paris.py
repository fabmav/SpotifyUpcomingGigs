#test API Mairie de Paris

import requests
import json
import os
dataset_id ="que-faire-a-paris-"
url = "https://opendata.paris.fr/api/v2"
complement_url = f"/catalog/datasets/{dataset_id}/exports/json"
url_def=url+complement_url

parameters = {
    "dataset_id": dataset_id,
    "where": "tags like '*Concert*'"
#    "q":"trabendo"
}

test = requests.get(url=url_def,params=parameters)

reponse=json.loads(test.content)
dump = json.dumps(reponse, indent=4)


f_out = open("test_api_mairiedeparis.txt",'w',encoding='UTF-8')
f_out.write(dump)
f_out.close

liste = []
for i in reponse : 
    liste.append(i["address_name"])
print(set(liste))