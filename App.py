# The main App for our project. This handles page shifts and direct calls for certain features like balance and load/unload,etc
import tkinter as tk
from itertools import combinations
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from _new_balance_alg import process_manifest,load_manifest,list_moves,move_crate

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
    
    
    
    
    process_manifest(path,output_file="balance.txt") # call the balance algorithm since list moves contains the steps and moves
    GUI(file)
    
    

    def t(file2,text ="",cmd=None):
        rr.destroy()
        
        button3.destroy()
        global button4
        global instructions
        
        GUI(file2)

        instructions = tk.Text(root)
        instructions.insert(tk.END,text)
        instructions.pack(expand=True)
        instructions.config(state="disabled",width=100,height=1,font=(30))

        button4 = tk.Button(root,text="Finish",height=5,width=15,command=cmd)
        button4.pack(expand=True,side="top")

    
    



    
    global cnt 
    cnt =0
    print(list_moves)
    def move(): # MOVE might have some minor bugs 
        global cnt
        
        button3.destroy()
        
        rr.destroy()


        if list_moves: # if the steps are available
        
            
            #move_crate(file,list_moves[cnt][0],list_moves[cnt][1],output_file="balance.txt")
            if cnt < len(list_moves):
                move_crate(file,list_moves[cnt][0],list_moves[cnt][1],output_file="balance.txt")

                print(f'cnt {cnt} list {len(list_moves)}')
                
                if cnt+1 == len(list_moves):
                    
                    
                    instructions.destroy()
                    button4.destroy()
                    button3.destroy()
                    t(file2=load_manifest("balance.txt"),text=f"Moving container{list_moves[cnt][0]} to  {list_moves[cnt][1]}",cmd=None)


                    messagebox.showinfo("Balance","congrats ship is balance")
                    rr.destroy()

                    trainsition_upload()    
                else:
                    t(file2=load_manifest("balance.txt"),text=f"Moving container{list_moves[cnt][0]} to  {list_moves[cnt][1]}",cmd=move)
                
                cnt +=1
                

    
                
                        
            else:
                button3.destroy()
                timer_label.destroy()
                button4.destroy()
                instructions.destroy()
                    #t(file2=load_manifest("balance.txt"),text=f"Moving container{list_moves[cnt][0]} to  {list_moves[cnt][1]}",cmd=trainsition_upload)
                messagebox.showinfo("Balance Successful","already downloaded and sent to captain")
        
        else: # if the steps was empty,the program knows that it is balance and no need to rebalance it once again
            messagebox.showwarning("Warning","Manifest is already balance. No need of rebalancing")
            trainsition_upload()
            



    def trainsition_upload(): # properly destroys the objects of the frame. Since global is used in a function that has sub functions, is not defined outside
        button3.destroy()
        timer_label.destroy()
        button4.destroy()
        rr.destroy()
        list_moves.clear()
        instructions.destroy()
        upload_manifest_tab()
        
            


    button3 = tk.Button(root,text="Continue",height=5,width=15,command=move)
    button3.pack(expand=True,side="top")



def Load_unload_tab():
    
    

    
    t= 0

    






credentials_tab()
root.title("Fragile Express")
root.geometry("1024x768")
root.configure(background="lightblue")

root.mainloop()