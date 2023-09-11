#!/usr/bin/python3

from GUI.widgets.progress_widegt.prog_widget import *

class RunMe:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.geometry("1024x768")
        self.prog_frame_1 = ProgressWidget(toplevel1, jump=10)
        self.prog_frame_2 = ProgressWidget(toplevel1, jump=15)
        self.prog_frame_3 = ProgressWidget(toplevel1, jump=20)

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
        self.prog_frame_3()  # self.prog_frame_3.update_bar()


if __name__ == "__main__":
    app = RunMe()
    app.run()
