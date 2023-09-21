#!/usr/bin/python3
import time
import tkinter as tk
import tkinter.ttk as ttk
from DB.dns_db import *
from GUI.widgets.combobox_widget import *
from dns_engine.dns_req_machine import DNS_FP_runner
from GUI.confirm_window import ConfirmDeatilsWindow, ConfirmWinTry
from GUI.helper_classes.window import Window

class MainWindow(Window):
    NAMES = ['Gilad', 'David', 'Irit']
    def __init__(self, wind_master: Window = None, db = DNSJsonDB()):
        # build ui
        super().__init__(wind_master=wind_master)

        #self.__set_validation_widget(self.combo_tester_name)
        self.db = db
        self.set_checkbox_options()

        # Main widget
        self.mainwindow = self.toplevel

    def init_window(self):
        self.toplevel.configure(height=200, width=200)
        self.toplevel.geometry("1152x768")
        self.toplevel.title("DNS FP Make Test")
        self.frame1 = ttk.Frame(self.toplevel)
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
        self.session_name_text = tk.StringVar()
        self.entry_session_name = ttk.Entry(self.frame1, textvariable=self.session_name_text)
        self.entry_session_name.grid(column=2, row=8, sticky="ew")
        self.button1 = ttk.Button(self.frame1)
        self.button1.configure(text='RUN')
        self.button1.grid(column=2, row=10)
        self.button1.configure(command=self.run_test)
        self.combo_tester_name = ComboBoxWidget(self.frame1)
        self.combo_tester_name.configure(width=25)
        self.combo_tester_name.grid(column=2, row=0, sticky="ew")

        self.combo_site = ComboBoxWidget(self.frame1)
        self.combo_site.grid(column=2, row=2, sticky="ew")
        self.combo_dns_servers = ComboBoxWidget(self.frame1)
        self.combo_dns_servers.grid(column=2, row=4, sticky="ew")
        self.combo_domain_names = ComboBoxWidget(self.frame1)
        self.combo_domain_names.grid(column=2, row=6, sticky="ew")
        self.frame1.pack(side="top")
        self.frame1.rowconfigure(1, minsize=20)
        self.frame1.rowconfigure(3, minsize=20)
        self.frame1.rowconfigure(5, minsize=20)
        self.frame1.rowconfigure(7, minsize=20)
        self.frame1.rowconfigure(9, minsize=30)
        self.frame1.rowconfigure("all", minsize=20)
        self.frame1.columnconfigure(1, minsize=5)
        self.frame1.columnconfigure("all", minsize=20)

    def run(self):
        self.mainwindow.mainloop()

    def run_test(self):

        print('button clicked')
        print('selected', self.combo_tester_name.get())
        print(self.combo_dns_servers.get())
        tester_name = self.combo_tester_name.get()
        site = self.combo_site.get()
        selected_srv_nams, dns_servers = self.combo_dns_servers.get()
        selected_dm_nams, domain_names = self.combo_domain_names.get()
        session_name = DNS_FP_runner.gen_session_name(self.session_name_text.get())     # already checks if good

        print('tester:', tester_name)
        print('site:', site)
        print('dns servers:', selected_srv_nams, dns_servers)
        print('domain names:', selected_dm_nams, domain_names)
        print('session name:', session_name)
        confirm_details_win = ConfirmDeatilsWindow(tester=tester_name, site=site,
                                                   dns_servers=(selected_srv_nams, dns_servers),
                                                   domain_names=(selected_dm_nams, domain_names), session_name=session_name)

        #from GUI.widgets.table_widget import create_table_window
        conf = ConfirmWinTry(self, *confirm_details_win.get_as_table_data())
        # conf.show_window()
        self.hide_window()
        print("end click")



    def set_checkbox_options(self):
        self.combo_tester_name.set_values_selection(self.NAMES)
        self.combo_site.set_values_selection(self.db.get_sites())
        self.combo_dns_servers.set_values_selection(self.db.get_dns_server_ip())
        self.combo_domain_names.set_values_selection(self.db.get_domain_names())

    # def valid_session_name(self):
    #     session = self.session_name_text.get()
    #     return session != '' and True   # TODO: add checkbox near




if __name__ == "__main__":
    app = MainWindow()
    app.run()

