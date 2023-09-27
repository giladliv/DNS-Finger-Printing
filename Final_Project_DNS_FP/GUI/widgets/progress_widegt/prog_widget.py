#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from math import ceil

class ProgressWidget(ttk.Frame):
    FORMAT_PERC = '{}%'
    FORMAT_PROG_NUM = '{0} / {1}'
    FORMAT_MARK = '{}\n'
    AFTER_DOT = 2

    def __init__(self, master, total: int = 100, jump: int = 1, title: str = 'title', num_after_dot=AFTER_DOT, *args, **kwargs):
        # build ui
        # TODO: check validity
        super().__init__(master, *args, **kwargs)
        self.jump = 0
        self.total = 0
        self.__rounds = 0
        self.__grid_data = self.grid_info()
        self.__set_num_after_dot(num_after_dot=num_after_dot)   # set the number after dots to be as the input


        # build the UI
        self.__build_visual(master)

        # set the basic data
        self.set_progress(total=total, jump=jump, title=title)

    def __build_visual(self, master):
        self.master = master
        # copied from pygubu-designer
        self.configure(height=40, width=800)
        self.title_lable = ttk.Label(self)
        self.title_lable.configure(text='title')
        self.title_lable.grid(column=0, row=0)
        self.main_progressbar = ttk.Progressbar(self)
        self.prog_bar = tk.IntVar(value=0)
        self.main_progressbar.configure(
            length=600,
            orient="horizontal",
            value=0,
            variable=self.prog_bar)
        self.main_progressbar.grid(column=0, row=1)
        self.prog_label = ttk.Label(self)
        self.prog_label.configure(text='100%', width=10)
        self.prog_label.grid(column=2, row=1)
        self.space_lbl = ttk.Label(self)
        self.space_lbl.configure(text='  ')
        self.space_lbl.grid(column=1, row=1)
        self.curr_pos_label = ttk.Label(self)
        self.curr_pos_label.configure(text='- / -')
        self.curr_pos_label.grid(row=2)
        self.mark_label = ttk.Label(self)
        self.mark_label.configure(text='mark')
        self.mark_label.grid(row=3)

        # self.pack(fill="both", side="top")
        # cols, rows = self.master.grid_size()
        # self.grid(row=rows, column=0)
        self.grid_anchor("s")
        print(self.grid_info())
        # self.grid(**self.grid_info())


    def set_progress(self, total: int = 100, jump: int = 1, title: str = ''):
        self.total = abs(total)
        self.jump = abs(jump)
        self.__rounds = ceil(self.total / self.jump)

        self.set_title(title)
        self.main_progressbar['maximum'] = self.total
        self.prog_bar.set(0)
        self.prog_label['text'] = self.FORMAT_PERC.format(0)
        self.curr_pos_label['text'] = self.FORMAT_PROG_NUM.format('-', '-')
        self.mark_label['text'] = self.FORMAT_MARK.format('')
        self.__set_position(0)

    def set_title(self, title: str = 'title'):
        self.title_lable['text'] = title

    def __set_num_after_dot(self, num_after_dot):
        try:
            if not isinstance(num_after_dot, int) or num_after_dot < 0:
                raise ValueError('not int')
        except:
            num_after_dot = self.AFTER_DOT
        finally:
            self.__num_after_dot = num_after_dot


    def update_bar(self):
        # update bar for move
        self.__make_move_proccess(self.jump)
        self.refresh_wind()

    def refresh_wind(self):
        self.update()

    def __call__(self, *args, **kwargs):
        self.update_bar()

    def total_rounds(self):
        # return how many rounds for the bar
        return self.__rounds

    def __make_move_proccess(self, n: int):     # for jumping in several options
        curr_pos = self.prog_bar.get()          # get the current position
        if n >= 0:
            curr_pos = min(curr_pos + n, self.total)     # for every positive move update and take the lowest
        else:
            curr_pos = max(curr_pos + n, 0)     # for every negative move update and take the highest (0 not changing)
        self.__set_position(curr_pos)

    def __set_position(self, curr_pos: int):
        if curr_pos < 0 or curr_pos > self.total:
            return False
        # update percentage
        self.prog_label['text'] = self.FORMAT_PERC.format(self.get_percent_fixed(curr_pos, max_num=self.total, after_dot=self.__num_after_dot))
        # update how many completed
        self.curr_pos_label['text'] = self.FORMAT_PROG_NUM.format(curr_pos, self.total)
        # self.mark_label['text'] = self.FORMAT_MARK.format(f'{curr_pos} / {self.total}')
        self.prog_bar.set(curr_pos)
        return True

    @staticmethod
    def get_percent_fixed(n, max_num: int = 100, after_dot=AFTER_DOT):
        n = (n / max_num) * 100
        if n.is_integer():
            return int(n)
        else:
            return round(n, after_dot)

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.__grid_data = self.grid_info()
        # print('grid me')

    def show_prog_bar(self):
        self.grid(self.__grid_data)

    def hide_prog_bar(self):
        self.grid_forget()


