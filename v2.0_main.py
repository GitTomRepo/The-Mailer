# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# MAIN PAGE
# UTF-8
# Version : V2.0

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

        valueA_time = valueA[1] + valueA[2]
        valueB_time = valueB[1] + valueB[2]

        #print(valueA[:5], valueB[:5])

        # Si il y a plus de 2 erreurs en 2 secondes, l'algorithme va stopper le lancement du programme principal
        if valueA_tag[:5] and valueB_tag[:5] == "ERROR" :
            valueA_hms = valueA_time.split(":")
            valueB_hms = valueB_time.split(":")

            if valueA_hms[0] == valueB_hms[0] and valueA_hms[1] == valueB_hms[1] :
                valueA_sec = valueA_hms[-1].split(".")
                valueB_sec = valueB_hms[-1].split(".")

                if int(int(valueB_sec[0]) - int(valueA_sec[0])) < 2 :
                    report_file = open(path_report, "a")
                    report_file.writelines("\nSTOPPED \t" + str(datetime.datetime.today()))
                    report_file.close()
                    exit()
# Si le fichier n'est pas trouvé
except FileNotFoundError :
    print("[!] FILE OF THE DAY NOT FOUND...")
    report_file = open(path_report, "w")
    report_file.writelines("-------------------- CREATION " + str(datetime.datetime.today()) + " --------------------")
    report_file.close()

except :
    print("[!] ERROR #003, error during anti-crash system running (please refer you at the ERROR_TYPE.txt file)")
    exit()

# ------------------------------------------ PRE-WRITED MESSAGES ------------------------------------------
# Définition des listes nécessaire au fonctionnement de la partie traitement
scripted_msg = ["Nouveau contenu sur ", "Il y a du nouveau sur ", "Du contenu a été mis sur ", "Nouvelle mise à jour sur "]
scripted_from = []
# Extraction de toutes les composantes nécessaires pour les sites web à scanner
try :
    names_sites = extract_info.extract_sites()
    padlet_names = []
    GS_names = []
    GS_list = extract_info.extract_links("GS")
    for i in range (len(names_sites)) :
        split_name = names_sites[i].split(" ")
        if split_name[0] == "Padlet":
            padlet_names.append(names_sites[i])
        else :
            GS_names.append(names_sites[i])
    list_padlet = extract_info.extract_links("PD")
    for i in range (len(padlet_names)) :
        scripted_from.append(("{} : {}").format(padlet_names[i], ("/".join(list_padlet[i].split("/")[:5]))))

    list_path_GS = extract_info.extract_path("GS")
    list_path_PD = extract_info.extract_path("PD")

    # Extraction des utilisateurs et de leurs informations dans la base de donnée
    path_dataBase = str("users.txt")
    open_dataBase = open(path_dataBase, "r")
    all_data = open_dataBase.readlines()
    scale_dataBase = len(all_data)

    users_name = extract_info.extract_fromDataBase("name")
    users_email = extract_info.extract_fromDataBase("email")
    users_data = extract_info.extract_fromDataBase("data")

except SystemError as err:
    print("ERROR #004, error during the extraction of user and sites info (please refer you at the ERROR_TYPE.txt file)")
    print(err)
    exit()

print("/".join(list_padlet[0].split("/")[:5]))

# Début de l'execution de la partie traitement logique
print("************************************ MAIN *****************************************")
print("Version : V2.0")
print("Start time :", time_start)
print("Start date :", date)
print("\n             -----------------------------------------------------       \n")
state = True

# Blocs de récupération d'informations

# Fonction d'envoie de mail
def email_post (content, scripted_msg, dest) :
    try :
        msg = EmailMessage()
        msg.set_content(random.choice(scripted_msg) + content)
        msg["Subject"] = "NOTIFICATION | NEW CONTENT"
        msg["From"] = "bot.mailnoreturn@gmail.com"
        msg["To"] = dest
        with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
            smtp.starttls()
            smtp.login("bot.mailnoreturn@gmail.com", "*******")
            smtp.send_message(msg)
        print("[.] EMAIL OK ...")

        report_file = open(path_report, "a")
        report_file.writelines("EMAIL TO " + dest + "DELIVERED \t" + str(datetime.datetime.today()) + "\n")
        report_file.close()
    except :
        print("ERROR #005, error during email transmission (please refer you at the ERROR_TYPE.txt file)")

# Fonction de reformatage de la chaine de la liste brute des données pour le traitement (éviter les bugs du au retour à la ligne)
def format_chaine_GS (data) :
    try :
        q = int(0)
        data_to_match = []
        while q < len(data):
            data_rls_terme = data[q]
            final_data_rls = data_rls_terme[:-2]
            # print(final_data_rls)
            data_to_match.append(final_data_rls + "'")
            q += 1
        return data_to_match
    except :
        print("ERROR #006 , format of the Google site info fail (please refer you at the ERROR_TYPE.txt file)")

# Fonction d'extraction de données pour les Google Sites
def Google_Site (link) :
    try :
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
    except :
        print("ERROR #007, error of Google Site extraction (please refer you at the ERROR_TYPE.txt file)")

