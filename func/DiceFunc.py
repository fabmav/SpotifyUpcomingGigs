#Brouillon
import re
import datetime

MONTH = {'janv' : 1,
        'févr' : 2,
        'mars' : 3, 
        'avr' : 4, 
        'mai' : 5,
        'juin' : 6,
        'juil' : 7,
        'août' : 8,
        'sep' : 9,
        'oct' : 10,
        'nov' : 11,
        'déc' : 12}

DAY = {'lun' : 1,
       'mar' : 2,
       'mer' : 3,
       'jeu' : 4,
       'ven' : 5,
       'sam' : 6,
       'dim' : 7}


def regex_dice_list (liste) : 
    '''ensemble of regex used to edit dice concert list. The aim is to split event name into the different artist in the event
        while getting rid of unnecessary text.
        dice concert list is as follow : \n
        event \n
        artist\n
        venue\n
        date\n
        '''

    #event which are fully suppressed : 
    a_suppr=re.compile(r'[sS]unday [tT]ribute')
    for index,item in enumerate(liste) : 
        if a_suppr.findall(item[1])!=[] : 
            liste.remove(item)
    
    # removing "xxx present : "
    rech=re.compile(r'.+: ')
    for index,item in enumerate(liste) : 
        if rech.findall(item[1]) !=[] : 
            new_item=[item[0],re.split(rech,item[1])[1],item[2],item[3]]
            liste.remove(item)
            liste.insert(index,new_item)

    # on enlève les trucs du style 'concert : '
    rech=re.compile(r'[cC]oncert [-:+•—] ')
    for index,item in enumerate(liste) : 
        if rech.findall(item[1]) !=[] : 
            new_item=[item[0],re.split(rech,item[1])[1],item[2],item[3]]
            liste.remove(item)
            liste.insert(index,new_item)

    #suppression caractères spéciaux qui délimitent les noms ajouts de chaque artiste dans la liste
    rech=re.compile(r' ?[\+\|•\,\-\◆] ?')
    compteur=1
    while compteur >0 : 
        compteur=0
        for item in liste : 
            if rech.findall(item[1]) !=[] : 
                compteur+=1
                new_item=re.split(rech,item[1])

                for line_up, new in enumerate(new_item) : 
                    print(item)
                    print(item[1])
                    print(new_item)
                    liste.append([item[0],new,item[2],item[3]])
                liste.remove(item)

    #on supprime les premières parties : 
    rech= re.compile(r"1[eè]re partie|première partie|[gG]uest")
    for index,item in enumerate(liste) : 
        if rech.findall(item[1])!=[] : 
            liste.remove(item)


    a_suppr=re.compile(r'[fF]estival')
    for index,item in enumerate(liste) : 
        if a_suppr.findall(item[1])!=[] : 
            liste.remove(item)

    return liste



def regex_dice_base (liste) : 
    '''ensemble of regex used to edit dice concert list'''
    #suppression des doublons
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
    rech=re.compile(r'[cC]oncert [-:+•—] ')
    for index,i in enumerate(liste) : 
        if rech.findall(i) !=[] : 
            new=re.split(rech,i)
            liste.remove(i)
            liste.insert(index,new[1])

    #suppression caractères spéciaux qui délimitent les noms ajouts de chaque artiste dans la liste
    rech=re.compile(r' ?[\+|•,-◆] ?')
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
    rech= re.compile(r"1[eè]re partie|première partie|[gG]uest")
    for index,i in enumerate(liste) : 
        if rech.findall(i)!=[] : 
            liste.remove(i)


    a_suppr=re.compile(r'[fF]estival')
    for index,i in enumerate(liste) : 
        if a_suppr.findall(i)!=[] : 
            liste.remove(i)

    return liste


def get_dice_date(date) : 
    search = re.compile(r'[\w\.]{4}[ ][\d]{1,2}[ ][\w\.]{3,4}[ \d]*')
    search_result = search.match(date)
    if search_result == None : 
        date_def = date
    else : 
        date_parsed = re.split(pattern=r' |\. ?',string=date)
        if date_parsed[-1] =='' : 
            date_parsed.pop(-1)
        year_def = datetime.datetime.now().year if len(date_parsed)==3 else int(date_parsed[3])
        date_int = int(date_parsed[1])
        date_def = datetime.datetime(year=year_def,month=MONTH[date_parsed[2]],day=int(date_parsed[1]))
    
    return date_def

if __name__ == '__main__' :
    None