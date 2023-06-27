#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from ttkwidgets.autocomplete.autocompletecombobox import AutocompleteCombobox
from DB.dns_db import *
from GUI.widgets.combobox_widget import ComboBoxWidget


class MainWindow:
    NAMES = ['Gilad', 'David', 'Irit']
    def __init__(self, master=None, db = DnsDBFiles()):
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
        self.label2 = ttk.Label(self.frame1)
        self.label2.configure(text='site:')
        self.label2.grid(column=0, row=2)
        self.label3 = ttk.Label(self.frame1)
        self.label3.configure(text='DNS servers:')
        self.label3.grid(column=0, row=4)
        self.label4 = ttk.Label(self.frame1)
        self.label4.configure(text='Domain Names:')
        self.label4.grid(column=0, row=6)
        self.label5 = ttk.Label(self.frame1)
        self.label5.configure(text='Session Name:')
        self.label5.grid(column=0, row=8)
        self.entry2 = ttk.Entry(self.frame1)
        self.entry2.grid(column=2, row=8, sticky="ew")
        self.button1 = ttk.Button(self.frame1)
        self.button1.configure(text='RUN')
        self.button1.grid(column=2, row=10)
        self.button1.configure(command=self.run_test)
        my_list = ['1', '2']
        self.autocompletecombobox1 = ComboBoxWidget(
            self.frame1, values_selection=my_list)#, completevalues=self.NAMES)
        my_list.append('3')
        self.autocompletecombobox1.print()
        self.autocompletecombobox1.configure(validate="focusout", width=25)
        self.autocompletecombobox1.grid(column=2, row=0, sticky="ew")
        # _validatecmd = (
        #     self.autocompletecombobox1.register(
        #         self.checkbox_validate), "%P")
        # self.autocompletecombobox1.configure(validatecommand=_validatecmd)
        # _validatecmd = (
        #     self.autocompletecombobox1.register(
        #         self.on_invalid), "%P", '%S', self.autocompletecombobox1)

        self.autocompletecombobox2 = AutocompleteCombobox(self.frame1)
        self.autocompletecombobox2.grid(column=2, row=2, sticky="ew")
        self.autocompletecombobox3 = AutocompleteCombobox(self.frame1)
        self.autocompletecombobox3.grid(column=2, row=4, sticky="ew")
        self.autocompletecombobox4 = AutocompleteCombobox(self.frame1)
        self.autocompletecombobox4.grid(column=2, row=6, sticky="ew")
        self.frame1.pack(side="top")
        self.frame1.rowconfigure(1, minsize=20)
        self.frame1.rowconfigure(3, minsize=20)
        self.frame1.rowconfigure(5, minsize=20)
        self.frame1.rowconfigure(7, minsize=20)
        self.frame1.rowconfigure(9, minsize=30)
        self.frame1.rowconfigure("all", minsize=20)
        self.frame1.columnconfigure(1, minsize=5)
        self.frame1.columnconfigure("all", minsize=20)

        self.__set_validation_widget(self.autocompletecombobox1)
        self.db = db
        # self.set_checkbox_options()

        # Main widget
        self.mainwindow = self.toplevel1


    def run(self):
        self.mainwindow.mainloop()

    def run_test(self):
        print('button clicked')

    def set_checkbox_options(self):
        self.autocompletecombobox1['completevalues'] = self.NAMES
        self.autocompletecombobox3['completevalues'] = self.db.get_list_dns_server_ip()


    @staticmethod
    def __checkbox_validate(widget):
        def checkbox_validate_inner(p_entry_value):
            return p_entry_value in widget['completevalues'] or p_entry_value == ''
        return checkbox_validate_inner

    @staticmethod
    def __on_invalid(widget):
        def on_invalid_inner(p_entry_value, s_prev_value):
            messagebox.showerror('error tester name', f'{p_entry_value} is not on the list')
            widget.set('')

        return on_invalid_inner

    @staticmethod
    def __make_ivalid(widget):
        widget.configure(
            invalidcommand=(widget.register(MainWindow.__on_invalid(widget)), "%P", '%S'))  # tring to make it short as function

    @staticmethod
    def __make_valid(widget):
        widget.configure(validatecommand=(widget.register(MainWindow.__checkbox_validate(widget)), "%P"))

    @staticmethod
    def __set_validation_widget(widget):
        MainWindow.__make_ivalid(widget)
        MainWindow.__make_valid(widget)



if __name__ == "__main__":
    app = MainWindow()
    app.run()
