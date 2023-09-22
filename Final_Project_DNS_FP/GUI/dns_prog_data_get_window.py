import pprint
from time import sleep

from DB.dns_db import DnsDBFiles
from GUI.helper_classes.window import Window
from GUI.widgets.progress_widegt.gui_prog_bar_control import ctor_control_prog_by_widget
from GUI.widgets.progress_widegt.prog_widget import ProgressWidget
import tkinter as tk
import tkinter.ttk as ttk

from dns_engine.dns_req_machine import *


class DNSDataProgWin(Window):
    def __init__(self, wind_master: Window = None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        super().__init__(wind_master=wind_master)


    
    def init_window(self):
        # self.toplevel.configure(height=200, width=200)
        self.toplevel.geometry("1024x768")
        self.frame2 = ttk.Frame(self.toplevel)
        self.frame2.configure(height=200, width=200)

        self.prog_frame_dns_ip = ProgressWidget(self.frame2, total=100, jump=10)
        self.prog_frame_dns_ip.grid(row=0, columnspan=2, sticky="ew")
        self.ip_bar_class_maker = ctor_control_prog_by_widget(self.prog_frame_dns_ip)
        
        self.prog_frame_domain_names = ProgressWidget(self.frame2, jump=10)  # jump 15
        self.prog_frame_domain_names.grid(row=1, columnspan=2, sticky="ew")
        self.domain_names_bar_class_maker = ctor_control_prog_by_widget(self.prog_frame_domain_names)

        self.prog_frame_wait_bar = ProgressWidget(self.frame2, jump=20)
        self.prog_frame_wait_bar.grid(row=2, columnspan=2, sticky="ew")
        self.wait_bar_class_maker = ctor_control_prog_by_widget(self.prog_frame_wait_bar)

        self.prog_frame_upload_data = ProgressWidget(self.frame2)
        self.prog_frame_upload_data.grid(row=3, columnspan=2, sticky="ew")

        self.show_run_4 = True

        # self.widget_control_2 = ctor_control_prog_by_widget(self.prog_frame_domain_names)(jump=15, title="second by try")
        # self.class_control_prog_4 = ctor_control_prog_by_widget(self.prog_frame_upload_data)
        button3 = ttk.Button(self.frame2)
        button3.configure(text='press me')
        button3.configure(command=self.push_all)
        button3.grid(row=4)
        self.prog_frame_upload_data.grid(row=3, columnspan=2)
        # Main widget
        self.frame2.pack(side="top")



    def push_all(self):

        # self.prog_frame_dns_ip.update_bar()
        #
        # self.widget_control_2()  # self.prog_frame_domain_names.update_bar()
        #
        # self.prog_frame_wait_bar()  # self.prog_frame_wait_bar.update_bar()
        #
        # # this is for checking the hiding method
        # if self.show_run_4:
        #     self.prog_frame_upload_data.show_prog_bar()
        #     with self.class_control_prog_4(jump=25, title='"with-as" bar 4') as bar:
        #         num_rounds = bar.total_rounds()
        #         for i in range(num_rounds):
        #             bar()
        #             sleep(0.5)
        # else:
        #     self.prog_frame_upload_data.hide_prog_bar()

        self.show_run_4 = not self.show_run_4
        # self.mainwindow.update()
        self.make_run_session(*self.args, **self.kwargs)


    def set_all_widgets_in_order(self):
        for widget in self.frame2.winfo_children():
            # if the widget is already in the grid continue
            if len(widget.grid_info()) > 0:
                continue
            cols, rows = self.frame2.grid_size()
            widget.grid(row=rows, column=0)

    def make_run_session(self, DNS_address_list: list = [], list_names: list = [], session_name: str = '',
                         repeats: int = 8, interval_wait_sec: int = INTERVAL_WAIT_SEC, is_first_rec: bool = True,
                         to_show_results: bool = True, json_file_name: str = JSON_FILE_NAME_DEFAULT):
        self.run_data = run_session_ip_list(DNS_address_list=DNS_address_list, list_names=list_names,
                                            session_name=session_name,
                                            repeats=repeats, interval_wait_sec=interval_wait_sec,
                                            is_first_rec=is_first_rec,
                                            to_show_results=to_show_results, json_file_name=json_file_name,
                                            progerss_bar_ip=self.ip_bar_class_maker,
                                            progerss_bar_domain=self.domain_names_bar_class_maker,
                                            prog_wait_class=self.wait_bar_class_maker)
        pprint.pprint(self.run_data)


dns_db = DnsDBFiles()
names = dns_db.get_list_domain_names()
# runner = DNS_FP_runner('8.8.8.8', names)
# print("started")
# run_result = runner.run_names_with_dns(is_recursive=False)
#
# for name in run_result:
#     print(f'{name}:')
#     pprint.pprint(runner.get_data_from_pkts(run_result[name]))
# return_data = run_session_ip_list(['8.8.8.8'], list_names=names)
dns_prog_run = DNSDataProgWin(DNS_address_list=['8.8.8.8'], list_names=names)
dns_prog_run.run_window()