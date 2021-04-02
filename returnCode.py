# Packet permettant de récupérer le code renvoyer par la page web à scanner

import requests
import datetime

def status_page (url) :
    path_report = str("REPORT/report_2021-03-26.txt")
    try :
        info = requests.get(url)
        code = int(info.status_code)
        #print(code)
        if code == 200 :
            #print("Page Reachable")
            return str("True")
        elif code == 404 :
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
