# usr/bin/python3
# UTF-8
# Author : Tom MANSIAT
# -------------------------------------------------------- #

# -------------------------------------------------------- #
# INTERFACE USER PAGE
# UTF-8
# Version : V2.0

# Importation des packets
from tkinter import *
import apply_changes
import extract_info
from tkinter import messagebox

# Initialisation de la couleur de fond
background_color = str("#EAD45B")

# Bloc d'application les changements à propos d'un utilisateur
def get_stat () :
    user = select_user.get(ANCHOR)
    user_tag = user_list.index(user)
    if messagebox.askyesno("CONFIRM", ("Do you want to change information about this user : {}").format(user)) :
        selected_sites = str(select_site.curselection())[1:-1].split(",")
        var_user = []
        if selected_sites[-1] == '':
            selected_sites = selected_sites[0]
            print(selected_sites)
            for i in range (len(site_list)) :
                if i == int(selected_sites) :
                    var_user.append("1")
                else :
                    var_user.append("0")
            var_user = "".join(var_user)
            apply_changes.write_changes(user_tag, user, var_user)
            return None
        scale = len(selected_sites)
        for i in range (scale) :
            if i == 0 :
                if str(i) == selected_sites[i] :
                    var_user.append("1")
                else :
                    var_user.append("0")
            else :
                if str(i) == selected_sites[i][-1] :
                    var_user.append("1")
                else :
                    var_user.append("0")
        var_user = "".join(var_user)
        apply_changes.write_changes(user_tag, user, var_user)
        return None

# Bloc activant toutes les CheckBox
def true_all () :
    var2 = [GS_state, PD_A_state, PD_ESC_SVT_state]
    btn_var = [btn_GS, btn_PD_A, btn_PD_ESC_SVT]
    m = int(0)
    if ALL_var.get() == 5 :
        while m < len(var2) :
            btn_var[m].select()
            m += 1
    elif ALL_var.get() == 6 :
        while m < len(var2) :
            btn_var[m].deselect()
            m += 1

# Bloc qui permet d'afficher une nouvelle fenêtre montrant les informations de l'utilisateur sélectionné
def data_user () :
    user = str(select_user.get(ANCHOR))
    user_tag = user_list.index(user)
    email = email_list[user_tag]
    data_user_all = extract_info.info_user(user)

    data = data_user_all[-2]

    data_true = []
    x = int(0)
    while x < len(site_list) :
        if data[x] == "1" :
            data_true.append(site_list[x])
        x += 1
    data_display = str("\n".join(data_true))
    #print(data_display)

    # Définition de la fenêtre
    window_user_info = Tk()
    window_user_info.geometry("500x400")
    window_user_info.title("USER INFO")
    user_label = Label(window_user_info, bg=background_color, fg="white", text=user, font=("Arial", 20))
    user_label.pack(expand=YES, fill=BOTH)
    email_label = Label(window_user_info, bg=background_color, fg="white", text=email, font=("Arial", 20))
    email_label.pack(expand=YES, fill=BOTH)
    data_user_label = Label(window_user_info, bg=background_color, fg="white", text=data_display, font=("Arial", 20))
    data_user_label.pack(expand=YES, fill=BOTH)

    window_user_info.mainloop()

