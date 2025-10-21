from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import time, sleep
import random
import re


#TODO cette liste de lien ne fonctionne pas.
#TODO scanner les liens du site et les matcher avec une liste de terme pour avoir plus de felxibilité
url_liste =['https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/indie',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/rock',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/alternative',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/indiepop',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/postpunk',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/indierock',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/punk',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/folk',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/metal',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/french_pop',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/poprock',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/garage',
            'https://dice.fm/browse/paris-5b23e8a0e63cc224a4c36a2d/music/gig/alt_rock']

liste=[]
for url in url_liste : 

    sleep(random.uniform(20,31))

    driver = webdriver.Edge()
    driver.get(url)

    sleep(random.uniform(1,5))
    autorize = driver.find_elements(By.CSS_SELECTOR,'.ch2-dialog-actions button')
    for auth in autorize : 
        if auth.text == 'Autoriser tous les cookies' :
            print('bouton cookie trouvé')
            print(auth.text)
            auth.click()
            print('bouton coockie cliqué')
    
    # Wait for the button to be clickable (you can adjust the timeout as needed)
    # wait = WebDriverWait(driver, 10)
    # button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cTuxKx')))

    sleep(random.uniform(1,5))

    print(driver.current_url)
    

#TODO n'affiche pas d'erreur si il ne trouve pas de bouton
    while True : 
        boutons = driver.find_elements(By.CSS_SELECTOR,'.kmEjJP')
        compteur=0
        for bouton in boutons : 
            # print(bouton.text)
            #TODO faire un regex sur le voir plus
            if bouton.text == 'VOIR PLUS' : 
                # print(bouton)
                print('Bouton voir plus trouvé')
                bouton.click()
                sleep(random.uniform(1,5))
                compteur+=1
        if compteur==0 : 
            break

    sleep(random.uniform(1,5))

    #*le css selector des artistes de l'event
    elements_name = driver.find_elements(By.CSS_SELECTOR,'.lpbnCo')
    #*le css selector de la date de l'event  
    elements_date = driver.find_elements(By.CSS_SELECTOR,'.krokMv')
    #*le css selector de la salle .VzsZc
    elements_salle = driver.find_elements(By.CSS_SELECTOR,'.bZgCvI')
    # elements_genre =   

    names = [element for element in elements_name]


    for elem in names:
        # print(f'''{elem.accessible_name}
        #         \r{elem.aria_role}\r{elem.id}\r
        #       {elem.location}\r{elem.location_once_scrolled_into_view}\r
        #       {elem.parent}\r{elem.rect}\r
        #       {elem.tag_name}\r{elem.shadow_root}\r{elem.size}''')
        liste.append(elem.text)
    driver.quit()
    # Close the browser

print(len(liste))
liste2=[]
for i in liste : 
    if i not in liste2 : 
        liste2.append(i)
liste=liste2[::]

print(len(liste))

f_out=open('liste_concert_dice.txt',mode='w',encoding='UTF-8')
for item in liste : 
    f_out.write(f'''{item}\r''')
f_out.close()