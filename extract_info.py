# Packet permettant d'extraire les données des utilisateurs stockées dans le fichier client
# Bloc d'extraction des données pour un utilisateur
def info_user (name) :
    #print("Starting extract ...")
    path = str("users.txt")
    get_data = open(path, "r")
    all_data = get_data.readlines()

    #print(all_data)
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
