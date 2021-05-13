# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# INIT VALUE PAGE
# UTF-8
# Version : V2.0

# Packet permettant d'initialiser les valeurs en cas de mise à jour, pour éviter de réenvoyer d'anciens mail | initialise les bases de données des scans de site

import requests
from bs4 import BeautifulSoup
import extract_info

# Même fonctionnement que le programme v2.0.main au niveau de la récupération des informations. Ici, on récupère toutes les données sur les sites cibles et on actualise les données dans les fichiers LOGS
def Google_Site (link) :
    requete = requests.get(link)
    page = requete.content
    soup = BeautifulSoup(page, features="html.parser")

    desc = soup.find_all("p", {'class': "CDt4Ke zfr3Q"})
    n = 0
    desc_final = []
    while n < len(desc):
        desc_final.append(str(desc[n].encode('utf-8')) + "\n")
        n += 1
    print(desc_final)
    return desc_final

def Padlet (link) :
    requete = requests.get(link)
    page = str(requete.content)
    page = str(page)

    page = page.split("   ")
    # print(page)
    # print(page[13])

    time_code = str(page[13].encode('utf-8'))

    return time_code

try :
    list_path_GS = extract_info.extract_path("GS")
    list_path_PD = extract_info.extract_path("PD")

    GS_list = extract_info.extract_links("GS")
    PD_list = extract_info.extract_links("PD")

    for i in range (2) :
        n = 0
        if i == 0 :
            while n < len(list_path_GS) :
                data = Google_Site(GS_list[n])
                file = open(list_path_GS[n], "w")
                file.writelines(data)
                file.close()
                n += 1

        if i == 1 :
            while n < len(list_path_PD) :
                data = Padlet(PD_list[n])
                file = open(list_path_PD[n], "w")
                file.writelines(data)
                file.close()
                n += 1
except SystemError as err:
    print("ERROR #011, error during the init of values (please refer you at the ERROR_TYPE.txt file)")
