#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class TryWindGUI:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.geometry("800x600")
        frame1 = ttk.Frame(toplevel1)
        frame1.configure(height=200, width=200)
        label1 = ttk.Label(frame1)
        label1.configure(text='select tester:')
        label1.pack(side="top")
        combobox2 = ttk.Combobox(frame1)
        combobox2.configure(values=['Gilad', 'David', 'Irit'])
        combobox2.pack(side="top")
        frame1.pack(side="top")
        self.progressbar1 = ttk.Progressbar(toplevel1)
        self.prog_bar = tk.IntVar(value=0)
        self.progressbar1.configure(
            length=200,
            orient="horizontal",
            value=0,
            maximum=100,
            variable=self.prog_bar)
        self.progressbar1.pack(side="top")
        frame2 = ttk.Frame(toplevel1)
        frame2.configure(height=200, width=300)
        button2 = ttk.Button(frame2)
        button2.configure(text='+')
        button2.pack(side="right")
        button2.configure(command=self.up_val)
        button3 = ttk.Button(frame2)
        button3.configure(text='-')
        button3.pack(side="right")
        button3.configure(command=self.down_val)
        frame2.pack(expand=False, side="top")
        label3 = ttk.Label(toplevel1)
        label3.configure(text='\n')
        label3.pack(side="top")
        self.label4 = ttk.Label(toplevel1)
        self.label4.configure(cursor="arrow", text='percent')
        self.label4.pack(side="top")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def make_move_proccess(self, n: int):
        curr_pos = self.prog_bar.get()
        max_num = self.progressbar1['maximum']
        if n >= 0:
            curr_pos = min(curr_pos + n, max_num)
        else:
            curr_pos = max(curr_pos + n, 0)
        self.label4['text'] = f'{self.get_percent_fixed(curr_pos, max_num)}%'
        self.prog_bar.set(curr_pos)

    @staticmethod
    def get_percent_fixed(n, max_num = 100, after_dot=2):
        n = n / max_num * 100
        if n.is_integer():
            return int(n)
        else:
            return round(n, after_dot)

        

    def up_val(self):
        #   self.prog_bar.set(self.prog_bar.get() + 10)
        self.make_move_proccess(10)

    def down_val(self):
        self.make_move_proccess(-10)


if __name__ == "__main__":
    print(f'{round(0.69999, 3)}')
    app = TryWindGUI()
    app.run()
