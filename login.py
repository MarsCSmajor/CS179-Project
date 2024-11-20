import tkinter as tk

from tkinter import messagebox 


database = ["admin"] # temporary data base to access username

def validation(): 
    name = credential_entry.get()

    if name == "": 
        messagebox.showerror("no username was found or invalid")
        
    
    elif name in database: 
        messagebox.showinfo("Login successfully","Welcome back ")
        
        
    


transition = True

window = tk.Tk()
window.geometry("640x480")

window.title("Fragile Express ")

credential = tk.Label(window, text=" username")
credential.pack()

credential_entry = tk.Entry(window)
credential_entry.pack()

button = tk.Button(window,text="Login",command=validation())
button.pack()






window.mainloop() # main 