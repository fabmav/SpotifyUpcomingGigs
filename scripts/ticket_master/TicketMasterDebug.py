#extraction of raw ticket master query
import os
print(os.getcwd())
from func import requests, load_dotenv, os, json, re, sqlite3, logging, datetime, timezone, DB
from func.TmasterFuntions import tmaster_main, get_tmaster_raw
from func.shared import write_to_db_lite

#getting the date
TODAY = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

logger = logging.getLogger(__name__)
logging.basicConfig(filename=f'log/spotify_upcoming_gigs{TODAY}.log', level=logging.INFO) 

load_dotenv()

#getting ticket master key. Only the public key is needed for this script
CLIENT_ID = os.getenv("TMASTER_PUB_KEY")

#getting the genres 
GENRE_FILE = 'scripts/ticket_master/tmaster_genre.txt'
genres = open(GENRE_FILE,'r',encoding='UTF-8')

ROOT_URL = "https://app.ticketmaster.com/discovery/v2/"
#le end point pour récupérer des infos sur l'event
END_POINT = "events.json?"
#le texte à ajouter pour ajouter la clé secrète
API_KEY=f'apikey={CLIENT_ID}'
#la recherche : un point sité dans paris centre : 48.8563763,2.351896
base_url=ROOT_URL+END_POINT+API_KEY
# radius de 12km
#search_pre = "&latlong=48.8563763,2.3518962&radius=12&unit=km&countryCode=FR&locale=*&size=200&genreId="


result = tmaster_main(baseUrl=base_url,genreFile=genres,funcQuery=get_tmaster_raw)

with open(file='log/tmaster_raw.txt',mode='w',encoding='UTF-8') as file : 
    for line in result : 
        file.write(line)