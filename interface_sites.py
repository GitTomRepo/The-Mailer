# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# INTERFACE SITE PAGE
# UTF-8
# Version : V2.0

# Importation des packets
from tkinter import *
import apply_changes
import extract_info
from tkinter import messagebox

# Bloc de suppression du site sélectionné
def get_list ():
    if select_GS[0] :
        site = GS_list.get(ANCHOR)
        if messagebox.askyesno("CONFIRM DELETING", ("Do you really want to delete this site : {}?").format(site)) :
            index_site = GS_sites.index(site)
            apply_changes.del_site(index_site)
            GS_list.delete(index_site)
            apply_changes.del_data_site(str(index_site))

    if select_PD[0] :
        site = PD_list.get(ANCHOR)
        if messagebox.askyesno("CONFIRM DELETING", ("Do you really want to delete this site : {} ?").format(site)):
            index_site = int(PD_sites.index(site)) + scale_GS[0]
            apply_changes.del_site(index_site)
            PD_list.delete(PD_sites.index(site))
            apply_changes.del_data_site(str(index_site))
    return None

# Blocs de sélection de chaque liste (double liste)
def selected_list_GS (e) :
    select_GS[0] = True
    select_PD[0] = False
    return None

def selected_list_PD (e) :
    select_GS[0] = False
    select_PD[0] = True
    return None

