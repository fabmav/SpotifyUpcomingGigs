#ce programme se connecte à l'API sowprog pour récupérer les concerts à venir 
#sur le périmètre des petites salles parisiennes


from func import shared, os,requests,json,base64,load_dotenv,DB
from func.shared import write_to_db_lite
from func.SowprogFunc import get_sowprog_full


load_dotenv()
NAME = os.getenv("nom_sowprog")
PWD = os.getenv("mdp_sowprog")

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

QUERY = '''INSERT INTO evenements (
            nom_evenement,
            artiste,
            date,
            salle,
            description_event,
            genre) VALUES (?,?,?,?,?,?);'''

result = get_sowprog_full(url,header)

write_to_db_lite(db=DB,query=QUERY,request_output=result)