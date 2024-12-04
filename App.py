# The main App for our project. This handles page shifts and direct calls for certain features like balance and load/unload,etc
import tkinter as tk
from itertools import combinations
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from _new_balance_alg import process_manifest,load_manifest

#https://docs.python.org/3/library/dialog.html#
# For login, reference https://www.w3resource.com/python-exercises/tkinter/python-tkinter-basic-exercise-16.phpx



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
    #messagebox.showinfo("Manifest File", manifest_file)

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
    
    def GUI(file):
        global rr

        
        
        rr = tk.Frame(root)
        rr.pack(anchor="n",expand=True)
        rows = 8

        while rows > 0: 
            for k in range(12):
                v = tk.StringVar()

                if rows == 8:
                    if file["Container"][k] == "NAN":
                        color = "gray"
                    
                    
                    if file["Container"][k] != "NAN" and file["Container"][k] != "UNUSED":
                        color = "green"
                    
                    v.set(file["Position"][k]+"\n"+file["Weight"][k] + "\n"+file["Container"][k])
                
                else: 
                    if file["Container"][(8-rows)*12+k] == "NAN":
                        color = "gray"

                    if file["Container"][(8-rows)*12+k] != "NAN" and file["Container"][(8-rows)*12+k] !="UNUSED":
                        color = "green"
                    
                    v.set(file["Position"][(8-rows)*12+k]+"\n"+file["Weight"][(8-rows)*12+k] + "\n"+file["Container"][(8-rows)*12+k])
                    
                    
            
                
                message = tk.Message(rr,relief="raised",width=100,textvariable=v,bg=color)
                color = "white"
                message.grid(padx=10,pady=10,row=rows,column=k)

            rows-=1
    
    
    
    file2 = load_manifest(process_manifest(path,output_file="balance.txt"))
    GUI(file)
    

    def t():
        rr.destroy()
        #Load_unload_tab
        button3.destroy()
        global button4
        global instructions
        
        GUI(file2)

        instructions = tk.Text(root)
        instructions.insert(tk.END,"Moving container Rations for US Army from [02,02] to [02,01] with weight 20")
        instructions.pack(expand=True)
        instructions.config(state="disabled",width=50,height=1,font=(30))

        button4 = tk.Button(root,text="Finish",height=5,width=15,command=Load_unload_tab)
        button4.pack(expand=True,side="top")


    
    button3 = tk.Button(root,text="continue",height=5,width=15,command=t)
    button3.pack(expand=True,side="top")


    


    #Load_unload_tab()




    

    



def Load_unload_tab():

    timer_label.destroy()
    button4.destroy()
    rr.destroy()
    instructions.destroy()

    

    
    t= 0

    






credentials_tab()
root.title("Fragile Express")
root.geometry("1024x768")
root.configure(background="lightblue")

root.mainloop()