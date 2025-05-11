#Brouillon
import re
import os


liste=[]
with open('liste_concert_dice.txt','r',encoding='UTF-8') as fichier_dice : 
    for line in fichier_dice : 
        nom = line.rstrip('\n')
        liste.append(nom)
print(liste)

for i in liste : 
    if liste.count(i)>1 : 
        liste.remove(i)

#on supprime simplement : 
a_suppr=re.compile(r'[sS]unday [tT]ribute')
for index,i in enumerate(liste) : 
    if a_suppr.findall(i)!=[] : 
        liste.remove(i)

# on enlève les trucs du style 'dédé prod présente : '
rech=re.compile(r'.+: ')
for index,i in enumerate(liste) : 
    if rech.findall(i) !=[] : 
        new=re.split(rech,i)
        liste.remove(i)
        liste.insert(index,new[1])

# on enlève les trucs du style 'concert : '
rech=re.compile(r'[cC]oncert [:-•] ')
for index,i in enumerate(liste) : 
    if rech.findall(i) !=[] : 
        new=re.split(rech,i)
        liste.remove(i)
        liste.insert(index,new[1])

rech=re.compile(r' ?[\+|] ?')
compteur=1
while compteur >0 : 
    compteur=0
    for i in liste : 
        if rech.findall(i) !=[] : 
            compteur+=1
            new=re.split(rech,i)
            liste.remove(i)
            for line_up, j in enumerate(new) : 
                liste.append(j)

#on supprime les premières parties : 
for i in liste : 
    if i in ['1ere partie','1ère partie','première partie',r'[gG]uest'] : 
        print(i)
        liste.remove(i)

print('---------------------------------------------------------')
print(liste)

fichier=open('list_dice_nettoye.txt',mode='w',encoding='UTF-8')
for i in liste : 
    fichier.write(f'''{i}\r''')