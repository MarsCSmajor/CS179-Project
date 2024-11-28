import tkinter as tk

from tkinter import messagebox

root = tk.Tk()

dataset = ["root"]

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
            messagebox.showerror("Login Failed")

    

    button = tk.Button(root,text="login",command=login)
    button.pack()



def upload_manifest_tab():
    
    credential.destroy()
    button.destroy()
    username.destroy()

    global upload_manifest
    global button2

    upload_manifest = tk.Label(root, text="Upload manifest")
    upload_manifest.pack()

    button2 = tk.Button(root,text="upload",command=main_menu_tab)
    button2.pack()



def main_menu_tab(): 
    upload_manifest.destroy()
    button2.destroy()

    global msg
    global Balance
    global Load_unload


    msg = tk.Label(root,text="Choose a task")
    msg.pack()

    Balance = tk.Button(root, text="Balance",command=Balance_tab,height=30,width=30,fg="blue",background="gray")
    Balance.pack(side="left",expand=True)
    
    
    Load_unload = tk.Button(root, text="Load / Unload",command=Load_unload_tab,height=30,width=30,fg = "red", background="gray")
    Load_unload.pack(side = "right",expand=True)




def Balance_tab():

    msg.destroy()
    Balance.destroy()
    Load_unload.destroy()


def Load_unload_tab():
    t= 0

    


credentials_tab()






root.title("Fragile Express")
root.geometry("1024x768")

root.mainloop()