#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class ProgressSet:
    FORMAT_PERC = '    {}%'
    FORMAT_MARK = '{}\n'

    def __init__(self, master, max_size: int = 100, jump: int = 1, title: str = 'title'):
        # build ui
        self.max_size = max_size
        self.jump = jump
        self.title_lable = ttk.Label(master)
        self.title_lable.configure(text=title)
        self.title_lable.pack(side="top")
        frame1 = ttk.Frame(master)
        frame1.configure(height=200, width=200)
        self.progressbar1 = ttk.Progressbar(frame1)
        self.prog_bar = tk.IntVar(value=0)
        self.progressbar1.configure(
            length=600,
            orient="horizontal",
            value=0,
            maximum=self.max_size,
            variable=self.prog_bar)
        self.progressbar1.pack(side="left")
        self.prog_label = ttk.Label(frame1)
        self.prog_label.configure(text='    0%')
        self.prog_label.pack(side="right")
        frame1.pack(side="top")
        self.mark_label = ttk.Label(master)
        self.mark_label.configure(text='mark')
        self.mark_label.pack(side="top")

    def make_move_proccess(self, n: int):
        curr_pos = self.prog_bar.get()          # get the current position
        if n >= 0:
            curr_pos = min(curr_pos + n, self.max_size)
        else:
            curr_pos = max(curr_pos + n, 0)
        self.prog_label['text'] = self.FORMAT_PERC.format(self.get_percent_fixed(curr_pos, self.max_size))
        self.prog_bar.set(curr_pos)

    @staticmethod
    def get_percent_fixed(n, max_num: int = 100, after_dot=2):
        n = n / max_num * 100
        if n.is_integer():
            return int(n)
        else:
            return round(n, after_dot)
