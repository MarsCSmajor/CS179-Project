import tkinter as tk

def visualize_manifest(manifest_lines):
    rows, cols = 8, 12
    manifest_grid = [["UNUSED" for _ in range(cols)] for _ in range(rows)]
    for line in manifest_lines:
        if line.strip():
            position, weight, label = line.strip().split(", ")
            row, col = map(int, position.strip("[]").split(","))
            manifest_grid[row-1][col-1] = f"{label.strip()} ({weight.strip('{}')})"
    root = tk.Tk()
    root.title("Manifest Visualization")
    for r, row in enumerate(manifest_grid):
        for c, cell in enumerate(row):
            cell_label = tk.Label(root, text=cell, borderwidth=1, relief="solid", width=15, height=2)
            cell_label.grid(row=r, column=c)
    tk.Button(root, text="Close", command=root.destroy).grid(row=9, column=0, columnspan=12)
    root.mainloop()