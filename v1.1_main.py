# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# FIRST_PAGE
# UTF-8
# Version : V1.1 | B0.9 DONE

import smtplib
from email.message import EmailMessage
import requests
import time
import random
import datetime
from bs4 import BeautifulSoup
import os
import extract_info
import returnCode

#******************************* ANTI-CRASH SYSTEM *******************************
date = str(datetime.date.today())
time_start = datetime.datetime.today()
path_report = str("REPORT/report_" + date + ".txt")

# Bloc de vérification des erreurs précédentes pour engager un arret d'urgence (sans envoie de mail)
try :
    list_report = extract_info.extract_texte(path_report)
    if len(list_report) >= 2 :
        last_values = [list_report[-2], list_report[-1]]
        valueA = last_values[0].split(" ")
        valueB = last_values[1].split(" ")

        #print(valueA, valueB)

        valueA_tag = valueA[0]
        valueB_tag = valueB[0]

        valueA_time = valueA[1]
        valueB_time = valueB[1]

        #print(valueA[:5], valueB[:5])

        if valueA_tag[:5] and valueB_tag[:5] == "ERROR" :
            valueA_hms = valueA_time.split(":")
            valueB_hms = valueB_time.split(":")

            if valueA_hms[0] == valueB_hms[0] and valueA_hms[1] != valueB_hms[1] :
                valueA_sec = valueA_hms[-1].split(".")
                valueB_sec = valueB_hms[-1].split(".")

                if int(int(valueB_sec[0]) - int(valueA_sec[0])) < 2 :
                    report_file = open(path_report, "a")
                    report_file.writelines("STOPPED \t" + str(datetime.datetime.today()) + "\n")
                    report_file.close()
                    exit()
except FileNotFoundError :
    print("[!] FILE OF THE DAY NOT FOUND...")
    report_file = open(path_report, "w")
    report_file.writelines("-------------------- CREATION " + str(datetime.datetime.today()) + " --------------------\n")
    report_file.close()

# ------------------------------------------ PRE-WRITED MESSAGES ------------------------------------------
# Définition des listes nécessaire au fonctionnement de la partie traitement
scripted_msg = ["Nouveau contenu sur ", "Il y a du nouveau sur ", "Du contenu a été mis sur ", "Nouvelle mise à jour sur "]
scripted_from = ["LIST OF SITES FOR EMAIL"]

path_padlet = str("LINKS_PADLET.txt")
path_GS = str("LINKS_GS.txt")

list_padlet = extract_info.extract_texte(path_padlet)
list_GS = extract_info.extract_texte(path_GS)

path_dataBase = str("users.txt")
open_dataBase = open(path_dataBase, "r")
all_data = open_dataBase.readlines()
scale_dataBase = len(all_data)

users_name = extract_info.extract_fromDataBase("name")
users_email = extract_info.extract_fromDataBase("email")
users_data = extract_info.extract_fromDataBase("data")

print(users_name)
print(users_email)
print(users_data)

# Début de l'execution de la partie traitement logique
print("************************************ MAIN *****************************************")
print("Version : V1.1 | B0.8 DONE")
print("Start time :", time_start)
print("Start date :", date)
print("\n             -----------------------------------------------------       \n")
state = True

# Blocs de récupération d'informations

# Fonction d'envoie de mail
def email_post (content, scripted_msg, dest) :
    msg = EmailMessage()
    msg.set_content(random.choice(scripted_msg) + content)
    msg["Subject"] = "NOTIFICATION | NEW CONTENT"
    msg["From"] = "bot.mailnoreturn@gmail.com"
    msg["To"] = dest
    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls()
        smtp.login("bot.mailnoreturn@gmail.com", "Qzt=25S@#/")
        smtp.send_message(msg)
    print("[.] EMAIL OK ...")

    report_file = open(path_report, "a")
    report_file.writelines("EMAIL TO " + dest + "DELIVERED \t" + str(datetime.datetime.today()))
    report_file.close()

# Fonction de reformatage de la chaine de la liste brute des données pour le traitement (éviter les bugs du au retour à la ligne)
def format_chaine_GS (data) :
    q = int(0)
    data_to_match = []
    while q < len(data):
        data_rls_terme = data[q]
        final_data_rls = data_rls_terme[:-2]
        # print(final_data_rls)
        data_to_match.append(final_data_rls + "'")
        q += 1
    return data_to_match

# Fonction d'extraction de données pour les Google Sites
def Google_Site (link) :
    requete = requests.get(link)
    page = requete.content
    soup = BeautifulSoup(page, features="html.parser")

    desc = soup.find_all("p", {'class': "CDt4Ke zfr3Q"})
    n = 0
    desc_final = []
    while n < len(desc):
        desc_final.append(str(desc[n].encode('utf-8')))
        n += 1

    # print(desc_final)
    return desc_final

# Fonction d'extraction de la donnée temporelle de dernier ajout (disponible dans un fichier développeur)
def Padlet (link) :
    requete = requests.get(link)
    page = str(requete.content)
    page = str(page)

    page = page.split("   ")
    # print(page)
    # print(page[13])

    time_code = str(page[13].encode('utf-8'))

    return time_code

