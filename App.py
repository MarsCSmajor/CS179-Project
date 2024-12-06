import tkinter as tk
#https://docs.python.org/3/library/dialog.html#

from tkinter import messagebox

from tkinter.filedialog import askopenfilename




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
            messagebox.showerror("Login Failed","invalid credentials")

    

    button = tk.Button(root,text="login",command=login)
    button.pack()



def open_manifest(): 
    global manifest_file
    path = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not path:
        return
    try:
        with open(path, 'r') as m:
            manifest_file = m.readlines()
        print("Manifest Content:", manifest_file)
        visualize_manifest(manifest_file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load manifest: {e}")

def visualize_manifest(manifest_lines):
    rows, cols = 8, 12
    manifest_grid = [["" for _ in range(cols)] for _ in range(rows)]
    cell_colors = [["white" for _ in range(cols)] for _ in range(rows)]

    for line in manifest_lines:
        if line.strip():
            position, weight, label = line.strip().split(", ")
            row, col = map(int, position.strip("[]").split(","))
            label = label.strip()
            manifest_grid[row-1][col-1] = label
            if label.lower() == "unused":
                cell_colors[row-1][col-1] = "black"

    grid_window = tk.Toplevel(root)
    grid_window.title("Manifest Visualization")

    for r in range(rows):
        for c in range(cols):
            cell_label = tk.Label(
                grid_window,
                text=manifest_grid[r][c],
                borderwidth=1,
                relief="solid",
                width=10,
                height=2,
                bg=cell_colors[r][c],
                fg="red" if manifest_grid[r][c] else "black"
            )
            cell_label.grid(row=r, column=c, padx=1, pady=1)

    close_button = tk.Button(grid_window, text="Close", command=grid_window.destroy)
    close_button.grid(row=rows, column=0, columnspan=cols, pady=10)


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

    msg.destroy()
    Balance.destroy()
    Load_unload.destroy()


def Load_unload_tab():
    t= 0

    






credentials_tab()
root.title("Fragile Express")
root.geometry("1024x768")
root.configure(background="lightblue")

root.mainloop()