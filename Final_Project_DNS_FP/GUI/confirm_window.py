from typing import Iterable

from GUI.helper_classes.window import Window


class ConfirmDeatilsWindow:
    COLUMNS = ('title', 'selction', 'more')
    def __init__(self, tester, site, dns_servers, domain_names, session_name):
        self.tester = tester
        self.site = site
        self.dns_servers = dns_servers
        self.domain_names = domain_names
        self.session_name = session_name

        # for k in self.__dict__.keys():
        #     print(k)
        print(list(self.__dict__))

    def get_as_table_data(self):
        '''
        the function makes from the details the data in the format of the table that tkinter wants
        :return: tuple[2]: (columns, the whole data as list of tuples)
        '''
        col_len = len(self.COLUMNS)
        lines = []
        for arg in self.__dict__:
            val = self.__getattribute__(arg)        # get the value of the field
            title = arg.replace('_', ' ').title()     # replace the '_' with space for title presentation

            try:
                assert not isinstance(val, str)
                val = tuple(val)
            except:
                val = (val,)        # if not iterable type then make it as tuple with simple value
            # append a tuple of the title (singel), and the rest of the val.
            # after that make sure that there is no more than the columns amount
            curr_line = ((title,) + val)[:col_len]
            # fill the tuple to the size of the amount of the columns
            # *note* if the amount is non-positive nothing will be added
            curr_line += ('',)*(col_len - len(curr_line))
            # add the line to the list of lines
            lines += [curr_line]
        return tuple(self.COLUMNS), lines



a = (1,2,3,4,5)
a += ('',)*(3-len(a))
print(a[:3])
a = (1,2,3)
a = tuple(a)

print(a[1])
# a[1] = 3
# print(a[1])


'''
*************************************************************************

                                try area

*************************************************************************
'''

import tkinter as tk
import tkinter.ttk as ttk

from utils.utils import *

class ConfirmWinTry(Window):

    # define our column
    CLMN_NAME = 'column name'
    CLMN_TXT = 'column text'

    def __init__(self, wind_master: Window, columns, lines):
        super().__init__(wind_master)
        self.create_table_window(columns, lines)

    def create_table_window(self, columns, lines):
        # columns, lines = table_overlook_repair(columns, lines)
        print(columns, lines, sep='\n'+"*"*50+'\n')

        self.toplevel.title('PythonGuides')
        self.toplevel.geometry('1152x768')
        # self.toplevel['bg'] = '#AC99F2'

        frame = ttk.Frame(self.toplevel)
        frame.pack(fill=tk.BOTH, expand=True)

        # scrollbar
        frame_scroll_y = ttk.Scrollbar(frame)
        frame_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        frame_scroll_x = ttk.Scrollbar(frame, orient='horizontal')
        frame_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        table = ttk.Treeview(frame, yscrollcommand=frame_scroll_y.set, xscrollcommand=frame_scroll_x.set)

        table.pack(fill=tk.BOTH, expand=True)

        frame_scroll_y.config(command=table.yview)
        frame_scroll_x.config(command=table.xview)

        #set the table data
        self.set_data_to_tables(table_widg=table, columns=columns, lines=lines)
        btn = ttk.Button(self.toplevel, text='CLICK')
        btn.pack(side=tk.TOP)


    def btn_function(self):
        self.set_show_prev_wind(False)
        self.destroy_wind()

    def set_data_to_tables(self, table_widg, columns, lines):
        table_widg['columns'] = columns
        keys_of_cols = {}

        # format our column
        table_widg.column("#0", width=20, anchor=tk.CENTER, stretch=tk.NO)
        table_widg.heading("#0", text="", anchor=tk.CENTER)
        is_first = True
        for title_og in columns:

            col_var = replace_whitespace(title_og, replacement='_').lower()
            col_text = col_var.replace('_', ' ').title()

            try:
                table_widg.column(col_var, anchor=tk.CENTER, stretch=tk.YES)    # sometimes name can trigger the try_catch
            except:
                col_var = replace_whitespace(title_og, replacement='_')
                table_widg.column(col_var, anchor=tk.CENTER, stretch=tk.YES)
            finally:
                table_widg.heading(col_var, text=col_text, anchor=tk.CENTER)

        for line in lines:
            if not isinstance(line[2], Iterable) or isinstance(line[2], str):
                table_widg.insert(parent='', index='end', values=line)
                continue
            row = table_widg.insert(parent='', index='end', values=line[:2] + ('...',))
            for val in line[2]:
                table_widg.insert(parent=row, index='end', values=('', '', val))
