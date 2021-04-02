# Packet permettant d'initialiser les valeurs en cas de mise à jour, pour éviter de réenvoyer d'anciens mail | initialise les bases de données des scans de site

import requests
from bs4 import BeautifulSoup

def GOOGLE_site_spe_terme1 () :
    requete = requests.get("https://sites.google.com/view/sciences-physiques-facile/terminale-sp%C3%A9")
    page = requete.content
    soup = BeautifulSoup(page, features="html.parser")

    desc = soup.find_all("p")
    n = 0
    desc_final = []
    while n < len(desc) :
        desc_final.append(str(desc[n].encode('utf-8')))
        n += 1
    return desc_final

def Padlet_ESC_SVT () :
    requete = requests.get("https://padlet.com/padlets/dwg0n1skdy/exports/feed.xml")
    page = str(requete.content)
    page = str(page)
    #print(type(page))

    page = page.split("   ")
    #print(page)
    #print(page[13])
    return str(page[13].encode('utf-8'))

def Padlet_Anglais () :
    requete = requests.get("https://padlet.com/padlets/w2g6cw4facefkhsw/exports/feed.xml")
    page = str(requete.content)
    page = str(page)
    #print(type(page))

    page = page.split("   ")
    #print(page)
    #print(page[13])
    return str(page[13].encode('utf-8'))

data = GOOGLE_site_spe_terme1()
data_file = open("LOGS_GS.txt", "r")
data_rls = data_file.readlines()
scale = len(data_rls)
data_file.close()
m = 0
data_file = open("LOGS_GS.txt", "w")
while m < len(data) :
   print(data[m])
   data_file.write(str(data[m])+"\n")
   m += 1
# ---------------------------------------------------------------------------------------- #
list_response_term = [Padlet_ESC_SVT(), Padlet_Anglais()]
list_path_term = ["LIST OF PATH"]

n = 0

while n < len(list_path_term) :
    change = open(list_path_term[n], "w")
    change = change.writelines(list_response_term[n])
    n += 1
