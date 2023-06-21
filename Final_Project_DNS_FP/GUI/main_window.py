#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class MainWindow:
    def __init__(self, master=None):
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.toplevel1.configure(height=200, width=200)
        self.toplevel1.geometry("1152x768")
        self.toplevel1.title("DNS FP Make Test")
        self.frame1 = ttk.Frame(self.toplevel1)
        self.frame1.configure(height=700, width=700)
        self.label1 = ttk.Label(self.frame1)
        self.label1.configure(text='tester name:')
        self.label1.grid(column=0, row=0)
        self.combobox1 = ttk.Combobox(self.frame1)
        self.combobox1.configure(values=['Gilad', 'David', 'Irit'], width=25)
        self.combobox1.grid(column=2, row=0, sticky="ew")
        self.label2 = ttk.Label(self.frame1)
        self.label2.configure(text='site:')
        self.label2.grid(column=0, row=2)
        self.combobox2 = ttk.Combobox(self.frame1)
        self.combobox2.grid(column=2, row=2, sticky="ew")
        self.label3 = ttk.Label(self.frame1)
        self.label3.configure(text='DNS servers:')
        self.label3.grid(column=0, row=4)
        self.combobox3 = ttk.Combobox(self.frame1)
        self.combobox3.grid(column=2, row=4, sticky="ew")
        self.label4 = ttk.Label(self.frame1)
        self.label4.configure(text='Domain Names:')
        self.label4.grid(column=0, row=6)
        self.combobox4 = ttk.Combobox(self.frame1)
        self.combobox4.grid(column=2, row=6, sticky="ew")
        self.label5 = ttk.Label(self.frame1)
        self.label5.configure(text='Session Name:')
        self.label5.grid(column=0, row=8)
        self.entry2 = ttk.Entry(self.frame1)
        self.entry2.grid(column=2, row=8, sticky="ew")
        self.button1 = ttk.Button(self.frame1)
        self.button1.configure(text='RUN')
        self.button1.grid(column=2, row=10)
        self.button1.configure(command=self.run_test)
        self.frame1.pack(side="top")
        self.frame1.rowconfigure(1, minsize=20)
        self.frame1.rowconfigure(3, minsize=20)
        self.frame1.rowconfigure(5, minsize=20)
        self.frame1.rowconfigure(7, minsize=20)
        self.frame1.rowconfigure(9, minsize=30)
        self.frame1.rowconfigure("all", minsize=20)
        self.frame1.columnconfigure(1, minsize=5)
        self.frame1.columnconfigure("all", minsize=20)

        # Main widget
        self.mainwindow = self.toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def run_test(self):
        pass


if __name__ == "__main__":
    app = MainWindow()
    app.run()
