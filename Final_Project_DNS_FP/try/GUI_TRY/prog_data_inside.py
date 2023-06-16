import tkinter as tk
from tkinter import ttk

def update_progress():
    progress_value = progress_var.get()
    if progress_value < 100:
        progress_var.set(progress_value + 10)
        progressbar['value'] = progress_var.get()
        percent_label['text'] = f"{progress_var.get()}%"

root = tk.Tk()
root.title("Progress Bar Example")

progress_var = tk.IntVar()
progress_var.set(0)

frame = ttk.Frame(root, padding=20)
frame.pack()

progressbar = ttk.Progressbar(frame, length=300, mode='determinate', variable=progress_var)
progressbar.grid(row=0, column=0, columnspan=2, pady=10)

percent_label = ttk.Label(frame, text="0%")
percent_label.grid(row=1, column=0, padx=(0, 5))

start_button = ttk.Button(frame, text="Start", command=update_progress)
start_button.grid(row=1, column=1, padx=(5, 0))

root.mainloop()
