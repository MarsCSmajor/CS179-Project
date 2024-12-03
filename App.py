import tkinter as tk
import pandas as pd
from itertools import combinations

from _new_balance_alg import process_manifest
from _new_balance_alg import load_manifest

#https://docs.python.org/3/library/dialog.html#

from tkinter import messagebox

from tkinter.filedialog import askopenfilename




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
    messagebox.showinfo("Manifest File", manifest_file)

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




def Balance_tab():

    global rr
    global file
    global button3
    global timer_label
    msg.destroy()
    Balance.destroy()
    Load_unload.destroy()



    timer_label = tk.Label(root, text="estimated time remanining",padx=10,pady=5)
    timer_label.pack()

    file = load_manifest(path)
    def GUI():

        rr = tk.Frame(root)
        rr.pack(anchor="n",expand=True)
        for i in range(8):
            for k in range(12):
                v = tk.StringVar()
                message = tk.Message(rr,relief="raised",width=100,textvariable=v)
                if k !=12 and i == 0:
                    v.set(file["Weight"][k]+file["Container"][k])
                else:
                    v.set(file["Weight"][12*i + k]+file["Container"][12*i+k])
                

                message.grid(row=i,column=k,padx=10,pady=10)

    GUI()

    button3 = tk.Button(root,text="continue",height=5,width=15)
    button3.pack(expand=True,side="top")




    

    



def Load_unload_tab():
    t= 0

    






credentials_tab()
root.title("Fragile Express")
root.geometry("1024x768")
root.configure(background="lightblue")

root.mainloop()