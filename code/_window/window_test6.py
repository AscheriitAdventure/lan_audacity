import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Practice with Grid")
root.geometry("210x180")

# Configure the grid
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=3)

# Configure List box
btn_show_lb = ttk.Label(root, text="Show List Box")
btn_show_lb.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

label_lb = ttk.Label(root, text="List Box Device")
label_lb.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

lb_device = tk.Listbox(root, selectmode=tk.BROWSE, width=24)
lb_device.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
cities = ["Beijing", "Singapore", "Tokyo", "Dubai", "New York"]
for c in cities:
    lb_device.insert(tk.END, c)

# Configure le Terminal
btn_show_console = ttk.Label(root, text="Show Console")
btn_show_console.grid(column=3, row=0, sticky=tk.E, padx=5, pady=5)

label_console = ttk.Label(root, text="Console Device")
label_console.grid(column=3, row=1, sticky=tk.E, padx=5, pady=5)

root.mainloop()
