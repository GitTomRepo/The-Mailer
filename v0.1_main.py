# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# FIRST_PAGE
# UTF-8
# Version : V1.0 | B0.5 DONE

import smtplib
from email.message import EmailMessage
import requests
import time, random
import datetime
from bs4 import BeautifulSoup
import os

#******************************* PRE-WRITED MESSAGES *******************************
scripted_msg = ["Nouveau contenu sur ", "Il y a du nouveau sur ", "Du contenu a été mis sur "]
scripted_from = ["Padlet ESC SVT : https://padlet.com/gsseprofsvt/Ens_scien", "Padlet d'Anglais : https://padlet.com/touzeletv/w2g6cw4facefkhsw", "Google Site Physique Chimie : https://sites.google.com/view/sciences-physiques-facile/terminale-sp%C3%A9"]
state = True

time_start = datetime.datetime.today()

print("************************************ MAIN *****************************************")
print("Version : V1.0 | B0.5 DONE")
print("Heure de Début :", time_start)
print("\n             -----------------------------------------------------       \n")

def email_post (content, scripted_msg, dest) :
    msg = EmailMessage()
    msg.set_content(random.choice(scripted_msg) + content)
    msg["Subject"] = "NOTIFICATION | NEW CONTENT"
    msg["From"] = "...mail adress for the bot..."
    msg["To"] = dest
    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls()
        smtp.login("...botmail adress...", "...Password of the botmail adress...")
        smtp.send_message(msg)
    print("EMAIL OK ...")

def GOOGLE_site_spe_terme () :
    requete = requests.get("https://sites.google.com/view/sciences-physiques-facile/terminale-sp%C3%A9")
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

#def Drive_sm ():
#    list_logs_dsm = DriveExploit.Drive_Maths_Spe_Term()
#    return list_logs_dsm

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

set_time = int(0)

try :
    while state :
        print(datetime.datetime.today())
        
        list_response_term = [Padlet_ESC_SVT(), Padlet_Anglais()]
        list_path_term = ["LOGS_SVT.txt", "LOGS_ANGLAIS.txt"]

        n = 0

        while n < len(list_path_term) :
            value_a = list_response_term[n]
            path_open = open(list_path_term[n], "r")
            read_value_b = path_open.readlines(1)
            value_b = read_value_b[-1]
            #print(value_a)
            #print(value_b)
            if str(value_b) != str(value_a) :
                path_open.close()
                change = open(list_path_term[n], "w")
                change = change.writelines(list_response_term[n])
                print("CHANGEMENT", list_path_term[n])
                email_post(scripted_from[n], scripted_msg, "USER1")
                email_post(scripted_from[n], scripted_msg, "USER2")
                email_post(scripted_from[n], scripted_msg, "USER3")
                email_post(scripted_from[n], scripted_msg, "USER4")
                email_post(scripted_from[n], scripted_msg, "USER5")
                email_post(scripted_from[n], scripted_msg, "USER6")
            else :
                path_open.close()
                print("AUCUN CHANGEMENT")
            n += 1

        data = GOOGLE_site_spe_terme()
        data_file = open("LOGS_GS.txt", "r")
        data_rls = data_file.readlines()
        scale = len(data_rls)
        data_file.close()

        #print(data)
        #print(data_rls)

        q = 0
        m = 0
        r = 0
        count_change = int(0)
        data_to_match = []

        if len(data) != scale:
            count_change += 1
            data_file = open("LOGS_GS.txt", "a")
            data_file.writelines(str(data[-1]) + "\n")
            data_file.close()
            print("FINISH")
            data_file = open("LOGS_GS.txt", "r")
            data_rls = data_file.readlines()
            scale = len(data_rls)
            data_file.close()

            while q < len(data):
                data_rls_terme = data[q]
                final_data_rls = data_rls_terme[:-2]
                #print(final_data_rls)
                data_to_match.append(final_data_rls + "'")
                q += 1
            print("OK")

        else :
            while q < len(data):
                data_rls_terme = data_rls[q]
                #print(data_rls_terme)
                final_data_rls = data_rls_terme[:-2]
                # print(final_data_rls)
                data_to_match.append(final_data_rls + "'")
                q += 1

            while m < len(data_rls):
                # print(data[m])
                # print(data_to_match[m])&
                if data[m] != data_to_match[m]:
                    count_change += 1
                m += 1

        while r < len(data) :
            data_to_match[r] = str(data[r] + "\n")
            data_file = open("LOGS_GS.txt", "w")
            data_file.writelines(data_to_match)
            data_file.close()
            r += 1

        if count_change >= int(1) :
            print("CHANGEMENT LOGS_GS.txt")
            email_post(scripted_from[-1], scripted_msg, "USER1")
            email_post(scripted_from[-1], scripted_msg, "USER2")
            email_post(scripted_from[-1], scripted_msg, "USER3")
            email_post(scripted_from[-1], scripted_msg, "USER4")
            email_post(scripted_from[-1], scripted_msg, "USER5")
            email_post(scripted_from[-1], scripted_msg, "USER6")
        else :
            print("AUCUN CHANGEMENT")

        print("\n             -----------------------------------------------------       \n")

        time.sleep(60)

        if set_time == 60 :
            email_post("SYSTEM ONLINE", [" ", " ", " "], "ADMIN")
            set_time = int(0)

        set_time += int(1)

except :
    print("ERROR ...")
    email_post("SYSTE OFFLINE", [" ", " ", " "], "ADMIN")
    os.system("sudo /mnt/init_start.sh")

