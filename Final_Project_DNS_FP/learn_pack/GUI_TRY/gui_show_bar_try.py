#!/usr/bin/python3
import time

from GUI.widgets.progress_widegt.gui_prog_bar_control import ctor_control_prog_by_widget, ProgBarGUIControl
from GUI.widgets.progress_widegt.prog_widget import *

class RunMe:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.geometry("1024x768")
        self.prog_frame_1 = ProgressWidget(toplevel1, jump=10)
        self.prog_frame_2 = ProgressWidget(toplevel1, jump=10)  # jump 15
        self.prog_frame_3 = ProgressWidget(toplevel1, jump=20)
        self.prog_frame_4 = ProgressWidget(toplevel1)
        self.widget_control_2 = ctor_control_prog_by_widget(self.prog_frame_2)(jump=15, title="second by try")
        self.class_control_prog_4 = ctor_control_prog_by_widget(self.prog_frame_4)
        button3 = ttk.Button(toplevel1)
        button3.configure(text='press me')
        button3.grid(row=toplevel1.grid_size()[1], column=0)
        button3.configure(command=self.push_all)
        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def push_all(self):

        self.prog_frame_1.update_bar()

        self.widget_control_2()     # self.prog_frame_2.update_bar()

        self.prog_frame_3()  # self.prog_frame_3.update_bar()

        with self.class_control_prog_4(jump=25, title='"with-as" bar 4') as bar:
            num_rounds = bar.total_rounds()
            for i in range(num_rounds):
                bar()
                time.sleep(0.5)
                # self.mainwindow.update()


if __name__ == "__main__":
    app = RunMe()
    app.run()