# Bloc d'ajout d'un site
def add_site () :
    # Fonction d'implémentation dans la base de donnée du nouveau site et extraction des informations relatives
    def add_linkApply():
        name = input_name.get()
        link = input_link.get()
        path = input_path.get() + ".txt"
        type = str()
        # Vérification de l'existence du site indiqué
        if messagebox.askyesno("CONFIRM", ("Do you want to add {} to the DataBase").format(name)) :
            if extract_info.check_print(name) == True :
                if extract_info.link_GS(link) == True :
                    type = str("GS")
                    scale_GS[0] = scale_GS[0] + 1
                    GS_sites.append(name)
                    GS_list.insert(scale_GS[0] - 1, name)
                    GS_links.append(link)
                    apply_changes.add_site(type, name, link, path)
                    file = open(path, "w")
                    file.close()
                elif extract_info.link_padlet(link) != False :
                    type = str("PD")
                    scale_PD[0] = scale_PD[0] + 1
                    PD_sites.append(name)
                    PD_list.insert(scale_PD[0]-1, name)
                    link = extract_info.link_padlet(link)
                    PD_links.append(link)
                    apply_changes.add_site(type, name, link, path)
                    file = open(path, "w")
                    file.close()
                else :
                    messagebox.showerror("ERROR #002", "Error during the verification of the link (please refer you at the ERROR_TYPE.txt file)")
            else :
                messagebox.showinfo("INCORRECT INPUT", "Please enter prints (under 25) for name")

    # Fonction de destruction de la fenêtre active
    def exit_add () :
        window_add.destroy()

    # Définition de la fenêtre au dessus de la fenêtre principale
    window_add = Toplevel()

    window_add.geometry("400x450")
    window_add.minsize(width=400, height=450)
    window_add.maxsize(width=400, height=450)
    window_add.title("ADD A NEW SITE")

    main_box = Frame(window_add, bg=background_color)
    main_box.pack(fill=BOTH, expand=YES)

    title_label = Label(main_box, text="ADD A NEW SITE", bg=background_color, fg='white', font=("Bahnschrift", 30))
    title_label.pack(padx=10, pady=30)

    label_name = Label(main_box, text="Name (No more than 25 prints)", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_name.pack(fill=BOTH, padx=5)
    input_name = Entry(main_box, fg='black', width=35)
    input_name.pack(padx=10, pady=20)

    label_link = Label(main_box, text="Link (please input a supported link (Google site or Padlet) )", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_link.pack(fill=BOTH, padx=5)
    input_link = Entry(main_box, fg='black', width=35)
    input_link.pack(padx=10, pady=20)

    label_path = Label(main_box, text="Name of the path (advice : put LOGS_ and your name as path)", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_path.pack(fill=BOTH, padx=5)
    input_path = Entry(main_box, fg='black', width=35)
    input_path.pack(padx=10, pady=20)

    # Définition des boutons de contrôle
    btn_exit = Button(main_box, text="EXIT", fg='black', command=exit_add)
    btn_exit.pack(padx=60, pady=10, side=LEFT)
    btn_enter = Button(main_box, text="CONFIRM", fg='black', command=add_linkApply)
    btn_enter.pack(padx=60, pady=10, side=RIGHT)

    window_add.mainloop()
    return None

# Bloc de changement d'informations relatives au site sélectionné
def change_site () :
    # Fonction de destruction de la fenêtre active
    def exit_add () :
        window_change.destroy()
        return None

    # Fonction d'application des modifications apportées
    def modify_site () :
        name = input_name.get()
        if extract_info.check_print(name) == True :
            change_link = input_link.get()
            change_name = input_name.get()
            if extract_info.link_GS(change_link) == True:
                index = GS_sites.index(site)
                type = str("GS")
                apply_changes.change_site(index, type, change_name, change_link)
                GS_list.delete(index)
                GS_list.insert(index, name)
                GS_sites[index] = name

            elif extract_info.link_padlet(change_link) != False :
                try :
                    index = int(PD_sites.index(site)) + scale_GS[0]
                    type = str("PD")
                    apply_changes.change_site(index, type, name, current_link)
                    PD_list.delete(PD_sites.index(site))
                    PD_list.insert(PD_sites.index(site), name)
                    PD_sites[PD_sites.index(site)] = name
                except :
                    messagebox.showerror("ERROR #001", "You can't change the type of link between us (please refer you at the ERROR_TYPE.txt file)")
            else :
                messagebox.showerror("ERROR #002", "Error during the verification of the link (please refer you at the ERROR_TYPE.txt file)")
        else :
            messagebox.showinfo("INCORRECT INPUT", "Please enter prints (under 25) for name")
            window_change.destroy()

    var_name = StringVar()
    var_link = StringVar()

    # Vérification de la sélection des listes (double liste)
    if select_GS[0] :
        site = GS_list.get(ANCHOR)
        index = GS_sites.index(site)
        current_link = str(GS_links[index])
        var_name.set(site)
        var_link.set(current_link)

    if select_PD[0] :
        site = PD_list.get(ANCHOR)
        index = PD_sites.index(site)
        current_link = str(PD_links[index])
        var_name.set(site)
        var_link.set(current_link)

    # Définition de la fenêtre par dessus la principale
    window_change = Toplevel()

    window_change.geometry("400x400")
    window_change.minsize(width=400, height=400)
    window_change.maxsize(width=400, height=400)
    window_change.title("CHANGE DATA OF THE SITE")

    main_box = Frame(window_change, bg=background_color)
    main_box.pack(fill=BOTH, expand=YES)

    title_label = Label(main_box, text="CHANGE DATA OF THE SITE", bg=background_color, fg='white', font=("Bahnschrift", 30))
    title_label.pack(padx=10, pady=30)

    label_name = Label(main_box, text="Name (No more than 25 prints)", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_name.pack(fill=BOTH, padx=5)
    input_name = Entry(main_box, fg='black', width=35, textvariable=var_name)
    input_name.pack(padx=10, pady=20)

    label_link = Label(main_box, text="Link (please input a supported link (Google site or Padlet) )", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_link.pack(fill=BOTH, padx=5)
    input_link = Entry(main_box, fg='black', width=35, textvariable=var_link)
    input_link.pack(padx=10, pady=20)

    # Définition des boutons de contrôle
    btn_exit = Button(main_box, text="EXIT", fg='black', command=exit_add)
    btn_exit.pack(padx=60, pady=10, side=LEFT)
    btn_enter = Button(main_box, text="CONFIRM", fg='black', command=modify_site)
    btn_enter.pack(padx=60, pady=10, side=RIGHT)

    window_change.mainloop()
    return None

# Définition des listes et variables usuels
background_color = str("#EAD45B")
path_site = str("sites_list.txt")

select_GS = [False]
select_PD = [False]

# Définition de la fenêtre principale
window_sites = Tk()
window_sites.geometry("500x600")
window_sites.minsize(width=500, height=600)
window_sites.maxsize(width=500, height=600)
window_sites.title("LOAD, DELETE OR DELET LINKS")

icon_GS = PhotoImage(file="GS_icon.png")
icon_PD = PhotoImage(file="PD_icon.png")

all_users = extract_info.extract_texte("users.txt")
scale_users = len(all_users)
user_names = []
n = int(0)
while n < scale_users :
    split_data = all_users[n].split(";")
    user_names.append(split_data[1])
    n += 1

site_list = extract_info.extract_texte(path_site)
scale_list = len(site_list)
GS_sites = []
PD_sites = []
GS_links = []
PD_links = []
for i in range (scale_list) :
    split_list = site_list[i].split(";")
    if split_list[0] == "GS" :
        GS_sites.append(split_list[1])
        GS_links.append(split_list[2])
    if split_list[0] == "PD" :
        PD_sites.append(split_list[1])
        PD_links.append(split_list[2])

scale_GS = [len(GS_sites)]
scale_PD = [len(PD_sites)]

title_control = Frame(window_sites, bg=background_color)
title_control.pack(fill=BOTH)

title_label = Label(title_control, text="CONTROL DATABASE", bg=background_color, fg='white', font=("Arial", 20))
title_label.pack(padx=10, pady=20)

info_control = Frame(window_sites, bg=background_color)
info_control.pack(fill=BOTH)

GS_frame = LabelFrame(info_control, bg=background_color, text="Google Site")
GS_frame.pack(fill=BOTH, padx=10, pady=5)

GS_logo = Canvas(GS_frame, width=100, height=100, bg=background_color)
GS_logo.create_image(50, 50, image=icon_GS)
GS_logo.grid(row=0, column=0, pady=15, padx=10)

GS_var = StringVar(value=GS_sites)
GS_list = Listbox(GS_frame, width=25, listvariable=GS_var)
GS_list.grid(row=0, column=1, padx=50, pady=15)
GS_list.bind('<ButtonRelease-1>', selected_list_GS)

PD_frame = LabelFrame(info_control, bg=background_color, text="Padlet", font=("Arial", 10))
PD_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)

PD_logo = Canvas(PD_frame, width=100, height=100, bg=background_color)
PD_logo.create_image(50, 50, image=icon_PD)
PD_logo.grid(row=0, column=0, pady=15, padx=10)

PD_var = StringVar(value=PD_sites)
PD_list = Listbox(PD_frame, width=25, listvariable=PD_var)
PD_list.grid(row=0, column=1, padx=50, pady=15)
PD_list.bind('<ButtonRelease-1>', selected_list_PD)

# Définition des boutons de contrôle
btn_control = Frame(window_sites, bg=background_color)
btn_control.pack(expand=YES, fill=BOTH)

btn_exit = Button(btn_control, fg='black', text="EXIT", command=window_sites.destroy)
btn_exit.grid(row=2, column=0, pady=10, padx=30)

btn_add_site = Button(btn_control, fg='black', text='ADD SITE', command=add_site)
btn_add_site.grid(row=2, column=3, pady=10, padx=30)

btn_del_site = Button(btn_control, fg='black', text='DELETE SITE', command=get_list)
btn_del_site.grid(row=2, column=4, pady=10, padx=30)

btn_change_site = Button(btn_control, fg='black', text='CHANGE SITE', command=change_site)
btn_change_site.grid(row=2, column=5, pady=10, padx=30)

window_sites.mainloop()