# Bloc d'ajout d'un utilisateur à la base de donnée
def add_user () :
    # Fonction d'ajout de l'utilisateur et du traitement des informations données
    def add_userApply():
        name = input_name.get()
        selected_sites = str(select_site.curselection()).split(",")
        scale = len(selected_sites)
        for i in range(scale):
            if selected_sites[i][0] == "(":
                selected_sites[i] = selected_sites[i][-1]
            elif selected_sites[i][-1] == ")":
                selected_sites[i] = selected_sites[i][1]
        var_user = []
        n = int(0)
        while n < scale:
            var_user.append(selected_sites[n])
            n += 1
        var_user = "".join(var_user)
        email = input_mail.get()
        if extract_info.check_print(name) == True :
            if messagebox.askyesno("CONFIRM", "Are you sure to add this new user ?") :
                apply_changes.add_user(name, var_user, email)
                user_list.append(name)
                email_list.append(email)
                select_user.insert(number_user + 1, name)
                messagebox.showinfo("UPDATE SUCCESS", "Data Base updated SUCCESSFULLY!")
        else :
            messagebox.showinfo("INCORRECT INPUT", "Please enter prints (under 25) for name")
    # Fonction de destruction de la fenêtre active
    def exit_add () :
        window_add.destroy()
        window_change.mainloop()
    # Définition de la fenêtre, par dessus la principale
    window_add = Toplevel()

    window_add.geometry("400x500")
    window_add.minsize(width=400, height=500)
    window_add.maxsize(width=400, height=500)
    window_add.title("ADD A NEW USER")

    # Box principale, contenant tous les widjets à l'écran
    main_box = Frame(window_add, bg=background_color)
    main_box.pack(fill=BOTH, expand=YES)

    title_label = Label(main_box, text="ADD A NEW USER", bg=background_color, fg='white', font=("Bahnschrift", 30))
    title_label.pack(padx=10, pady=30)

    label_name = Label(main_box, text="Name (Surname NAME)", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_name.pack(fill=BOTH, padx=5)
    input_name = Entry(main_box, fg='black', width=35)
    input_name.pack(padx=10, pady=20)

    label_mail = Label(main_box, text="Email address", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_mail.pack(fill=BOTH, padx=5)
    input_mail = Entry(main_box, fg='black', width=35)
    input_mail.pack(padx=10, pady=20)

    label_data = Label(main_box, text="Choose options", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_data.pack(padx=10, pady=10)

    nb_site = len(site_list)
    select_site = Listbox(main_box, selectmode="multiple", width=40, height=5)
    select_site.pack(pady=10, padx=30)

    for i in range(nb_site):
        select_site.insert(i, site_list[i])
    select_site.pack()

    btn_exit = Button(main_box, text="EXIT", fg='black', command=exit_add)
    btn_exit.pack(padx=60, pady=10, side=LEFT)
    btn_enter = Button(main_box, text="CONFIRM", fg='black', command=add_userApply)
    btn_enter.pack(padx=60, pady=10, side=RIGHT)

    window_add.mainloop()

# Bloc de suppression d'un utilisateur
def delete_user () :

    # Fonction supprimant l'utilisateur et traitant les informations données
    def del_user () :
        try :
            name = input_name.get()
            email = input_mail.get()
            if user_list.index(name) == email_list.index(email) :
                if messagebox.askyesno("CONFIRM", "Are you sure to delete this user ?"):
                    apply_changes.del_user(name)
                    select_user.delete(user_list.index(name))
            else :
                messagebox.showerror("ERROR", "EMAIL IS NOT CORRECT")

        except :
            messagebox.showerror("ERROR", "THE USER OR EMAIL IS NOT IN LIST")
            window_del.destroy()
            window_change.mainloop()

    # Fonction de destruction de la fenêtre active
    def exit_del () :
        window_del.destroy()

    # Définition d'une nouvelle fenêtre par dessus la principale
    window_del = Toplevel()
    window_del.geometry("300x400")
    window_del.minsize(width=300, height=400)
    window_del.maxsize(width=300, height=400)
    window_del.title("DELETE USER")

    main_box = Frame(window_del, bg=background_color)
    main_box.pack(fill=BOTH, expand=YES)

    title_label = Label(main_box, text="DELETE USER", bg=background_color, fg='white', font=("Bahnschrift", 30))
    title_label.pack(padx=10, pady=30)

    label_name = Label(main_box, text="Name (Surname NAME)", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_name.pack(fill=BOTH, padx=5)
    input_name = Entry(main_box, fg='black', width=35)
    input_name.pack(padx=10, pady=20)

    label_mail = Label(main_box, text="Email address", bg=background_color, fg='white', font=("Bahnschrift", 10))
    label_mail.pack(fill=BOTH, padx=5)
    input_mail = Entry(main_box, fg='black', width=35)
    input_mail.pack(padx=10, pady=20)

    btn_exit = Button(main_box, text="EXIT", fg='black', command=exit_del)
    btn_exit.pack(padx=50, pady=10, side=LEFT)
    btn_enter = Button(main_box, text="CONFIRM", fg='black', command=del_user)
    btn_enter.pack(padx=50, pady=10, side=RIGHT)

    window_del.mainloop()


# Définition et extraction des informations à propos des utilisateurs
user_list = extract_info.extract_fromDataBase("name")
email_list = extract_info.extract_fromDataBase("email")
nb_user = int(len(user_list) + 1)

site_list = extract_info.extract_sites()

var_all_users = []
a = int(0)
while a < len(user_list) :
    var_all_users.append(extract_info.info_user(user_list[a]))
    a += 1

# Définition de la fenêtre principale
window_change = Tk()

window_change.geometry("600x400")
window_change.minsize(width=600, height=400)
window_change.maxsize(width=600, height=400)
# Titre de la fenêtre
window_change.title("APPLY AND MODIFY DATA")
window_change.config(bg=background_color)

title_label = Label(window_change, text="CONTROL DATABASE", bg=background_color, fg='white', font=("Arial", 20), anchor=E)
title_label.pack(padx=10, pady=20)

frame_btn = Frame(window_change, bg=background_color, borderwidth=2, relief=GROOVE)
frame_btn.pack(padx=10, pady=10)

# Insertion des utilisateur dans la liste définie
select_user = Listbox(frame_btn)
number_user = int(1)
while number_user < nb_user :
    select_user.insert(number_user, user_list[number_user-1])
    number_user += 1

select_user.pack(padx=30, pady=10, side=LEFT)

# Définition de la liste pour la sélection des options
nb_site = len(site_list)
select_site = Listbox(frame_btn, selectmode="multiple", width=40)
select_site.pack(pady=10, padx=30)

for i in range (nb_site) :
    select_site.insert(i, site_list[i])

# Définition de tous les boutons de contrôles en bas de la page
btn_control = Frame(window_change, bg=background_color)
btn_control.pack(pady=20)

btn_exit = Button(btn_control, fg='black', text="EXIT", command=window_change.destroy)
btn_exit.grid(row=2, column=0, pady=10, padx=20)

btn_show_User_data = Button(btn_control, fg='black', text='SHOW USER DATA', command=data_user)
btn_show_User_data.grid(row=2, column=1, pady=10, padx=20)

btn_show_stat = Button(btn_control, fg='black', text='APPLY CHANGES', command=get_stat)
btn_show_stat.grid(row=2, column=2, pady=10, padx=20)

btn_add_user = Button(btn_control, fg='black', text='ADD USER', command=add_user)
btn_add_user.grid(row=2, column=3, pady=10, padx=20)

btn_del_user = Button(btn_control, fg='black', text='DELETE USER', command=delete_user)
btn_del_user.grid(row=2, column=4, pady=10, padx=20)

window_change.mainloop()
