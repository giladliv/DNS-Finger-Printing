#!/usr/bin/python3
import tkinter as tk
from prog_set import *

class RunMe:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.geometry("800x600")
        prog_frame_1 = ProgressSet(toplevel1)
        prog_frame_2 = ProgressSet(toplevel1)
        prog_frame_3 = ProgressSet(toplevel1)
        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = RunMe()
    app.run()
