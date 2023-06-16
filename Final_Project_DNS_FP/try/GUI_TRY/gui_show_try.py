#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk

from prog_set import *

class RunMe:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.geometry("800x600")
        self.prog_frame_1 = ProgressSet(toplevel1, jump=10)
        self.prog_frame_2 = ProgressSet(toplevel1, jump=15)
        self.prog_frame_3 = ProgressSet(toplevel1, jump=20)
        button3 = ttk.Button(toplevel1)
        button3.configure(text='press me')
        button3.pack(side="top")
        button3.configure(command=self.push_all)
        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def push_all(self):
        self.prog_frame_1.update_bar()
        self.prog_frame_2.update_bar()
        self.prog_frame_3.update_bar()


if __name__ == "__main__":
    app = RunMe()
    app.run()
