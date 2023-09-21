import tkinter as tk
import tkinter.ttk as ttk

class Window:
    def __init__(self, wind_master=None):
        self.wind_master: Window = wind_master
        self.master = None if wind_master is None else self.wind_master.master
        self.toplevel = tk.Tk() if self.master is None else tk.Toplevel(self.master)
        self.toplevel.bind("<Destroy>", self.on_destroy)
        self.__to_show_prev_wind = True
        self.__connected_winds = set()
        self.__connect_win_from_parent()
        self.init_window()

    def init_window(self):
        pass

    def __connect_win_from_parent(self):
        if self.wind_master is not None:
            self.wind_master.__connected_winds.add(self)

    def __disconnect_wind_from_parent(self):
        if self.wind_master is not None:
            self.wind_master.__connected_winds.remove(self)

    def get_top_level(self):
        return self.toplevel

    def set_show_prev_wind(self, to_show: bool = True):
        self.__to_show_prev_wind = to_show

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

    def on_destroy(self, event):
        # if it is the last one or the flag to present the previous one - than show the previous window
        if (self.__to_show_prev_wind or len(self.__connected_winds) <= 1)\
                and self.wind_master is not None:
            self.wind_master.show_window()

    def destroy_wind(self):
        self.toplevel.destroy()

    def run_window(self):
        self.toplevel.mainloop()