# Fonction d'extraction de la donnée temporelle de dernier ajout (disponible dans un fichier développeur)
def Padlet (link) :
    try :
        requete = requests.get(link)
        page = str(requete.content)
        page = str(page)

        page = page.split("   ")
        # print(page)
        # print(page[13])

        time_code = str(page[13].encode('utf-8'))

        return time_code
    except :
        print("ERROR #008, error of Padlet site extraction (please refer you at the ERROR_TYPE.txt file)")

# Début de la boucle infinie et traitement des données brut obtenues
try :
    while state :
        #print(datetime.datetime.today())
        set_time = int(0)

        n = int(0)
        # Bloc de traitement Padlet
        while n < len(list_path_PD) :
            if returnCode.status_page(list_padlet[n]) == "True" :
                value_a = Padlet(list_padlet[n])
                # Lecture des valeures de temps stockées
                path_open = open(list_path_PD[n], "r")
                read_value_b = path_open.readlines(1)
                value_b = read_value_b[-1]
                #print(value_a)
                #print(value_b)
                # Comparaison da la valeur stockée et de celle en ligne
                if str(value_b) != str(value_a) :
                    report_file = open(path_report, "a")
                    report_file.writelines("\n" + padlet_names[n] + "\t" + str(datetime.datetime.today()))
                    report_file.close()

                    print("[.] CHANGEMENT Padlet :" + padlet_names[n])
                    tag_user = int(0)

                    # Bloc d'envoie de mail
                    while tag_user < scale_dataBase :
                        selected_data = users_data[tag_user]
                        selected_email = users_email[tag_user]
                        #print(selected_data[n])
                        if selected_data[n] == "1" :
                            #email_post(scripted_from[n], scripted_msg, selected_email)
                            message = str(padlet_names[n] + ("/".join(list_padlet[0].split("/")[:5])))
                            print(message, selected_email)
                        tag_user += 1

                    path_open.close()
                    change = open(list_path_PD[n], "w")
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
        GS_list = extract_info.extract_links("GS")
        scale_link_GS = len(GS_list)

        while q < scale_link_GS :
            if returnCode.status_page(GS_list[q]) == "True" :
                # Récupération des valeurs liées au Google site
                data = Google_Site(GS_list[q])
                data_file = open(list_path_GS[q], "r")
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
                    data_file = open(list_path_GS[q], "a")
                    data_file.writelines(str(data[-1]) + "\n")
                    data_file.close()
                    data_file = open(list_path_GS[q], "r")
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
                    print("[.] CHANGEMENT Google site :" + GS_names[q])

                    report_file = open(path_report, "a")
                    report_file.writelines("\n" + GS_names[q] + "\t" + str(datetime.datetime.today()))
                    report_file.close()

                    tag_user = int(0)
                    while tag_user < scale_dataBase:
                        selected_data = users_data[tag_user]
                        selected_email = users_email[tag_user]
                        #print(selected_data[-1])
                        if selected_data[-1] == "1":
                            #email_post(GS_names[q] + list_GS[q], scripted_msg, selected_email)
                            message = str(GS_names[q] + GS_list[q])
                            print(message, selected_email)
                        tag_user += 1
                #else :
                    #print("AUCUN CHANGEMENT")

                # Modification du fichier LOGS pour mettre à jour les données sauvegardées
                data_logs = []
                while r < len(data) :
                    data_logs.append(str(data[r] + "\n"))
                    r += 1
                data_file = open(list_path_GS[q], "w")
                data_file.writelines(data_logs)
                data_file.close()
            else:
                report_file = open(path_report, "a")
                report_file.writelines("\nSERVER UNREACHABLE | GOOGLE SITE\t" + str(datetime.datetime.today()))
                report_file.close()
                print("[!] SERVER UNREACHABLE | GOOGLE SITE")
            q += 1

        print("\n             -----------------------------------------------------       \n")

        time.sleep(60)

        # Mise à jour du fichier REPORT tous les jours à 00:00
        if date != str(datetime.date.today()) :
            print("[.] DATE CHANGED")
            date = str(datetime.date.today())
            path_report = str("REPORT/report_" + str(date) + ".txt")
            report_file = open(path_report, "w")
            report_file.close()
            #os.system(sudo ./mnt/init_start.sh)

# Gestion des potentielles erreurs systèmes
except SystemError as err :
    print("[!] ERROR #009, error during the interpretation of informations (please refer you at the ERROR_TYPE.txt file) \n" + err)
    report_file = open(path_report, "a")
    report_file.writelines("\nERROR \t" + str(datetime.datetime.today()))
    report_file.close()

    # Bloc intégré pour gérer les erreurs de connection
    try :
        print("[!] SYSTEME OFFLINE")
        #email_post("SYSTEM OFFLINE", [err], "*** ADMIN EMAIL ***")
    except :
        # Si la connexion au serveur de messagerie ne marche pas ou si la connexion de l'hôte n'est pas activée, un report sera fait et le programme arrété
        report_file = open(path_report, "a")
        report_file.writelines("\nERROR EMAIL NOT POSTED \t" + str(datetime.datetime.today()))
        report_file.close()
        print("[!] ERROR #010, the transmission of error mail fail(please refer you at the ERROR_TYPE.txt file)")
        # os.system("sudo ./mnt/init_start.sh")

except KeyboardInterrupt :
    print("[!] Programme interrupted ...")
    report_file = open(path_report, "a")
    report_file.writelines("\nINTERUPTION \t" + str(datetime.datetime.today()))
    report_file.close()
    exit()
