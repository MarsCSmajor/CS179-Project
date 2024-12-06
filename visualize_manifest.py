import tkinter as tk

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