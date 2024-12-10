# The main App for our project. This handles page shifts and direct calls for certain features like balance and load/unload,etc
import tkinter as tk
from itertools import combinations
from tkinter import messagebox,filedialog
from tkinter.filedialog import askopenfilename
from _new_balance_alg import process_manifest,load_manifest,list_moves,move_crate,save_manifest

import os
from datetime import datetime


LOG = "KeoghsPort2024.txt" # Brent's log function
def log_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG, "a") as log: 
        log.write(f"{timestamp}: {event}\n")

#https://docs.python.org/3/library/dialog.html#
# For login, reference https://www.w3resource.com/python-exercises/tkinter/python-tkinter-basic-exercise-16.phpx



root = tk.Tk()

#dataset = ["root"]
#dataset = ["Micheal","Gabriel", "Owner"] #testing
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
            name = username.get()
            log_event(f"{name} signs in")
            upload_manifest_tab()



        else: 
            messagebox.showerror("Login Failed","invalid credentials")

    

    button = tk.Button(root,text="login",command=login)
    button.pack()



def open_manifest(): 
    global file
    global manifest_file # Manifest file can be access anywhere in the program since is global
    global path
    path = askopenfilename(filetypes=[("Text Files", "*.txt")])
    with open(path, 'r') as m:
        
        manifest_file = m.read()
        file = load_manifest(path)
        container_count = file[(file['Container'] != "NAN") & (file["Container"] != "UNUSED")]['Container'].nunique() # counts the number of containers in the manifest

    log_event(f"Manifest {os.path.basename(path)} is oppened, there are {container_count} containers") # saves the information in the log file    

    #messagebox.showinfo("Manifest File", manifest_file)
    
    main_menu_tab()
        
  



def upload_manifest_tab():
    
    credential.destroy()
    button.destroy()
    username.destroy()

    global upload_manifest
    global button2


    list_moves.clear()
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

    #messagebox.showinfo("Info","Ready to balance")

    timer_label = tk.Label(root, text="estimated time remanining",padx=10,pady=5)
    timer_label.pack()

    

    file = load_manifest(path)
    rename = os.path.splitext(os.path.basename(path))[0] # to get correct format like case1OUTBOUND.txt
    
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
    
    
    
    
    process_manifest(path,output_file=rename+"OUTBOUND.txt") # call the balance algorithm since list moves contains the steps and moves
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

    
    


    
    global distance
    distance =4
    global cnt 
    cnt =0
    print(list_moves)
    def move(): # MOVE might have some minor bugs 
        global cnt
        global distance
        
        #button3.destroy()
        for widget in root.winfo_children():
            widget.destroy()
        #rr.destroy()


        if list_moves: # if the steps are available
        
            
            #move_crate(file,list_moves[cnt][0],list_moves[cnt][1],output_file="balance.txt")
            if cnt < len(list_moves):
                move_crate(file,list_moves[cnt][0],list_moves[cnt][1],output_file=rename+"OUTBOUND.txt")

                print(f'cnt {cnt} list {len(list_moves)}')
                
                if cnt+1 == len(list_moves):
                    
                    
                    # instructions.destroy()
                    # button4.destroy()
                    # button3.destroy()
                    for widget in root.winfo_children():
                        widget.destroy()
                        
                    distance += abs(list_moves[cnt][1][0] - list_moves[cnt][0][0]) + abs(list_moves[cnt][1][1] - list_moves[cnt][0][1])
                    t(file2=load_manifest(rename+"OUTBOUND.txt"),text=f"Moving container{list_moves[cnt][0]} to  {list_moves[cnt][1]} Est time {distance} minutes",cmd=None)


                    messagebox.showinfo("Balance","congrats ship is balance")
                    #rr.destroy()

                    trainsition_upload()    
                else:
                    distance += abs(list_moves[cnt][1][0] - list_moves[cnt][0][0]) + abs(list_moves[cnt][1][1] - list_moves[cnt][0][1])

                    t(file2=load_manifest(rename+"OUTBOUND.txt"),text=f"Moving container{list_moves[cnt][0]} to  {list_moves[cnt][1]} Est time: {distance} minutes",cmd=move)
                
                cnt +=1
                

    
                
                        
            else:
                # button3.destroy()
                # timer_label.destroy()
                # button4.destroy()
                # instructions.destroy()
                for widget in root.winfo_children():
                    widget.destroy()
                list_moves.clear()
                    
                messagebox.showinfo("Balance Successful","already downloaded and sent to captain")



                
        
        else: # if the steps was empty,the program knows that it is balance and no need to rebalance it once again
            messagebox.showwarning("Warning","Manifest is already balance. No need of rebalancing")
            trainsition_upload()
            



    def trainsition_upload(): # properly destroys the objects of the frame. Since global is used in a function that has sub functions, is not defined outside
        # button3.destroy()
        # timer_label.destroy()
        # button4.destroy()
        # rr.destroy()
        # list_moves.clear()
        # instructions.destroy()
        for widget in root.winfo_children():
            widget.destroy()
        upload_manifest_tab()
        
            


    button3 = tk.Button(root,text="Continue",height=5,width=15,command=move)
    button3.pack(expand=True,side="top")


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




