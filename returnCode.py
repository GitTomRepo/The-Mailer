# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# MODULE PAGE
# UTF-8
# Version : V2.0

# Packet permettant de récupérer le code renvoyer par la page web à scanner
# Importations des packets
import requests
import datetime

# Bloc permettant la vérification de l'existance d'un lien donné
def status_page (url) :
    path_report = str("REPORT/report_2021-03-26.txt")
    try :
        info = requests.get(url)
        code = int(info.status_code)
        #print(code)
        if code == 200 :
            # La page existe
            #print("Page Reachable")
            return str("True")
        elif code == 404 :
            # La page est innexistante
            #print("Page Unreachable")
            report_file = open(path_report, "a")
            report_file.writelines("ERROR 404 \t" + str(datetime.datetime.today()) + "\n")
            report_file.close()
            return str("False")

    # En cas de coupure internet, un processus de coupure d'urgence se met en place
    except :
        report_file = open(path_report, "a")
        report_file.writelines("ERROR CONNEXION NOT ENABLE \t" + str(datetime.datetime.today()))
        report_file.close()
        exit()