# Début de la boucle infinie et traitement des données brut obtenues
try :
    while state :
        print(datetime.datetime.today())
        set_time = int(0)

        list_path_term = ["LIST OF PATH FOR DATA"]

        n = 0
        # Bloc de traitement Padlet
        while n < len(list_path_term) :

            if returnCode.status_page(list_padlet[n]) == "True" :
                value_a = Padlet(list_padlet[n])

                # Lecture des valeures de temps stockées
                path_open = open(list_path_term[n], "r")
                read_value_b = path_open.readlines(1)
                value_b = read_value_b[-1]
                #print(value_a)
                #print(value_b)

                # Comparaison da la valeur stockée et de celle en ligne
                if str(value_b) != str(value_a) :
                    report_file = open(path_report, "a")
                    report_file.writelines(list_path_term[n] + "\t" + str(datetime.datetime.today()) + "\n")
                    report_file.close()

                    print("[.] CHANGEMENT", list_path_term[n])
                    tag_user = int(0)

                    # Bloc d'envoie de mail
                    while tag_user < scale_dataBase :
                        selected_data = users_data[tag_user]
                        selected_email = users_email[tag_user]
                        print(selected_data[n])
                        if selected_data[n] == "1" :
                            email_post(scripted_from[n], scripted_msg, selected_email[:-1])
                            #print(scripted_from[n], selected_email[:-1])
                        tag_user += 1

                    path_open.close()
                    change = open(list_path_term[n], "w")
                    change = change.writelines(value_a)
                else :
                    path_open.close()
                    #print("AUCUN CHANGEMENT")
            else :
                report_file = open(path_report, "a")
                report_file.writelines("SERVER UNREACHABLE | PADLET\t" + str(datetime.datetime.today()) + "\n")
                report_file.close()
                print("[!] SERVER UNREACHABLE | PADLET")
            n += 1


        # Bloc de traitement de traitement du Google Site
        q = int(0)
        scale_link_GS = len(list_GS)

        while q < scale_link_GS :
            if returnCode.status_page(list_GS[q]) == "True" :
                # Récupération des valeurs liées au Google site
                data = Google_Site(list_GS[q])
                data_file = open("LOGS_GS.txt", "r")
                data_rls = data_file.readlines()
                scale = len(data_rls)
                data_file.close()

                # print(data)
                # print(data_rls)

                m = 0
                r = 0
                count_change = int(0)
                data_to_match = format_chaine_GS(data_rls)

                # Vérification d'un ajout
                if len(data) != scale:
                    count_change += 1
                    data_file = open("LOGS_GS.txt", "a")
                    data_file.writelines(str(data[-1]) + "\n")
                    data_file.close()
                    data_file = open("LOGS_GS.txt", "r")
                    data_rls = data_file.readlines()
                    scale = len(data_rls)
                    data_file.close()

                else :
                    # Vérification d'un changement à partir des données formatées dans le bloc précédent
                    while m < len(data_rls):
                        # print(data[m])
                        # print(data_to_match[m])
                        if data[m] != data_to_match[m]:
                            count_change += 1
                        m += 1

                # Bloc d'envoie des mails et de mise à jour du fichier REPORT
                if count_change >= int(1) :
                    print("[.] CHANGEMENT Google site")

                    report_file = open(path_report, "a")
                    report_file.writelines("GOOGLE SITE\t" + str(datetime.datetime.today()) + "\n")
                    report_file.close()

                    tag_user = int(0)
                    while tag_user < scale_dataBase:
                        selected_data = users_data[tag_user]
                        selected_email = users_email[tag_user]
                        print(selected_data[-1])
                        if selected_data[-1] == "1":
                            email_post("Google Site Physique Chimie", scripted_msg, selected_email[:-1])
                            #print("Google Site Physique Chimie", selected_email[:-1])
                        tag_user += 1
                #else :
                    #print("AUCUN CHANGEMENT")

                # Modification du fichier LOGS pour mettre à jour les données sauvegardées
                while r < len(data) :
                    data_to_match[r] = str(data[r] + "\n")
                    data_file = open("LOGS_GS.txt", "w")
                    data_file.writelines(data_to_match)
                    data_file.close()
                    r += 1
            else:
                report_file = open(path_report, "a")
                report_file.writelines("SERVER UNREACHABLE | GOOGLE SITE\t" + str(datetime.datetime.today()) + "\n")
                report_file.close()
                print("[!] SERVER UNREACHABLE | GOOGLE SITE")
            q += 1

        print("\n             -----------------------------------------------------       \n")

        time.sleep(60)

        # Mise à jour du fichier REPORT tous les jours à 00:00
        if date != datetime.date.today() :
            print("[.] DATE CHANGED")
            date = datetime.date.today()
            path_report = str("REPORT/report_" + str(date) + ".txt")
            report_file = open(path_report, "w")
            report_file.close()
            os.system("clear")

# Gestion des potentielles erreurs systèmes
except EnvironmentError as err:
    print("[!] ERROR ..." + err)
    report_file = open(path_report, "a")
    report_file.writelines("ERROR \t" + str(datetime.datetime.today()))
    report_file.close()

    # Bloc intégré pour gérer les erreurs de connection
    try :
        print("[!] SYSTEME OFFLINE")
        email_post("SYSTEM OFFLINE", [err], "tommscolaire@gmail.com")
    except :
        report_file = open(path_report, "a")
        report_file.writelines("ERROR EMAIL NOT POSTED \t" + str(datetime.datetime.today()))
        report_file.close()
        print("[!] EMAIL NOTIF ERROR")
        os.system("sudo *****SECRET PATH******")
