# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# MODULE PAGE
# UTF-8
# Version : V2.0

# Packet permettant d'extraire les données des utilisateurs stockées dans le fichier client

import returnCode
import requests
from bs4 import BeautifulSoup

# Bloc d'extraction des données pour un utilisateur
def info_user (name) :
    #print("Starting extract ...")
    path = str("users.txt")
    get_data = open(path, "r")
    all_data = get_data.readlines()

    n = int(0)
    ID = []
    scale = len(all_data)

    while n < scale :
        data = all_data[n]
        list_data = data.split(";")
        if list_data[1] == name :
            #print("MATCH ID="+list_data[0])
            ID.append(str(list_data[0]))
        n += 1

    if len(ID) > 1 :
        #print("[!] DUPLICATE NAME")
        return None
    elif len(ID) == 1 :
        info_ID = all_data[int(ID[0])-1]
        list_ID = str(info_ID).split(";")
        data_ID = list_ID[-1]
        #print(name + " | DATA=" + data_ID[:-1])
        return list_ID
    else :
        #print("[!] NO MATCH IN THE DATABASE")
        return None

# Bloc d'extraction des liens contenus dans le fichier dont on donne le chemin d'accès (ici, le fichier contenant les liens vers les sites à scanner)
def extract_texte (path) :
    file = open(path, "r")
    links = file.readlines()
    list_links = []
    for i in range(0, len(links)) :
        value = links[i]
        if value[-1:] == "\n" :
            list_links.append(str(value[:-1]))
        else :
            list_links.append(value)
    file.close()
    return list_links

# Bloc d'extraction en fonction du mode, des mails, noms et données de chaque utilisateur
def extract_fromDataBase (mode) :
    path_dataBase = str("users.txt")
    open_dataBase = open(path_dataBase, "r")
    all_data = open_dataBase.readlines()
    scale_dataBase = len(all_data)

    users_name = []
    users_email = []
    users_data = []

    a = int(0)

    while a < scale_dataBase:
        data_user = all_data[a].split(";")
        users_name.append(data_user[1])
        if data_user[-1][-1] == "\n" :
            users_email.append(data_user[-1][:-1])
        else :
            users_email.append(data_user[-1])
        users_data.append(data_user[-2])
        a += 1

    if mode == "name" :
        return users_name
    elif mode == "email" :
        return users_email
    elif mode == "data" :
        return users_data
    else :
        print("[!] MODE IS NOT CORRECT")
        return []

# Bloc d'extraction des sites contenus dans la base de donnée
def extract_sites () :
    file = open("sites_list.txt", "r")
    all_data = file.readlines()
    scale = len(all_data)
    format_list = []

    for i in range(scale) :
        #print(all_data[i])
        data_split = all_data[i].split(";")
        if data_split[0] == "GS":
            if data_split[1][-1] == "\n" :
                format_list.append(str("Google Site ({})").format(data_split[1][:-1]))
            else :
                format_list.append(str("Google Site ({})").format(data_split[1]))
        elif data_split[0] == "PD" :
            if data_split[1][-1] == "\n" :
                format_list.append(str("Padlet ({})").format(data_split[1][:-1]))
            else :
                format_list.append(str("Padlet ({})").format(data_split[1]))
    return format_list

# Bloc d'extraction des liens des sites dans la base de données
def extract_links (type) :
    file = open("sites_list.txt", "r")
    all_data = file.readlines()
    scale = len(all_data)
    links_list = []
    for i in range(scale) :
        data = all_data[i]
        data_format = data.split(";")
        if type == "GS" :
            if data_format[0] == "GS" :
                links_list.append(data_format[2])

        if type == "PD" :
            if data_format[0] == "PD" :
                links_list.append(data_format[2])
    return links_list

# Bloc d'extraction des noms de fichiers LOG dans la base de donnée
def extract_path (mode) :
    path = str("sites_list.txt")
    file = open(path, "r")
    data = file.readlines()

    scale = len(data)
    list_path = []
    for i in range (scale) :
        if mode == "GS" and data[i].split(";")[0] == "GS" :
            if data[i].split(";")[3][-1] == "\n" :
                list_path.append(data[i].split(";")[3][:-1])
            else :
                list_path.append(data[i].split(";")[3])
        if mode == "PD" and data[i].split(";")[0] == "PD" :
            if data[i].split(";")[3][-1] == "\n" :
                list_path.append(data[i].split(";")[3][:-1])
            else :
                list_path.append(data[i].split(";")[3])
    return list_path

# Bloc de traitement pour extraire le lien feed.xml sur les pages padlet (création des liens padlet exploitables)
def link_padlet (link) :
    if link.split("/")[2] == "padlet.com" :
        if link.split("/")[-1] != "feed.xml" :
            if returnCode.status_page(link) == "True":
                requete = requests.get(link)
                page = requete.content
                soup = BeautifulSoup(page, features="html.parser")

                desc = soup.find_all("link", {'type': "application/rss+xml"})
                data = str(desc[0])
                rank_start = data.find("https://")
                rank_final = data.find("feed.xml")
                link_xml = str(data[rank_start:rank_final]) + str("feed.xml")
                # print(link_xml)
                return link_xml
            else:
                print("[!] Server unreachable or doesn't exist")
                return False
        elif returnCode.status_page(link) == "True":
            return True

    else:
        return False

# Bloc de vérification de la validité d'un lien de type GS
def link_GS (link) :
    if link.split("/")[2] == "sites.google.com" :
        if link.split("/")[3] == "view" :
            if returnCode.status_page(link) == "True":
                return True
            else:
                print("[!] Server unreachable or doesn't exist")
                return False
        else :
            return False
    else:
        return False

# Bloc de vérification de la longueur de la chaine de caractère entrée
def check_print (value) :
    if len(value) <= 25 :
        return True
    else :
        return False
