#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class ProgressSet:
    FORMAT_PERC = '{}%'
    FORMAT_PROG_NUM = '{0} / {1}'
    FORMAT_MARK = '{}\n'

    def __init__(self, master, max_size: int = 100, jump: int = 1, title: str = 'title'):
        # build ui
        # TODO: check validity
        self.jump = 0
        self.max_size = 0

        self.__build_visual(master)

        # set the basic data
        self.set_progress(max_size, jump)

    def __build_visual(self, toplevel1):
        self.toplevel1 = toplevel1

        self.title_lable = ttk.Label(self.toplevel1)
        self.title_lable.configure(text='title')
        self.title_lable.pack(side="top")
        self.frame1 = ttk.Frame(self.toplevel1)
        self.frame1.configure(height=40, width=800)
        self.progressbar1 = ttk.Progressbar(self.frame1)
        self.prog_bar = tk.IntVar(value=0)
        self.progressbar1.configure(
            length=600,
            orient="horizontal",
            value=0,
            variable=self.prog_bar)
        self.progressbar1.grid(column=0, row=0)
        self.prog_label = ttk.Label(self.frame1)
        self.prog_label.configure(
            compound="center",
            justify="center",
            text='0%')
        self.prog_label.grid(column=0, row=1)
        self.curr_pos_label = ttk.Label(self.frame1)
        self.curr_pos_label.configure(compound="center", text='-/-')
        self.curr_pos_label.grid(column=0, row=2)
        self.frame1.pack(fill="both", side="top")
        self.frame1.grid_anchor("s")
        self.mark_label = ttk.Label(self.toplevel1)
        self.mark_label.configure(text='mark')
        self.mark_label.pack(side="top")



    def set_progress(self, max_size: int = 100, jump: int = 1):
        self.max_size = abs(max_size)
        self.jump = abs(jump)
        self.progressbar1['maximum'] = self.max_size
        self.prog_bar.set(0)
        self.prog_label['text'] = self.FORMAT_PERC.format(0)
        self.curr_pos_label['text'] = self.FORMAT_PROG_NUM.format('-', '-')
        self.mark_label['text'] = self.FORMAT_MARK.format('')
    def __make_move_proccess(self, n: int):     # for jumping in several options
        curr_pos = self.prog_bar.get()          # get the current position
        if n >= 0:
            curr_pos = min(curr_pos + n, self.max_size)     # for every positive move update and take the lowest
        else:
            curr_pos = max(curr_pos + n, 0)     # for every negative move update and take the highest (0 not changing)
        self.__set_position(curr_pos)

    def __set_position(self, curr_pos: int):
        if curr_pos < 0 or curr_pos > self.max_size:
            return False
        # update percentage
        self.prog_label['text'] = self.FORMAT_PERC.format(self.get_percent_fixed(curr_pos, self.max_size))
        # update how many completed
        self.curr_pos_label['text'] = self.FORMAT_PROG_NUM.format(curr_pos, self.max_size)
        # self.mark_label['text'] = self.FORMAT_MARK.format(f'{curr_pos} / {self.max_size}')
        self.prog_bar.set(curr_pos)
        return True


    # update bar for move
    def update_bar(self):
        self.__make_move_proccess(self.jump)


    @staticmethod
    def get_percent_fixed(n, max_num: int = 100, after_dot=2):
        n = n / max_num * 100
        if n.is_integer():
            return int(n)
        else:
            return round(n, after_dot)
