#!/usr/bin/python3
import time

from GUI.widgets.progress_widegt.gui_prog_bar_control import ctor_control_prog_by_widget, ProgBarGUIControl
from GUI.widgets.progress_widegt.prog_widget import *

class RunMe:
    def __init__(self, master=None):
        # build ui
        self.master = tk.Tk() if master is None else tk.Toplevel(master)
        self.master.configure(height=200, width=200)
        self.master.geometry("1024x768")
        self.frame2 = ttk.Frame(self.master)
        self.frame2.configure(height=200, width=200)

        self.prog_frame_1 = ProgressWidget(self.frame2, jump=10)
        self.prog_frame_1.grid(row=0, columnspan=2, sticky="ew")
        self.prog_frame_2 = ProgressWidget(self.frame2, jump=10)  # jump 15
        self.prog_frame_2.grid(row=1, columnspan=2, sticky="ew")
        self.prog_frame_3 = ProgressWidget(self.frame2, jump=20)
        self.prog_frame_3.grid(row=2, columnspan=2, sticky="ew")
        self.prog_frame_4 = ProgressWidget(self.frame2)
        self.prog_frame_4.grid(row=3, columnspan=2, sticky="ew")

        self.show_run_4 = True

        self.widget_control_2 = ctor_control_prog_by_widget(self.prog_frame_2)(jump=15, title="second by try")
        self.class_control_prog_4 = ctor_control_prog_by_widget(self.prog_frame_4)
        button3 = ttk.Button(self.frame2)
        button3.configure(text='press me')
        button3.configure(command=self.push_all)
        button3.grid(row=4)
        self.prog_frame_4.grid(row=3, columnspan=2)
        # Main widget
        self.frame2.pack(side="top")
        # self.set_all_widgets_in_order()
        self.mainwindow = self.master

    def run(self):
        self.mainwindow.mainloop()

    def push_all(self):

        self.prog_frame_1.update_bar()

        self.widget_control_2()     # self.prog_frame_2.update_bar()

        self.prog_frame_3()  # self.prog_frame_3.update_bar()

        # this is for checking the hiding method
        if self.show_run_4:
            self.prog_frame_4.show_prog_bar()
            with self.class_control_prog_4(jump=25, title='"with-as" bar 4') as bar:
                num_rounds = bar.total_rounds()
                for i in range(num_rounds):
                    bar()
                    time.sleep(0.5)
        else:
            self.prog_frame_4.hide_prog_bar()

        self.show_run_4 = not self.show_run_4
                    # self.mainwindow.update()
    def set_all_widgets_in_order(self):
        for widget in self.frame2.winfo_children():
            # if the widget is already in the grid continue
            if len(widget.grid_info()) > 0:
                continue
            cols, rows = self.frame2.grid_size()
            widget.grid(row=rows, column=0)

if __name__ == "__main__":
    app = RunMe()
    app.run()
