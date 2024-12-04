# The main App for our project. This handles page shifts and direct calls for certain features like balance and load/unload
import tkinter as tk
import pandas as pd
from itertools import combinations
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from _new_balance_alg import process_manifest,load_manifest

#https://docs.python.org/3/library/dialog.html#




root = tk.Tk()

#dataset = ["root"]
dataset = [""]

def credentials_tab():

    global credential
    global button
    global username

    
        
    credential = tk.Label(root,text="Welcome back, provide credentials")
    credential.pack()

    username = tk.Entry(root)
    username.pack()
    
    # For login, reference https://www.w3resource.com/python-exercises/tkinter/python-tkinter-basic-exercise-16.phpx
    def login():
        if username.get() in dataset: 
            upload_manifest_tab()
        else: 
            messagebox.showerror("Login Failed","invalid credentials")

    

    button = tk.Button(root,text="login",command=login)
    button.pack()



def open_manifest(): 

    global manifest_file # Manifest file can be access anywhere in the program since is global
    global path
    path = askopenfilename(filetypes=[("Text Files", "*.txt")])
    with open(path, 'r') as m:
        
        manifest_file = m.read()
    # messagebox.showinfo("Manifest File", manifest_file)

    main_menu_tab()


def upload_manifest_tab():
    credential.destroy()
    button.destroy()
    username.destroy()

    global upload_manifest
    global button2



    upload_manifest = tk.Label(root, text="Upload manifest")
    upload_manifest.pack()

    button2 = tk.Button(root,text="UPLOAD",command=open_manifest,height=10,width=40)
    button2.pack(expand=True)



def main_menu_tab(): 
    upload_manifest.destroy()
    button2.destroy()

    global msg
    global Balance
    global Load_unload


    msg = tk.Label(root,text="Choose a task")
    msg.pack()

    Balance = tk.Button(root, text="Balance",command=Balance_tab,height=20,width=40,fg="blue",background="gray")
    Balance.pack(side="left",expand=True)
    
    
    Load_unload = tk.Button(root, text="Load / Unload",command=Load_unload_tab,height=20,width=40,fg = "red", background="gray")
    Load_unload.pack(side = "right",expand=True)

def GUI():
    global rr

    color = "white"

    rr = tk.Frame(root)
    rr.pack(anchor="n", expand=True)
    rows = 8
    while rows > 0:
        for k in range(12):
            v = tk.StringVar()

            if rows == 8:
                if file["Container"][k] == "NAN":
                    color = "gray"

                if file["Container"][k] != "NAN" and file["Container"][k] != "UNUSED":
                    color = "green"

                v.set(file["Position"][k] + "\n" + file["Weight"][k] + "\n" + file["Container"][k])
            else:
                if file["Container"][(8 - rows) * 12 + k] == "NAN":
                    color = "gray"

                if file["Container"][(8 - rows) * 12 + k] != "NAN" and file["Container"][
                    (8 - rows) * 12 + k] != "UNUSED":
                    color = "green"

                v.set(file["Position"][(8 - rows) * 12 + k] + "\n" + file["Weight"][(8 - rows) * 12 + k] + "\n" +
                      file["Container"][(8 - rows) * 12 + k])
            message = tk.Message(rr, relief="raised", width=100, textvariable=v, bg=color)

            color = "white"

            message.grid(row=rows, column=k, padx=10, pady=10)
        rows -= 1

def Balance_tab():

    global file
    global button3
    global timer_label
    msg.destroy()
    Balance.destroy()
    Load_unload.destroy()

    messagebox.showinfo("Info","Ready to balance")

    timer_label = tk.Label(root, text="estimated time remanining",padx=10,pady=5)
    timer_label.pack()

    file = load_manifest(path)

    GUI()

    button3 = tk.Button(root,text="continue",height=5,width=15)
    button3.pack(expand=True,side="top")




    #Load_unload_tab()

def Load_unload_tab():
    global file
    global button3
    global timer_label
    msg.destroy()
    Balance.destroy()
    Load_unload.destroy()

    messagebox.showinfo("Info", "Ready to load/unload")

    timer_label = tk.Label(root, text="estimated time remaining", padx=10, pady=5)
    timer_label.pack()

    file = load_manifest(path)
    GUI()

    user_action_label = tk.Label(root, text="Enter 'load' to load a container or 'unload' to unload a container:")
    user_action_label.pack()
    user_action_entry = tk.Entry(root)
    user_action_entry.pack()

    def handle_action():
        user_action = user_action_entry.get().lower()
        if user_action == "load":
            load_container()
        elif user_action == "unload":
            unload_container()
        else:
            messagebox.showerror("Invalid Action", "Please enter 'load' or 'unload'")

    submit_action_button = tk.Button(root, text="Submit", command=handle_action)
    submit_action_button.pack()

def load_container():
    global file
    location_label = tk.Label(root, text="Enter the desired load location (e.g., 01,02):")
    location_label.pack()
    location_entry = tk.Entry(root)
    location_entry.pack()

    def handle_load():
        location = location_entry.get().strip()
        if location in file["Position"].values and file.loc[file["Position"] == location, "Container"].values[0] == "UNUSED":
            container_name_label = tk.Label(root, text="Enter the container name:")
            container_name_label.pack()
            container_name_entry = tk.Entry(root)
            container_name_entry.pack()

            container_mass_label = tk.Label(root, text="Enter the container mass:")
            container_mass_label.pack()
            container_mass_entry = tk.Entry(root)
            container_mass_entry.pack()

            def finalize_load():
                container_name = container_name_entry.get().strip()
                container_mass = container_mass_entry.get().strip()
                file.loc[file["Position"] == location, "Container"] = container_name
                file.loc[file["Position"] == location, "Weight"] = container_mass
                GUI()

            finalize_button = tk.Button(root, text="Finalize Load", command=finalize_load)
            finalize_button.pack()
        else:
            messagebox.showerror("Invalid Location", "The selected location is either not empty or invalid.")

    load_button = tk.Button(root, text="Load Container", command=handle_load)
    load_button.pack()

def unload_container():
    global file
    location_label = tk.Label(root, text="Enter the desired unload location (e.g., 01,02):")
    location_label.pack()
    location_entry = tk.Entry(root)
    location_entry.pack()

    def handle_unload():
        location = location_entry.get().strip()
        if location in file["Position"].values and file.loc[file["Position"] == location, "Container"].values[0] != "UNUSED" and file.loc[file["Position"] == location, "Container"].values[0] != "NAN":
            file.loc[file["Position"] == location, "Container"] = "UNUSED"
            file.loc[file["Position"] == location, "Weight"] = "00000"
            GUI()
        else:
            messagebox.showerror("Invalid Location", "The selected location is either empty or invalid.")

    unload_button = tk.Button(root, text="Unload Container", command=handle_unload)
    unload_button.pack()

credentials_tab()
root.title("Fragile Express")
root.geometry("1024x768")
root.configure(background="lightblue")

root.mainloop()