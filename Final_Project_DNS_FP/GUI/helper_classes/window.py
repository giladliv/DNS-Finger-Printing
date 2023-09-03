import tkinter as tk
import tkinter.ttk as ttk

class Window:
    def __init__(self, master=None):
        self.master = master
        self.toplevel = tk.Tk() if master is None else tk.Toplevel(master)

    def hide_window(self):
        if self.toplevel is None:
            return False
        self.toplevel.withdraw()
        return True

    def show_window(self):
        if self.toplevel is None:
            return False
        self.toplevel.deiconify()
        return True