# Right now this code can import and export manifest (meanwhile deleting)
# This code also uses brute force appraoch to access/transfer container content
# TODO:
# Use more efficient logic to read from manifest and transfer container
# Display instruction for operator to follow

import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar, Text

# Initialize global variable for manifest lines
manifest_lines = []

def open_file():
    """Opens a text file and displays its content."""
    global manifest_lines
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")],
        title="Open a text file"
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                manifest_lines = file.readlines()
                update_text_area()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}")

def update_text_area():
    """Update the text area to display the current manifest."""
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, ''.join(manifest_lines))

def modify_manifest(action):
    """Modify the manifest based on the action."""
    global manifest_lines

    if action == "add_12345_cat":
        # Add weight 12345 and content cat to position [01,01]
        for i, line in enumerate(manifest_lines):
            if "[01,01]" in line:
                manifest_lines[i] = "[01,01], {12345}, cat\n"
                break

    elif action == "add_54321_dog":
        # Add weight 54321 and content dog to position [01,01]
        for i, line in enumerate(manifest_lines):
            if "[01,01]" in line:
                manifest_lines[i] = "[01,01], {54321}, dog\n"
                break

    elif action == "clean_01_01":
        # Clean position [01,01]
        for i, line in enumerate(manifest_lines):
            if "[01,01]" in line:
                manifest_lines[i] = "[01,01], {00000}, UNUSED\n"
                break

    elif action == "move_01_01_to_02_03":
        # Move container's weight and content from [01,01] to [02,03]
        current_data = None
        for i, line in enumerate(manifest_lines):
            if "[01,01]" in line:
                current_data = [part.strip() for part in line.split(",")[1:]]  # Extract weight and content
                manifest_lines[i] = "[01,01], {00000}, UNUSED\n"  # Clear current position
                break
        for i, line in enumerate(manifest_lines):
            if "[02,03]" in line and current_data:
                manifest_lines[i] = f"[02,03], {current_data[1]}, {current_data[2]}\n"
                break

    elif action == "move_02_03_to_01_01":
        # Move container's weight and content from [02,03] to [01,01]
        current_data = None
        for i, line in enumerate(manifest_lines):
            if "[02,03]" in line:
                current_data = line.split(",")[1:]  # Extract weight and content
                manifest_lines[i] = "[02,03], {00000}, UNUSED\n"  # Clear current position
                break
        for i, line in enumerate(manifest_lines):
            if "[01,01]" in line and current_data:
                manifest_lines[i] = f"[01,01], {current_data[1].strip()}, {current_data[2].strip()}\n"
                break

    elif action == "export_manifest":
        # Export the current manifest to a file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Manifest"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(manifest_lines)
                messagebox.showinfo("Success", "Manifest exported successfully!")
                manifest_lines = []  # Clear the current manifest
                update_text_area()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    update_text_area()

# Create the main window
root = tk.Tk()
root.title("Manifest Viewer")
root.geometry("600x400")  # Set a default size
root.resizable(True, True)  # Allow resizing

# Create Open button
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

open_button = tk.Button(button_frame, text="Open Manifest", command=open_file)
open_button.pack(side=tk.LEFT, padx=5)

# Create action buttons
actions_frame = tk.Frame(root)
actions_frame.pack(pady=10)

add_12345_cat_button = tk.Button(actions_frame, text="Add 12345 Weight Cat in 01,01", command=lambda: modify_manifest("add_12345_cat"))
add_12345_cat_button.pack(side=tk.LEFT, padx=5)

add_54321_dog_button = tk.Button(actions_frame, text="Add 54321 Weight Dog in 01,01", command=lambda: modify_manifest("add_54321_dog"))
add_54321_dog_button.pack(side=tk.LEFT, padx=5)

clean_button = tk.Button(actions_frame, text="Clean 01,01", command=lambda: modify_manifest("clean_01_01"))
clean_button.pack(side=tk.LEFT, padx=5)

move_01_01_to_02_03_button = tk.Button(actions_frame, text="Move from 01,01 to 02,03", command=lambda: modify_manifest("move_01_01_to_02_03"))
move_01_01_to_02_03_button.pack(side=tk.LEFT, padx=5)

move_02_03_to_01_01_button = tk.Button(actions_frame, text="Move from 02,03 to 01,01", command=lambda: modify_manifest("move_02_03_to_01_01"))
move_02_03_to_01_01_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(actions_frame, text="Export Manifest", command=lambda: modify_manifest("export_manifest"))
export_button.pack(side=tk.LEFT, padx=5)

# Create a text area with a scrollbar
text_frame = tk.Frame(root)
text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_area = Text(text_frame, wrap=tk.WORD, width=50, height=15, yscrollcommand=scrollbar.set)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=text_area.yview)

# Run the Tkinter event loop
root.mainloop()





