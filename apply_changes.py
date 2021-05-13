# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# MODULE PAGE
# UTF-8
# Version : V2.0

# Packet d'application des modifications demandées par l'utilisateur

# Importation des packets
import extract_info

# Bloc d'écriture des changements à apporter à la base de donnée utilisateurs
def write_changes (tag, name, data) :
    path = str("users.txt")
    document_r = open(path, 'r')
    all_users_data = document_r.readlines()
    document_r.close()

    email_all = extract_info.extract_fromDataBase("email")
    mail_adress = email_all[tag]

    document_w = open(path, "w")
    tag_file = int(tag + 1)
    all_users_data[tag] = str("{};{};{};{}").format(str(tag_file), name, data, mail_adress)
    #print(str("{};{};{};{}\n").format(str(tag_file), name, data, mail_adress))
    document_w.writelines(all_users_data)

    document_w.close()

def del_data_site (site_tag) :
    path = str("users.txt")
    document_r = open(path, 'r')
    all_users_data = document_r.readlines()
    document_r.close()

    scale_db = len(all_users_data)
    for i in range (scale_db) :
        data_split = all_users_data[i].split(";")
        data_user = []
        n = int(0)
        while n < len(data_split[2]) :
            if str(n) != site_tag :
                data_user.append(data_split[2][n])
            n += 1
        data_split[2] = "".join(data_user)
        all_users_data[i] = ";".join(data_split)

    document_w = open(path, "w")
    document_w.writelines(all_users_data)
    document_w.close()

def add_data_site () :
    path = str("users.txt")
    document_r = open(path, 'r')
    all_users_data = document_r.readlines()
    document_r.close()

    scale_db = len(all_users_data)
    final_users_data = []
    for i in range(scale_db):
        data_split = all_users_data[i].split(";")
        data_split[2] = data_split[2] + "0"
        final_users_data.append(";".join(data_split))

    document_w = open(path, "w")
    document_w.writelines(all_users_data)
    document_w.close()

# Bloc d'ajout dans la base de donnée d'un utilisateur
def add_user (name, data, email) :
    path = str("users.txt")
    document_r = open(path, 'r')
    all_users_data = document_r.readlines()
    scale = len(all_users_data)
    document_r.close()
    #print(scale)

    document_add = open(path, "a")
    line_nex_user = str("\n{};{};{};{}").format(str(scale+1), name, data, email)
    document_add.writelines(line_nex_user)
    document_add.close()

# Bloc de suppression dans la base de donnée d'un utilisateur
def del_user (name) :
    path = str("users.txt")
    document_r = open(path, 'r')
    all_users_data = document_r.readlines()
    scale = len(all_users_data)
    document_r.close()
    #print(scale)

    d = int(0)
    users_name = []
    while d < scale :
        data_user_split = all_users_data[d].split(";")
        users_name.append(data_user_split[1])
        d += 1
    #print(users_name)

    try :
        tag = users_name.index(name)
        #print(tag)
        all_users_data.remove(all_users_data[tag])

        document_w = open(path, 'w')

        names = []
        data = []
        email = []
        for i in range(0, len(all_users_data)):
            user_data = all_users_data[i]
            user_data_split = user_data.split(";")
            names.append(user_data_split[1])
            data.append(user_data_split[2])
            email.append(user_data_split[3])
        email[-1] = email[-1][:-1]

        d = 0
        modified_data = []
        while d < len(all_users_data):
            modified_data.append(str("{};{};{};{}").format(str(d + 1), names[d], data[d], email[d]))
            d += 1
        #print(modified_data)
        document_w.writelines(modified_data)
        document_w.close()
        return None

    except ValueError :
        print(str("[!] The user {} is NOT in list").format(name))
        return None

# Bloc de changement des informations dans la base de donnée des sites
def change_site (index, type, name, link) :
    path = str("sites_list.txt")
    file = open(path, "r")
    data = file.readlines()
    scale = len(data)
    file.close()
    file = open(path, "w")
    data[index] = ("{};{};{}\n").format(type, name, link)
    file.writelines(data)
    file.close()

    return None

# Bloc d'ajout d'un site web dans la base de donnée ainsi que ses informations
def add_site(type, name, link, path_log) :
    path = str("sites_list.txt")
    file = open(path, "r")
    data = file.readlines()
    file.close()

    if data == None :
        data = []

    file = open(path, "w")

    if str(type) == "PD" :
        data.append(("{};{};{};{}").format(type, name, link, path_log))
        file.writelines(data)
    elif str(type) == "GS" :
        r = int(0)
        if data != [] :
            while data[r][:1] == "GS" :
                r += 1
        else :
            r = 0
        data.insert(r, ("{};{};{};{}\n").format(type, name, link, path_log))
        file.writelines(data)
    file.close()

# Bloc de suppression dans la base de donnée d'un site ainsi que de ses informations
def del_site (index) :
    path = str("sites_list.txt")
    file = open(path, "r")
    data = file.readlines()
    scale = len(data)

    final_data = []
    for i in range(scale) :
        if str(i) != str(index) :
            final_data.append(data[i])

    file.close()
    file = open(path, "w")
    file.writelines(final_data)
    file.close()