def Load_unload_tab():
    global file
    global button3
    global timer_label    


    # Jay's load and unload
    #  

    msg.destroy()
    Balance.destroy()
    Load_unload.destroy()

    timer_label = tk.Label(root, text="estimated time remanining", padx=10, pady=5)
    timer_label.pack()

    #file = load_manifest(path)
    GUI()

    def handle_back_action():
        clear_all_widgest(root)
        upload_manifest_tab()

    def handle_done_action():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="testOUTBOUND.txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            save_manifest(file,file_path)
            clear_all_widgest(root)
            upload_manifest_tab()

    def handle_reset_action():
        clear_all_widgest(root)
        Load_unload_tab()

    frame = tk.Frame(root)
    frame.pack(expand=True, side="top")
    frame.configure(background="lightblue")
    back_button = tk.Button(frame, text="Back", command=handle_back_action)
    back_button.pack(side="left")
    done_button = tk.Button(frame, text="Done/Download Updated Manifest", command=handle_done_action)
    done_button.pack(side="left")
    reset_button = tk.Button(frame, text="Restart", command=handle_reset_action)
    reset_button.pack(side="left")

    user_action_label = tk.Label(root, text="Enter 'load' to load a container or 'unload' to unload a container:")
    user_action_label.pack()
    user_action_entry = tk.Entry(root)
    user_action_entry.pack()

    def handle_action():
        user_action = user_action_entry.get().lower()
        if user_action == "load":
            user_action_entry.config(state="disabled")
            submit_action_button.destroy() # avoid repeat submit
            load_container()
        elif user_action == "unload":
            user_action_entry.config(state="disabled")
            submit_action_button.destroy() # avoid repeat submit
            unload_container()
        else:
            messagebox.showerror("Invalid Action", "Please enter 'load' or 'unload'")

    submit_action_button = tk.Button(root, text="Submit", command=handle_action)
    submit_action_button.pack()

def validate_location(location):
    matching_rows = file.loc[file["Position"] == location]
    if not matching_rows.empty:
        container_status = matching_rows["Container"].values[0]
        return container_status
    else:
        return None

def clear_all_widgest(parent):
    for widget in parent.winfo_children():
        widget.destroy()

def load_container():
    global file

    location_label = tk.Label(root, text="Enter the desired load container location (e.g., [01,02])")
    location_label.pack()
    location_entry = tk.Entry(root)
    location_entry.pack()

    def handle_load():
        location = location_entry.get().strip()
        container_status = validate_location(location)

        if container_status:
            if container_status == "UNUSED":
                load_button.destroy()
                container_name_label = tk.Label(root, text="Enter the container name:")
                container_name_label.pack()
                container_name_entry = tk.Entry(root)
                container_name_entry.pack()

                container_mass_label = tk.Label(root, text="Enter the container mass (e.g., {00000}):")
                container_mass_label.pack()
                container_mass_entry = tk.Entry(root)
                container_mass_entry.pack()

                def finalize_load():
                    container_name = container_name_entry.get().strip()
                    container_mass = container_mass_entry.get().strip()
                    file.loc[file["Position"] == location, "Container"] = container_name
                    file.loc[file["Position"] == location, "Weight"] = container_mass

                    log_event(f"'{container_name}' container is loaded") # when a valid container is loaded in manifest, keep a log record of it

                    clear_all_widgest(root)
                    Load_unload_tab()

                finalize_button = tk.Button(root, text="Finalize Load", command=finalize_load)
                finalize_button.pack()
            else:
                messagebox.showerror("Invalid Location", f"Location is not UNUSED. Current Status: {container_status}")
        else:
            messagebox.showerror("Invalid Location", f"No Matching location found for: {location}")

    load_button = tk.Button(root, text="Load Container", command=handle_load)
    load_button.pack()

def unload_container():
    global file

    location_label = tk.Label(root, text="Enter the desired load container location (e.g., [01,02])")
    location_label.pack()
    location_entry = tk.Entry(root)
    location_entry.pack()

    def handle_unload():
        location = location_entry.get().strip()
        container_status = validate_location(location)

        if container_status:
            if container_status != "UNUSED" and container_status != "NAN":

                log_event(f"'{container_status}' container is offloaded") # keeps log record of the container that was unloaded

                file.loc[file["Position"] == location, "Container"] = "UNUSED"
                file.loc[file["Position"] == location, "Weight"] = "{00000}"
                clear_all_widgest(root)
                Load_unload_tab()
            else:
                messagebox.showerror("Invalid Location", f"Location is UNUSED")
        else:
            messagebox.showerror("Invalid Location", f"No Matching location found for: {location}")
    unload_button = tk.Button(root, text="Finalize Unload", command=handle_unload)
    unload_button.pack()
    

    






credentials_tab()
root.title("Fragile Express")
root.geometry("1024x768")
root.configure(background="lightblue")

root.mainloop()